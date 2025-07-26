#!/usr/bin/env -S bash -euo pipefail

if [ $# -ne 3 ]; then
    echo "Usage: $0 <breakdown> <pattern> <increment>" >&2
    exit 1
fi

breakdown="$1"
pattern="$2"
increment="$3"

if [ ! -f "$breakdown" ]; then
    echo "Error: Control file '$breakdown' not found" >&2
    exit 1
fi

# only one match allowed
match_count=$(grep -c "$pattern" "$breakdown" || true)
if [ "$match_count" -ne 1 ]; then
    echo "Error: Pattern '$pattern' matches $match_count lines:" >&2
    grep -n "$pattern" "$breakdown" >&2
    exit 1
fi

temp_file=$(mktemp)

awk -v pattern="$pattern" -v increment="$increment" '
        function reindent(inc_first, inc_second) {
            match($0, /^[ \t]*/)
            indent = substr($0, RSTART, RLENGTH)

            first_end = index($0, $1) + length($1)
            second_start = index($0, $2)
            space1 = substr($0, first_end, second_start - first_end)

            space2 = ""
            rest = ""
            if (NF >= 3) {
                second_end = second_start + length($2)
                third_start = index($0, $3)
                space2 = substr($0, second_end, third_start - second_end)
                rest = substr($0, third_start)
            }

            print indent ($1 + inc_first) space1 ($2 + inc_second) space2 rest
        }

        {
            if (match($0, pattern)) {
                if (NF >= 2 && $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/) {
                    reindent(0, increment)  # increment only second column
                } else {
                    print $0
                }
                found = 1
                next
            }
            if (found && NF >= 2 && $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/) {
                reindent(increment, increment)  # increment both columns
            } else {
                print $0
            }
        }
    ' "$breakdown" > "$temp_file"

mv "$temp_file" "$breakdown"
