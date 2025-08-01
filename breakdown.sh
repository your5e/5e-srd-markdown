#!/usr/bin/env -S bash -euo pipefail

function main {
    extract_only=0
    match_pattern=""
    quiet=0

    while getopts "ehm:q" option; do
        case "$option" in
            e)  extract_only=1 ;;
            m)  match_pattern="$OPTARG"; extract_only=1 ;;
            q)  quiet=1 ;;
            *)  usage ;;
        esac
    done
    shift $((OPTIND-1))

    [ "$#" -lt 1 ] && usage

    source_file="$1"
    source_dir=$(dirname "$source_file")
    [ ! -f "$source_file" ] && abort "Source file '$source_file' not found"

    command_file="${2:-$source_dir/breakdown.txt}"
    [ ! -f "$command_file" ] && abort "Command file '$command_file' not found"


    mapfile -t original < "$source_file"
    local source_line_count=$(wc -l < "$source_file")
    local last_range_start=0
    local last_line_used=0
    declare -a errors=()
    declare -a lines_claimed=()
    declare -A files_seen=()
    declare -a output=()
    declare -a commands=()

    while IFS= read -r line; do
        commands+=("$line")
    done < <(
        # filter blanks/comments
        sed 's/^[[:space:]]*//; s/#.*$//; s/[[:space:]]*$//; /^$/d' "$command_file"
    )

    for line in "${commands[@]}"; do
        read -r start_line end_line target_file fourth_param fifth_param <<< "$line"

        if [[ "$start_line" =~ ^@ ]]; then
            output+=("$start_line $end_line")
            continue
        fi

        if [ $start_line -le $last_range_start ]; then
            errors+=("${start_line}-${end_line} ${target_file} - not in numerical order")
            continue
        fi
        last_range_start=$start_line

        if [ $start_line -gt $end_line ]; then
            errors+=("${start_line}-${end_line} ${target_file} - descending line numbers")
            continue
        fi

        if [ $end_line -gt $source_line_count ]; then
            errors+=("${start_line}-${end_line} ${target_file} - lines beyond the source")
            continue
        fi

        if [ -n "${files_seen[$target_file]:-}" ]; then
            errors+=("${start_line}-${end_line} ${target_file} - duplicate filename")
            continue
        fi
        files_seen[$target_file]="${start_line}-${end_line}"

        for index in $(seq $start_line $end_line); do
            if [ -n "${lines_claimed[$index]:-}" ]; then
                errors+=("${start_line}-${end_line} ${target_file} - overlaps with ${lines_claimed[$index]}")
                break
            fi
            lines_claimed[$index]="$target_file"
        done

        if [ ${#errors[@]} = 0 -a $extract_only -eq 0 ]; then
            if [ $last_line_used -lt $((start_line-1)) ]; then
                for index in $(seq $last_line_used $((start_line-2))); do
                    output+=("${original[$index]}")
                done
            fi

            if [ "$fourth_param" = "-" ] && [[ "$fifth_param" =~ ^[0-9]+$ ]]; then
                output+=("@include- $fifth_param $target_file")
            elif [ "$fourth_param" = "-" ]; then
                output+=("@include-   $target_file")
            elif [[ "$fourth_param" =~ ^[0-9]+$ ]]; then
                output+=("@include  $fourth_param $target_file")
            else
                output+=("@include    $target_file")
            fi

            [ "$fourth_param" = "-" ] \
                && last_line_used=$end_line \
                || last_line_used=$((end_line + 1))
        fi
    done

    if [ ${#errors[@]} -gt 0 ]; then
        printf '%s\n' "${errors[@]}" >&2
        exit 1
    fi

    for line in "${commands[@]}"; do
        read -r start_line end_line target_file fourth_param fifth_param <<< "$line"

        [[ "$start_line" =~ ^@ ]] \
            && continue
        [[ -n "$match_pattern" && ! "$target_file" =~ $match_pattern ]] \
            && continue

        target_path="$source_dir/$target_file"
        mkdir -p "$(dirname "$target_path")"
        sed -n "${start_line},${end_line}p" "$source_file" > "$target_path"

        [ $quiet -eq 1 ] \
            && continue

        if [[ ! -t 1 ]]; then
            echo "$start_line-$end_line > $target_file"
        else
            printf '%-118s\r' "$start_line-$end_line > $target_file"
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
}

function usage {
    abort "breakdown.sh [-e] [-m pattern] [-q] file.md [breakdown.txt]" "Usage"
}

function abort {
    echo "${2:-Error}: $1" >&2
    exit 1
}

main "$@"
