#!/usr/bin/env -S bash -euo pipefail

function main {
    [ $# -lt 1 -o $# -gt 2 ] \
        && usage

    local input_file="$1"
    local compare_to="${2:-}"
    local processed

    [ ! -f "$input_file" ] \
        && abort "'$input_file' not found"

    if [ -n "$compare_to" ]; then
        [ ! -f "$compare_to" ] \
            && abort "'$compare_to' not found"

        if processed=$(process_includes "$input_file"); then
            diff -u "$compare_to" <(echo "$processed") \
                | tail -n +3
        else
            exit 1
        fi
    else
        process_includes "$input_file"
    fi
}

function adjust_header_depth {
    local file="$1"
    local adjustment="${2:-1}"

    while IFS= read -r line; do
        if [[ $line =~ ^(#+)(.*)$ ]]; then
            local rest=""
            local new_depth_count=$((${#BASH_REMATCH[1]} + adjustment))

            [ $new_depth_count -lt 1 ] \
                && new_depth_count=1
            echo "$(printf '%*s' "$new_depth_count" | tr ' ' '#')${BASH_REMATCH[2]}"
        else
            echo "$line"
        fi
    done < "$file"
}

function process_includes {
    local file="$1"
    local adjustment="${2:-0}"

    while IFS= read -r line; do
        if [[ $line =~ ^@adjust[[:space:]]+(-?[0-9]+)$ ]]; then
            adjustment="${BASH_REMATCH[1]}"
        elif [[ $line =~ ^@include(-)?[[:space:]]+((-?[0-9]+)[[:space:]]+)?([0-9]+-[0-9]+[[:space:]]+)?(.+)$ ]]; then
            local suppress_newline="${BASH_REMATCH[1]:-}"
            local include_adjustment="${BASH_REMATCH[3]}"
            local line_range="${BASH_REMATCH[4]% }"
            local include="${BASH_REMATCH[5]}"
            local full_path="$(dirname "$file")/$include"

            include_adjustment="${include_adjustment:-$adjustment}"

            [ ! -f "$full_path" ] && \
                abort "'$file' includes '$include': not found"

            if [ -n "$line_range" ]; then
                local start_line="${line_range%-*}"
                local end_line="${line_range#*-}"
                local file_dir="$(dirname "$full_path")"
                local temp_file="$file_dir/.rebuild_tmp_$$_$RANDOM"

                sed -n "${start_line},${end_line}p" "$full_path" > "$temp_file"

                if [ $include_adjustment -ne 0 ]; then
                    adjust_header_depth "$temp_file" "$include_adjustment" > "${temp_file}.adj"
                    mv "${temp_file}.adj" "$temp_file"
                fi

                process_includes "$temp_file" "$include_adjustment"
                rm -f "$temp_file"
            else
                if [ $include_adjustment -ne 0 ]; then
                    adjust_header_depth "$full_path" "$include_adjustment" \
                        | process_includes /dev/stdin "$include_adjustment"
                else
                    process_includes "$full_path" "$include_adjustment"
                fi
            fi

            [ -n "$suppress_newline" ] \
                || echo
        else
            echo "$line"
        fi
    done < "$file"
}


function usage {
    abort "rebuild.sh <markdown_with_includes> [comparison_file]" "Usage"
}

function abort {
    echo "${2:-Error}: $1" >&2
    exit 1
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
