#!/usr/bin/env -S bash -euo pipefail

function main {
    local markdown="${1:-}"

    while IFS= read -r line; do
        local line_number=""

        echo "$line"

        if [[ "$line" =~ ^Warning:\ (.+\.md),\ ([0-9]+): ]]; then
            # fix_headers warning format
            markdown="${BASH_REMATCH[1]}"
            line_number="${BASH_REMATCH[2]}"
        elif [[ "$line" =~ Warning:.*,\ ([0-9]+): ]]; then
            # clean_srd warning format
            line_number="${BASH_REMATCH[1]}"
        fi

        if [ -z "$markdown" ]; then
            echo "Error: markdown file argument required for clean_srd warnings" >&2
            exit 1
        fi

        if [ -z "$line_number" ]; then
            echo "Warning: line number not found" >&2
            subl --wait "$markdown"
        else
            subl --wait "$markdown:$line_number"
        fi
    done
}

main "$@"
