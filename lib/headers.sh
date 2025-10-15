#!/usr/bin/env bash

function check_header_progression {
    local file="$1"
    local line_num=0
    local prev_level=0
    local error_messages=()

    while IFS= read -r line; do
        ((line_num++))

        if [[ "$line_num" -eq 1 ]]; then
            [[ ! "$line" =~ ^#[[:space:]][^[:space:]] ]] && break
            prev_level=1
            continue
        fi

        [[ ! "$line" =~ ^#+.* ]] && continue

        local level=0
        while [[ "${line:$level:1}" == "#" ]]; do
            ((level++))
        done

        if [[ "$line" =~ ^#+[[:space:]]*$ ]]; then
            error_messages+=("Warning: $file, $line_num: no text in header")
            continue
        fi

        if [[ ! "$line" =~ ^#+[[:space:]][^[:space:]] ]]; then
            error_messages+=("Warning: $file, $line_num: invalid spacing in header")
        else
            [[ $level -eq 1 ]] && \
                error_messages+=("Warning: $file, $line_num: multiple level 1 headers")
            [[ $level -gt $((prev_level + 1)) ]] && \
                error_messages+=("Warning: $file, $line_num: expected level $((prev_level + 1)) header")
            prev_level="$level"
        fi
    done < "$file"

    if [[ "$prev_level" -eq 0 ]]; then
        echo "Warning: $file, 1: doesn't start with level 1 header"
        return 1
    fi

    if [[ ${#error_messages[@]} -gt 0 ]]; then
        printf '%s\n' "${error_messages[@]}"
        return 1
    fi

    return 0
}

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

function fix_statblock_headers {
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
            elif [[ "$header_text" =~ ^(Traits|Actions|Bonus Actions|Reactions|Legendary Actions)$ ]]; then
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
