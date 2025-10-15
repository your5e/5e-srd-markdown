#!/usr/bin/env -S bash -euo pipefail

function main {
    if [ $# -ne 1 ]; then
        echo "Usage: initial_breakdown.sh <markdown_file>" >&2
        exit 1
    fi

    markdown_file="$1"
    last_start=1
    last_section='__false__'
    last_bold_text='__false__'
    index=1

    while IFS= read -r line; do
        if [[ "$line" =~ ^# ]]; then
            header_text=$(extract_header_text "$line")

            if [[ -z "$header_text" ]]; then
                ((index++))
                continue
            fi

            if should_skip_header "$header_text"; then
                ((index++))
                continue
            fi

            # skip duplicate headers (5.2.1 has "aboleth -> aboleth")
            if [[ "$header_text" == "$last_bold_text" ]]; then
                last_start=$index
                ((index++))
                continue
            fi

            slug=$(
                echo "$header_text" \
                    | sed "s/'//g" \
                    | tr 'A-Z' 'a-z' \
                    | sed \
                        -e 's/[^a-z0-9]/_/g' \
                        -e 's/__*/_/g' \
                        -e 's/_$//' \
                        -e 's/^_//'
            )

            if [[ "$last_section" != "__false__" ]]; then
                output_section "$last_start" "$((index-2))" "$last_section"
            fi

            last_start=$index
            last_section="markdown/${slug}.md"
            last_bold_text="$header_text"
        fi
        ((index++))
    done < "$markdown_file"

    if [[ "$last_section" != "__false__" ]]; then
        output_section "$last_start" "$((index-1))" "$last_section"
    fi
}

function extract_header_text {
    local line="$1"

    if [[ "$line" =~ \*\*([^*]+)\*\*[[:space:]]*$ ]]; then
        echo "${BASH_REMATCH[1]}"
    elif [[ "$line" =~ \*\*([^*]+)\*\* ]]; then
        echo "${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^#+[[:space:]]*(.+)$ ]]; then
        echo "${BASH_REMATCH[1]}"
    fi
}

function should_skip_header {
    local header="$1"

    [[ "$header" =~ ^(Actions|Traits|Bonus Actions)$ ]] && return 0
    [[ "$header" =~ ^(Reactions|Legendary Actions)$ ]] && return 0
    [[ "$header" =~ ^(Vulnerabilities|Resistances)$ ]] && return 0
    [[ "$header" =~ ^(Immunities|Skills)$ ]] && return 0
    [[ "$header" =~ ^(AC|HP|Speed|Components|Duration) ]] && return 0
    [[ "$header" =~ [Ww]ondrous\ [Ii]tem ]] && return 0
    [[ "$header" =~ [Rr]equires\ [Aa]ttunement ]] && return 0

    local item_types="(Rod|Ring|Rope|Wand|Potion|Armor|Staff|Weapon|Scroll)"
    local rarities="(Uncommon|Common|Rare|Very Rare|Legendary|Rarity Varies)"
    [[ "$header" =~ $item_types.*$rarities ]] && return 0

    return 1
}

function output_section {
    local start=$1
    local end=$2
    local section=$3

    if [[ "$start" == "$end" ]]; then
        printf '# %6d %6d  %s\n' "$start" "$end" "$section"
    else
        printf '%6d %6d  %s\n' "$start" "$end" "$section"
    fi
}

main "$@"
