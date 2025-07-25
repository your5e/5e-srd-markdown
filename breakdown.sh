#!/usr/bin/env -S bash -euo pipefail

function main {
    extract_only=false
    if [ "$#" -gt 0 ] && [ "$1" = "-e" ]; then
        extract_only=true
        shift
    fi

    [ "$#" -lt 1 ] && abort "breakdown.sh [-e] file.md [breakdown.txt]" "Usage"

    source_file="$1"
    source_dir=$(dirname "$source_file")
    [ ! -f "$source_file" ] && abort "Source file '$source_file' not found"

    command_file="${2:-$source_dir/breakdown.txt}"
    [ ! -f "$command_file" ] && abort "Command file '$command_file' not found"

    source_line_count=$(wc -l < "$source_file")

    declare -a ranges=()
    declare -a errors=()
    declare -a lines_claimed=()
    declare -A files_seen=()

    while IFS=' ' read -r start_line end_line target_file suppress; do
        if [ $start_line -gt $end_line ]; then
            errors+=("${start_line}-${end_line} ${target_file} has descending line numbers")
            continue
        fi

        if [ $end_line -gt $source_line_count ]; then
            errors+=("${start_line}-${end_line} ${target_file} has lines larger than the source file")
            continue
        fi

        if [ -n "${files_seen[$target_file]:-}" ]; then
            errors+=("${start_line}-${end_line} ${target_file} duplicates ${files_seen[$target_file]}")
            continue
        fi
        files_seen[$target_file]="${start_line}-${end_line}"

        for ((line_num=start_line; line_num<=end_line; line_num++)); do
            if [ -n "${lines_claimed[$line_num]:-}" ]; then
                errors+=("${start_line}-${end_line} ${target_file} overlaps with ${lines_claimed[$line_num]}")
                break
            fi
        done

        for ((line_num=start_line; line_num<=end_line; line_num++)); do
            lines_claimed[$line_num]="$target_file"
        done

        ranges+=("$start_line $end_line $target_file $suppress")
    done < <(
            # filters, then sorts the file based on start line number
            sed '/^[[:space:]]*#/d; /^[[:space:]]*$/d; s/#.*$//' "$command_file" \
                | sort -k1,1n
        )

    if [ ${#errors[@]} -gt 0 ]; then
        printf '%s\n' "${errors[@]}" >&2
        exit 1
    fi

    for range in "${ranges[@]}"; do
        read -r start_line end_line target_file suppress <<< "$range"

        target_path="$source_dir/$target_file"
        target_dir=$(dirname "$target_path")
        mkdir -p "$target_dir"

        sed -n "${start_line},${end_line}p" "$source_file" > "$target_path"
        echo "$start_line-$end_line > $target_file"
    done

    if [ "$extract_only" = false ]; then
        mapfile -t edited < "$source_file"

        for range in "${ranges[@]}"; do
            read -r start_line end_line target_file suppress <<< "$range"

            if [ -n "$suppress" ]; then
                edited[$((start_line-1))]="@include- $target_file"
            else
                edited[$((start_line-1))]="@include  $target_file"
            fi

            for ((line_num=start_line+1; line_num<=end_line; line_num++)); do
                unset edited[$((line_num-1))]
            done

            if [ -z "$suppress" -a -z "${edited[$end_line]:-}" ]; then
                # also remove trailing blank
                unset edited[$end_line]
            fi
        done

        printf '%s\n' "${edited[@]}" > "$source_file"
    fi
}

function abort {
    echo "${2:-Error}: $1" >&2
    exit 1
}

main "$@"
