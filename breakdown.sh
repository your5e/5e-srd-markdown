#!/usr/bin/env -S bash -euo pipefail

source lib/headers.sh

function main {
    extract_only=0
    match_pattern=""
    quiet=0
    ignore_headers=1
    fix_headers=1
    check_headers=1
    force_write=0

    while getopts "acefhm:qs" option; do
        case "$option" in
            a)  force_write=1 ;;
            c)  check_headers=0 ;;
            e)  extract_only=1 ;;
            f)  fix_headers=0 ;;
            h)  usage ;;
            m)  match_pattern="$OPTARG"; extract_only=1 ;;
            q)  quiet=1 ;;
            s)  ignore_headers=0 ;;
            *)  abort ;;
        esac
    done
    shift $((OPTIND-1))

    [ "$#" -lt 1 ] && abort

    source_file="$1"
    source_dir=$(dirname "$source_file")
    [ ! -f "$source_file" ] && abort "Source file '$source_file' not found"

    command_file="${2:-$source_dir/breakdown.txt}"
    [ ! -f "$command_file" ] && abort "Command file '$command_file' not found"


    mapfile -t original < "$source_file"
    local last_range_start=0
    local last_line_used=0
    declare -a errors=()
    declare -a lines_claimed=()
    declare -A files_seen=()
    declare -A files_written=()
    declare -A fragment_positions=()
    declare -a output=()
    declare -a commands=()

    while IFS= read -r line; do
        commands+=("$line")
    done < <(
        # filter blanks/comments
        sed 's/^[[:space:]]*//; s/#.*$//; s/[[:space:]]*$//; /^$/d' "$command_file"
    )

    for line in "${commands[@]}"; do
        parse_breakdown_line \
            "$line" start end action target_file padding_or_offset offset

        if [[ "$start" =~ ^@ ]]; then
            output+=("$start $end")
            continue
        fi

        if [[ "$action" != "extract" && "$action" != "append" ]]; then
            errors+=("${start}-${end}  - missing action")
            continue
        fi

        if [ $start -le $last_range_start ]; then
            errors+=("${start}-${end} ${target_file} - not in numerical order")
            continue
        fi
        last_range_start=$start

        if [ $start -gt $end ]; then
            errors+=("${start}-${end} ${target_file} - descending line numbers")
            continue
        fi

        if [ $end -gt $(wc -l < "$source_file") ]; then
            errors+=("${start}-${end} ${target_file} - lines beyond the source")
            continue
        fi

        if [ -n "$target_file" ]; then
            if [ -n "${files_seen[$target_file]:-}" ] \
                && [ "$action" = "extract" ]; \
            then
                errors+=("${start}-${end} ${target_file} - duplicate filename")
                continue
            fi
            files_seen[$target_file]="${start}-${end}"
        fi

        for index in $(seq $start $end); do
            if [ -n "${lines_claimed[$index]:-}" ]; then
                local overlap="${lines_claimed[$index]}"
                errors+=("${start}-${end} ${target_file} - overlaps with $overlap")
                break
            fi
            lines_claimed[$index]="$target_file"
        done

        if [ ${#errors[@]} = 0 -a $extract_only -eq 0 ]; then
            if [ $last_line_used -lt $((start-1)) ]; then
                for index in $(seq $last_line_used $((start-2))); do
                    output+=("${original[$index]}")
                done
            fi

            # calculate fragment position
            local fragment_lines=$((end - start + 1))

            if [ "$action" = "append" ]; then
                # for append, calculate position in combined fragment
                local current_pos=${fragment_positions[$target_file]:-0}
                if [ $current_pos -gt 0 ]; then
                    # not the first append, blank line separator
                    current_pos=$((current_pos + 1))
                fi
                local fragment_start=$((current_pos + 1))
                local fragment_end=$((fragment_start + fragment_lines - 1))
                fragment_positions[$target_file]=$fragment_end
            else
                # for extract, always start from 1
                local fragment_start=1
                local fragment_end=$fragment_lines
                fragment_positions[$target_file]=$fragment_end
            fi

            # the last two params (when both provided) are the padding
            # indicator "-" and the offset adjustment -- but padding
            # is optional so this could contain the offset
            local offset_param=""
            if [ "$padding_or_offset" = "-" ]; then
                offset_param="$offset"
                if [ -n "$offset_param" ]; then
                    local range="$fragment_start-$fragment_end"
                    output+=(
                        "@include- $offset_param $range $target_file"
                    )
                else
                    local range="$fragment_start-$fragment_end"
                    output+=("@include-   $range $target_file")
                fi
            else
                offset_param="$padding_or_offset"
                if [ -n "$offset_param" ]; then
                    local range="$fragment_start-$fragment_end"
                    output+=(
                        "@include  $offset_param $range $target_file"
                    )
                else
                    local range="$fragment_start-$fragment_end"
                    output+=("@include    $range $target_file")
                fi
            fi

            [ "$padding_or_offset" = "-" ] \
                && last_line_used=$end \
                || last_line_used=$((end + 1))
        fi
    done

    if [ ${#errors[@]} -gt 0 ]; then
        printf '%s\n' "${errors[@]}" >&2
        exit 1
    fi

    local start_width=0
    local end_width=0
    for line in "${commands[@]}"; do
        parse_breakdown_line \
            "$line" start end action target_file padding_or_offset offset

        [[ "$start" =~ ^@ ]] \
            && continue
        [ "${#start}" -gt "$start_width" ] \
                && start_width="${#start}"
        [ "${#end}" -gt "$end_width" ] \
                && end_width="${#end}"
    done

    for line in "${commands[@]}"; do
        parse_breakdown_line \
            "$line" start end action target_file padding_or_offset offset

        [[ "$start" =~ ^@ ]] \
            && continue
        [[ -n "$match_pattern" && ! "$target_file" =~ $match_pattern ]] \
            && continue

        if extract_file \
            "$source_file" \
            "$start" \
            "$end" \
            "$source_dir/$target_file" \
            "$ignore_headers" \
            "$action" \
            0 \
            0 \
            "$force_write"; \
        then
            files_written[$target_file]=1
            [ $quiet -eq 1 ] \
                && continue

            if [[ ! -t 1 ]]; then
                if [ "$action" = "append" ]; then
                    printf "%*s-%-*s >> %s\n" \
                        "$start_width" "$start" "$end_width" "$end" "$target_file"
                else
                    printf "%*s-%-*s >  %s\n" \
                        "$start_width" "$start" "$end_width" "$end" "$target_file"
                fi
            else
                if [ "$action" = "append" ]; then
                    printf '%-118s\r' "$(
                        printf "%*s-%-*s >> %s" \
                            "$start_width" "$start" "$end_width" "$end" "$target_file"
                    )"
                else
                    printf '%-118s\r' "$(
                        printf "%*s-%-*s >  %s" \
                            "$start_width" "$start" "$end_width" "$end" "$target_file"
                    )"
                fi
            fi
        fi
    done

    if [ $extract_only -eq 0 ]; then
        if [ $last_line_used -lt ${#original[@]} ]; then
            for index in $(seq $last_line_used $((${#original[@]}-1))); do
                output+=("${original[$index]}")
            done
        fi
        printf '%s\n' "${output[@]}" > "$source_file"
    fi

    if [ "$fix_headers" -eq 1 ] || [ "$check_headers" -eq 1 ]; then
        for target_file in "${!files_written[@]}"; do
            local target_path="$source_dir/$target_file"
            [ ! -f "$target_path" ] && continue

            if [ "$fix_headers" -eq 1 ]; then
                if [[ "$target_path" =~ /statblocks/ ]]; then
                    fix_statblock_headers "$target_path" 2>/dev/null || true
                else
                    fix_headers "$target_path" 2>/dev/null || true
                fi
            fi
            [ "$check_headers" -eq 1 ] \
                && check_header_progression "$target_path" || true

            if [ $quiet -eq 0 ]; then
                if [[ ! -t 1 ]]; then
                    printf "%*s#  %s\n" \
                        "$((start_width + end_width + 2))" \
                        "" "$target_file"
                else
                    printf '%-118s\r' "$(
                        printf "%*s#  %s" \
                            "$((start_width + end_width + 2))" \
                            "" "$target_file"
                    )"
                fi
            fi
        done
    fi
}

function extract_file {
    local source_file="$1"
    local start="$2"
    local end="$3"
    local target_path="$4"
    local ignore_headers="$5"
    local action="${6:-extract}"
    local fix_headers_flag="${7:-1}"
    local check_headers_flag="${8:-1}"
    local force_write="${9:-0}"

    local files_differ=0
    local new_content=$(sed -n "${start},${end}p" "$source_file")

    mkdir -p "$(dirname "$target_path")"

    if [ "$force_write" -eq 1 ]; then
        files_differ=1
    elif [ ! -f "$target_path" ]; then
        files_differ=1
    elif [ "$action" = "append" ]; then
        files_differ=1
    elif [ "$ignore_headers" -eq 1 ]; then
        # compare ignoring header depth
        if [ \
            "$(echo "$new_content" | sed 's/^##* *//')" \
            != "$(sed 's/^##* *//' "$target_path")" \
        ]; then
            files_differ=1
        fi

    else
        if [ "$new_content" != "$(cat "$target_path")" ]; then
            files_differ=1
        fi
    fi

    if [ $files_differ -eq 1 ]; then
        if [ "$action" = "append" ]; then
            echo "" >> "$target_path"
            echo "$new_content" >> "$target_path"
        else
            echo "$new_content" > "$target_path"
        fi
        if [ "$fix_headers_flag" -eq 1 ]; then
            if [[ "$target_path" =~ /statblocks/ ]]; then
                fix_statblock_headers "$target_path" 2>/dev/null || true
            else
                fix_headers "$target_path" 2>/dev/null || true
            fi
        fi
        [ "$check_headers_flag" -eq 1 ] \
            && check_header_progression "$target_path" || true
        return 0
    fi

    return 1
}

function parse_breakdown_line {
    local line="$1"
    local -n start_ref=$2
    local -n end_ref=$3
    local -n action_ref=$4
    local -n target_file_ref=$5
    local -n padding_or_offset_ref=$6
    local -n offset_ref=$7
    local remainder

    read -r start_ref end_ref action_ref remainder <<< "$line"

    if [[ "$start_ref" =~ ^@ ]]; then
        action_ref=""
        target_file_ref=""
        padding_or_offset_ref=""
        offset_ref=""
        return
    fi

    if [ -z "$start_ref" -o -z "$end_ref" -o -z "$action_ref" ] \
        || ! [[ "$start_ref" =~ ^[1-9][0-9]*$ ]] \
        || ! [[ "$end_ref" =~ ^[1-9][0-9]*$ ]];
    then
        start_ref=""
        end_ref=""
        action_ref=""
        target_file_ref=""
        padding_or_offset_ref=""
        offset_ref=""
        return
    fi

    # strip leading whitespace from remainder
    remainder="${remainder#"${remainder%%[![:space:]]*}"}"

    if [[ "${remainder:0:1}" == '"' ]]; then
        local filename=""
        local index=1
        local char
        local found_closing_quote=0

        # parse quoted filename character by character to handle escapes
        while [ $index -lt ${#remainder} ]; do
            char="${remainder:$index:1}"

            if [ "$char" == '\' ]; then
                # backslash escapes next character
                ((index++))
                filename+="${remainder:$index:1}"
            elif [ "$char" == '"' ]; then
                # closing quote
                ((index++))
                found_closing_quote=1
                break
            else
                filename+="$char"
            fi
            ((index++))
        done

        if [ $found_closing_quote -eq 0 ]; then
            start_ref=""
            end_ref=""
            action_ref=""
            target_file_ref=""
            padding_or_offset_ref=""
            offset_ref=""
            return
        fi

        target_file_ref="$filename"
        remainder="${remainder:$index}"
        read -r padding_or_offset_ref offset_ref <<< "$remainder"
    else
        read -r target_file_ref padding_or_offset_ref offset_ref <<< "$remainder"
    fi
}

function usage {
    exec perldoc -T "$0"
}

function abort {
    if [ -n "${1:-}" ]; then
        echo "${2:-Error}: $1" >&2
    fi
    perldoc -T -u "$0" | sed -n '/^=head1 SYNOPSIS/,/^=head1/p' | sed '1d;$d' >&2
    exit 1
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

: <<'=cut'
=head1 NAME

breakdown.sh - Extract sections from a markdown file into separate files

=head1 SYNOPSIS

breakdown.sh [-a] [-c] [-e] [-f] [-h] [-m pattern] [-q] [-s] file.md [breakdown.txt]

=head1 DESCRIPTION

Turns the one-big-file Markdown of an SRD into multiple small files for
easier reference. Reads a breakdown file containing line ranges and target
filenames, then extracts those ranges into separate files.

=head1 OPTIONS

=over 4

=item B<-a>

Always write files even if content hasn't changed

=item B<-c>

Disable header progression checking after extraction

=item B<-e>

Extract only mode - create fragment files but don't modify the source file

=item B<-f>

Disable automatic header fixing during extraction

=item B<-h>

Show this help documentation

=item B<-s>

Strict comparison - disable ignoring header depth when comparing files (by
default header depth differences are ignored; this flag makes comparison exact)

=item B<-m pattern>

Extract only files matching the given pattern (implies -e)

=item B<-q>

Quiet mode - suppress progress output

=back

=head1 ARGUMENTS

=over 4

=item B<file.md>

Source markdown file to break down (required)

=item B<breakdown.txt>

File containing extraction commands (defaults to breakdown.txt in same
directory as source file)

=back

=head1 BREAKDOWN FILE FORMAT

Each line in the breakdown file specifies a range of lines to extract:

    start-end [action] target_file [-]

Where:

=over 4

=item B<start-end>

Line range to extract from source file

=item B<action>

Optional action: extract (default), append, or remove

=item B<target_file>

Path to output file (relative to source directory)

=item B<->

Optional trailing dash to suppress blank line after @include directive

=back

Lines starting with @ are preserved as-is in the modified source file.
Comments (# to end of line) and blank lines are ignored.

=head1 EXAMPLES

Extract sections 5-11 and 14-20 into separate files:

    5-11 extract sections/section_one.md
    14-20 extract sections/section_two.md

Append multiple sections to a single file:

    4-4 extract sections/combined.md
    9-9 append sections/combined.md

Remove a section from the source file:

    100-150 remove

=cut
