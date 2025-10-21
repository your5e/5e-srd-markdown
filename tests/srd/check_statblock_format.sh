#!/usr/bin/env -S bash -euo pipefail

exit_code=0
edit_mode=0
problems=0

function should_ignore_error {
    local error_header="$1"
    local error_content="${2:-}"
    local full_error="${error_header}"$'\n'"${error_content}"
    local filename=$(basename "$file")

    [[ "$ignore_content" =~ (^|$'\n')"$filename"($'\n'|$) ]] && return 0
    [[ "$ignore_content" == *"$full_error"* ]] && return 0

    return 1
}

function report_error {
    local error_type="$1"
    local error_content="$2"
    local error_msg="$file: $error_type"
    
    if ! should_ignore_error "$error_msg" "$error_content"; then
        echo "$error_msg"
        if [ -n "$error_content" ]; then
            echo "$error_content"
        fi
        echo ''
        exit_code=1
        problems=1
    fi
}

function main {
    if [ "$1" = '-e' ]; then
        edit_mode=1
        shift
    fi

    ignore_file="${1%/}/ignore_statblock_errors.txt"
    ignore_content=""
    if [ -f "$ignore_file" ]; then
        ignore_content=$(cat "$ignore_file")
    fi

    for arg in "$@"; do
        files=$(find "${arg%/}" -name "*.md" -type f | sort)

        while read -r file; do
            problems=0

            [[ "$ignore_content" =~ (^|$'\n')"$(basename "$file")"($'\n'|$) ]] \
                && continue

            metadata="$(sed -n '5,8p' "$file")"

            # Check for either 5.1 format (Armor Class/Hit Points/Speed) or 5.2.1 format (AC/HP/Speed)
            has_ac=0
            has_hp=0
            has_speed=0

            grep -q "^- \*\*\(Armor Class\|AC\)\*\*" <(echo "$metadata") && has_ac=1
            grep -q "^- \*\*\(Hit Points\|HP\)\*\*" <(echo "$metadata") && has_hp=1
            grep -q "^- \*\*Speed\*\*" <(echo "$metadata") && has_speed=1

            [ $has_ac -eq 0 ] && report_error "missing Armor Class" ""
            [ $has_hp -eq 0 ] && report_error "missing Hit Points" ""
            [ $has_speed -eq 0 ] && report_error "missing Speed" ""

            ability_scores="$(sed -n '9,14p' "$file")"
            ability_table_lines=$(grep '^|' <(echo "$ability_scores") | wc -l)
            [ $ability_table_lines -ne 3 -a $ability_table_lines -ne 5 ] \
                && report_error "missing ability scores" ""

            grep -q "^- \*\*\(Challenge\|CR\)\*\*" "$file" || report_error "missing CR" ""

            unusual="$(grep "^\\\\\\*" "$file" || true)"
            [ -n "$unusual" ] \
                && report_error "unusual formatting" "$unusual"

            no_traits=$(sed -n '/^##* Traits$/{N;N;/^##* Traits\n\n##* Actions$/p;}' "$file")
            [ -n "$no_traits" ] && report_error "empty traits section" ""

            unexpected_headers=$(
                tail -n +2 "$file" \
                    | grep "^##* " \
                    | grep -vE "^##* (Traits|Actions|Bonus Actions|Reactions|Legendary Actions)$"
            ) || true
            [ -n "$unexpected_headers" ] && report_error "unexpected headers" "$unexpected_headers"

            underscore_lines=$(grep "^_[^*].*[^_]_\.$" "$file" || true)
            [ -n "$underscore_lines" ] && report_error "underscore formatting" "$underscore_lines"

            # Only check bare paras for 5.1 format (uses "Armor Class")
            if grep -q "^- \*\*Armor Class\*\*" "$file"; then
                bare_paras=$(
                    grep "^[A-Za-z0-9]" "$file" \
                        | grep -v 'can take.*legendary actions'
                ) || true
                [ -n "$bare_paras" ] && report_error "bare paras" "$bare_paras"
            fi

            bold_start=$(grep "^\*\*" "$file" || true)
            [ -n "$bold_start" ] && report_error "bold start" "$bold_start"

            # Check for unindented spell lists (should be indented under spellcasting trait)
            unindented_spells=$(grep "^- [0-9]/day\|^- At will:\|^- [0-9][a-z]* level\|^- Cantrips" "$file" || true)
            [ -n "$unindented_spells" ] && report_error "unindented spell list" "$unindented_spells"


            if [ $problems -eq 1 -a $edit_mode -eq 1 ]; then
                open -a Marked\ 2 "$file"
                ${SRD_MARKDOWN_EDITOR:-${VISUAL:-${EDITOR:-vim}}} "$file"
                echo ''
            fi
        done <<< "$files"
    done
}

main "$@"
exit $exit_code
