#!/usr/bin/env -S bash -euo pipefail

function main {
    if [ $# -eq 0 ]; then
        echo "Usage: fix_statblock_headers.sh file|dir [file|dir ...]" >&2
        exit 1
    fi

    local exit_code=0

    for arg in "$@"; do
        files=$(find "${arg%/}" -name "*.md" -type f | sort)

        while read -r file; do
            if ! process_file "$file"; then
                exit_code=1
            fi
        done <<< "$files"
    done

    exit $exit_code
}

function process_file {
    local file="$1"
    local content=""
    local index=0
    local warnings=0

    while IFS= read -r line; do
        index=$((index + 1))

        if [[ "$line" =~ ^#+[[:space:]] ]]; then
            local header_level=$(( $(echo "$line" | grep -o '^#*' | wc -c) - 1 ))
            local header_text=$(echo "$line" | sed 's/^#* *//')

            if [ $index -eq 1 ]; then
                content+="# $header_text"$'\n'
            elif [[ "$header_text" =~ ^(Traits|Actions|Reactions|Legendary Actions)$ ]]; then
                content+="## $header_text"$'\n'
            else
                echo "Warning: $file, $index: check header '$header_text'"
                ((warnings++))
            fi
        else
            if [ $index -eq 1 ]; then
                echo "Warning: $file, $index: first line must be a header"
                ((warnings++))
            fi
            content+="$line"$'\n'
        fi
    done < "$file"

    [ $warnings -gt 0 ] \
        && return 1

    echo -n "$content" > "$file"
}

main "$@"
