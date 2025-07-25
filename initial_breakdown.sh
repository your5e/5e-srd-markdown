#!/usr/bin/env -S bash -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: initial_breakdown.sh <markdown_file>" >&2
    exit 1
fi

markdown_file="$1"
last_start=1
last_section='__false__'
index=1

while IFS= read -r line; do
    if [[ "$line" =~ ^# ]]; then

        # this will probably tun out to be
        # D&D 5.1 SRD specific handling

        # "## **Bard**"             a genuine header
        # "#### **Speed** 30 ft."   mischaracterisation
        # "#### **Actions**"        another, and way too common

        if [[ "$line" =~ \*\*([^*]+)\*\*[[:space:]]*$ ]]; then
            bold_text="${BASH_REMATCH[1]}"

            if [[ "$bold_text" == "Actions" ]]; then
                ((index++))
                continue
            fi

            slug=$(
                echo "$bold_text" \
                    | sed "s/'//g" \
                    | tr 'A-Z' 'a-z' \
                    | sed \
                        -e 's/[^a-z0-9]/_/g' \
                        -e 's/__*/_/g' \
                        -e 's/_$//' \
                        -e 's/^_//'
            )

            printf '%8d %5d  %s\n' "$last_start" "$((index-2))" "$last_section"
            last_start=$index
            last_section="markdown/${slug}.md"
        fi
    fi
    ((index++))
done < "$markdown_file"

printf '%8d %5d  %s\n' "$last_start" "$index" "$last_section"
