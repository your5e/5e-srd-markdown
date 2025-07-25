#!/usr/bin/env -S bash -euo pipefail

temp_file=$(mktemp)

function main {
    [ $# -ne 2 ] && \
        abort "./compare.sh <markdown_with_includes> <comparison>" Usage

    local input_file="$1"
    local input_dir=$(dirname "$input_file")
    local comparison="$2"

    [ ! -f "$input_file" ] && \
        abort "'$input_file' not found"
    [ ! -f "$comparison" ] && \
        abort "'$comparison' not found"

    trap 'cleanup' EXIT
    process_includes "$input_file" "$input_dir" > "$temp_file"
    diff -u "$comparison" "$temp_file" \
        | tail -n +3
}

function process_includes {
    local file="$1"
    local base_dir="$2"

    while IFS= read -r line; do
        if [[ $line =~ ^@include(-)?[[:space:]]+(.+)$ ]]; then
            local suppress_line="${BASH_REMATCH[1]:-}"
            local include_file="${BASH_REMATCH[2]}"
            local full_path="$base_dir/$include_file"

            [ ! -f "$full_path" ] && \
                abort "'$file' includes '$include_file': not found"

            process_includes "$full_path" "$(dirname "$full_path")"
            [ -n "$suppress_line" ] || echo
        else
            echo "$line"
        fi
    done < "$file"
}

function cleanup {
    rm -f "$temp_file"
}

function abort {
    echo "${2:-Error}: $1" >&2
    exit 1
}

main "$@"
