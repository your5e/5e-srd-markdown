#!/usr/bin/env -S bash -euo pipefail

function main {
    local edit_mode=0

    while getopts "e" option; do
        case "$option" in
            e)  edit_mode=1 ;;
            *)  usage ;;
        esac
    done
    shift $((OPTIND-1))

    [ $# -eq 0 ] \
        && usage

    local exit_code=0
    for arg in "$@"; do
        local files=()

        if [ -d "$arg" ]; then
            while IFS= read -r -d '' file; do
                files+=("$file")
            done < <(find "${arg%/}" -name "*.md" -type f -print0)
        elif [ -f "$arg" ]; then
            files+=("$arg")
        else
            echo "$arg: file not found"
            exit_code=1
        fi

        for file in "${files[@]}"; do
            if ! check_header_progression "$file"; then
                exit_code=1

                if [ $edit_mode -eq 1 ]; then
                    ${SRD_MARKDOWN_EDITOR:-${VISUAL:-${EDITOR:-vim}}} "$file"
                    echo ''
                fi
            fi
        done
    done

    exit $exit_code
}

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

function usage {
    echo "Usage: headers.sh [-e] file|directory [file|directory ...]" >&2
    exit 1
}

main "$@"
