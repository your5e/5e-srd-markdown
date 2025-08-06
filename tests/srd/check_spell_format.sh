#!/usr/bin/env -S bash -euo pipefail

function main {
    local exit_code=0

    find "$1" -name "*.md" -type f | while read -r file; do
        metadata="$(sed -n '5,8p' "$file")"
        for item in 'Casting Time' 'Range' 'Components' 'Duration'; do
            if ! grep -q "^- \*\*$item:\*\*" <(echo "$metadata"); then
                echo "$file: missing $item"
                exit_code=1
            fi
        done

        current_dir=$(dirname "$file" | sed "s|.*/spells/||")
        spell_level=$(extract_spell_level "$file")

        if [[ -n "$spell_level" && "$current_dir" != "$spell_level" ]]; then
            echo "$file: '$spell_level' doesn't match directory"
            exit_code=1
        fi
    done

    exit $exit_code
}

function extract_spell_level {
    local file="$1"

    # "_1st-level abjuration (ritual)_"
    local level_line=$(sed -n '3p' "$file")

    if [[ "$level_line" =~ _.*cantrip.* ]]; then
        echo "cantrip"
    elif [[ "$level_line" =~ _([0-9]+)(st|nd|rd|th)-level ]]; then
        echo "${BASH_REMATCH[1]}${BASH_REMATCH[2]}_level"
    else
        echo "unknown_level"
    fi
}

main "$@"
