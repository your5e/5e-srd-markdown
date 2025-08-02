#!/usr/bin/env -S bash -euo pipefail

function main {
    local markdown="${1:-}"

    while IFS= read -r line; do
        local markdown=""
        local line_number=""

        if [[ "$line" =~ ^Warning:\ (.+\.md),\ ([0-9]+): ]]; then
            # fix_headers warning format
            markdown="${BASH_REMATCH[1]}"
            line_number="${BASH_REMATCH[2]}"
        elif [[ "$line" =~ Warning:.*,\ ([0-9]+): ]]; then
            # clean_srd warning format
            line_number="${BASH_REMATCH[1]}"
        fi

        [[ -n "$markdown" && -n "$line_number" ]] \
            && subl --wait "$markdown:$line_number"
    done
}

main "$@"
