#!/usr/bin/env -S bash -euo pipefail

source lib/fix_headers.sh


function main {
    if [ $# -eq 0 ]; then
        echo "Usage: fix_headers.sh file|dir [file|dir ...]" >&2
        exit 1
    fi

    local exit_code=0

    for arg in "$@"; do
        files=$(find "${arg%/}" -name "*.md" -type f | sort)

        while read -r file; do
            if ! fix_headers "$file"; then
                exit_code=1
            fi
        done <<< "$files"
    done

    exit $exit_code
}

main "$@"
