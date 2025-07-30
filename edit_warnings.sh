#!/usr/bin/env -S bash -euo pipefail

function main {
    markdown="$1"

    while IFS= read -r line; do
        if [[ "$line" =~ Warning:.*,\ ([0-9]+): ]]; then
            line_number="${BASH_REMATCH[1]}"

            echo "$line"
            subl --wait "$markdown:$line_number"
        fi
    done
}

main "$@"
