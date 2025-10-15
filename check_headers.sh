#!/usr/bin/env -S bash -euo pipefail

source lib/headers.sh

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

function usage {
    echo "Usage: headers.sh [-e] file|directory [file|directory ...]" >&2
    exit 1
}

main "$@"
