#!/usr/bin/env -S bash -euo pipefail

function main {
    local dir="${SRD_DIR:-}"
    local increment=""

    while getopts "d:" opt; do
        case $opt in
            d)  dir="$OPTARG" ;;
            *)  usage ;;
        esac
    done
    shift $((OPTIND - 1))

    local pattern="${1:-}"
    local increment="${2:-}"
    [ -z "$pattern" -o -z "$increment" ] && usage

    [ -z "$dir" ] && error "Error: No directory specified and SRD_DIR environment variable not set"
    [ ! -d "$dir" ] && error "Error: Directory '$dir' not found"

    local breakdown="$dir/breakdown.txt"
    [ ! -f "$breakdown" ] && error "Error: '$breakdown' not found"

    local ignore_warnings="$dir/ignore_warnings.txt"
    [ ! -f "$ignore_warnings" ] && error "Error: '$ignore_warnings' not found"

    # must be exactly one match in breakdown file
    local match_count=$(grep -c "$pattern" "$breakdown" || true)
    if [ "$match_count" -ne 1 ]; then
        echo "Error: Pattern '$pattern' matches $match_count lines in breakdown.txt:" >&2
        grep -n "$pattern" "$breakdown" >&2
        exit 1
    fi

    alter_breakdown_file "$breakdown" "$pattern" "$increment"
    alter_ignore_warnings_file "$breakdown" "$ignore_warnings" "$pattern" "$increment"
}

function alter_breakdown_file {
    local breakdown="$1"
    local pattern="$2"
    local increment="$3"

    local result=$(
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
                    found = 1
                }

                if (NF >= 2 && $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/) {
                    if (match($0, pattern)) {
                        reindent(0, increment)          # increment second column
                        next
                    } else if (found) {
                        reindent(increment, increment)  # increment both
                        next
                    }
                }

                print $0
            }
        ' "$breakdown"
    )
    echo "$result" > "$breakdown"
}

function alter_ignore_warnings_file {
    local breakdown="$1"
    local ignore_warnings="$2"
    local pattern="$3"
    local increment="$4"

    local pattern_line_num=$(grep "$pattern" "$breakdown" | awk '{print $1}')
    local result=$(
        awk -v increment="$increment" -v threshold="$pattern_line_num" '
            {
                # find "[...], 125: [...]"
                if (match($0, /, [0-9]+:/)) {
                    line_num = int(substr($0, RSTART+2, RLENGTH-3))
                    if (line_num >= threshold) {
                        new_line_num = line_num + increment
                        gsub(/, [0-9]+:/, ", " new_line_num ":")
                    }
                }
                print $0
            }
        ' "$ignore_warnings"
    )
    echo "$result" > "$ignore_warnings"
}

function usage {
    error "Usage: alter_lines.sh [-d <dir>] <pattern> <increment>"
}

function error {
    echo "$1" 2>&1
    exit 1
}

main "$@"
