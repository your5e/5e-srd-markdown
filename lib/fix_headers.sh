#!/usr/bin/env bash

function fix_headers {
    local file="$1"
    local content=""
    local index=0
    local warnings=0
    local offset=""
    local last_level=0

    while IFS= read -r line; do
        index=$((index+1))

        if [[ "$line" =~ ^#+[[:space:]] ]]; then
            local header_level=$(( $(echo "$line" | grep -o '^#*' | wc -c) - 1 ))
            local header_text=$(echo "$line" | sed 's/^#* *//')

            if [ -z "$offset" ]; then
                offset=$((header_level - 1))
                last_level=1
            fi

            local new_level=$((header_level - offset))

            if [ $new_level -lt 1 ]; then
                echo "Warning: $file, $index: header too low"
                ((warnings++))
            else
                local new_header=$(printf '%*s' "$new_level" | tr ' ' '#')
                content+="$new_header $header_text"$'\n'
                last_level=$new_level
            fi
        else
            if [ $index -eq 1 ]; then
                echo "Warning: $file, $index: first line must be a header"
                ((warnings++))
            fi
            content+="$line"$'\n'
        fi
    done < "$file"

    [ $warnings -gt 0 ] && return 1

    echo -n "$content" > "$file"
}
