#!/usr/bin/env -S bash -euo pipefail

function main {
    local version="${1:-521}"
    local vault_dir="dnd/$version/obsidian_vault"
    local markdown_dir="dnd/$version/markdown"

    if [ ! -d "$vault_dir" ]; then
        echo "Error: '$vault_dir' not found" >&2
        exit 1
    fi

    list_spells "$markdown_dir/Spells" > "$vault_dir/Spells/List of Spells by A-Z.md"
    list_spells_by_level "$markdown_dir/Spells" > "$vault_dir/Spells/List of Spells by Level.md"
    list_magic_items "$markdown_dir/Magic Items" > "$vault_dir/Magic Items/List of Magic Items by A-Z.md"
    list_magic_items_by_rarity "$markdown_dir/Magic Items" > "$vault_dir/Magic Items/List of Magic Items by Rarity.md"
    list_monsters "$markdown_dir/Monsters" > "$vault_dir/Monsters/List of Monsters by A-Z.md"
    list_animals "$markdown_dir/Monsters" > "$vault_dir/Monsters/List of Animals by A-Z.md"
}

function list_spells {
    local dir="$1"

    echo "# Spells A-Z"

    current_letter=""

    find "$dir" -name "*.md" -type f | while read -r file; do
        basename "$file" .md
    done | sort | while read -r spell; do
        first_letter="${spell:0:1}"
        first_letter_upper="${first_letter^^}"

        if [ "$first_letter_upper" != "$current_letter" ]; then
            current_letter="$first_letter_upper"
            echo ""
            echo "## $current_letter"
            echo ""
        fi

        echo "- [[$spell]]"
    done
}

function list_spells_by_level {
    local dir="$1"

    echo "# Spells by Level"
    echo ""

    # Sort spell levels in specific order
    for level in "Cantrip" "Level 1" "Level 2" "Level 3" "Level 4" "Level 5" "Level 6" "Level 7" "Level 8" "Level 9"; do
        level_dir="$dir/$level"

        if [ ! -d "$level_dir" ]; then
            continue
        fi

        # Print level header
        echo "## $level"
        echo ""

        # List spells in this level
        find "$level_dir" -name "*.md" -type f | while read -r file; do
            basename "$file" .md
        done | sort | sed 's/^/- [[/' | sed 's/$/]]/'

        echo ""
    done
}

function list_magic_items {
    local dir="$1"

    echo "# Magic Items A-Z"

    current_letter=""

    find "$dir" -mindepth 2 -name "*.md" -type f | while read -r file; do
        basename "$file" .md
    done | sort | while read -r item; do
        first_letter="${item:0:1}"
        first_letter_upper="${first_letter^^}"

        if [ "$first_letter_upper" != "$current_letter" ]; then
            current_letter="$first_letter_upper"
            echo ""
            echo "## $current_letter"
            echo ""
        fi

        echo "- [[$item]]"
    done
}

function list_magic_items_by_rarity {
    local dir="$1"

    echo "# Magic Items by Rarity"
    echo ""

    # Sort rarities in specific order
    for rarity in "Varies" "Common" "Uncommon" "Rare" "Very Rare" "Legendary" "Artifact"; do
        rarity_dir="$dir/$rarity"

        if [ ! -d "$rarity_dir" ]; then
            continue
        fi

        # Print rarity header
        echo "## $rarity"
        echo ""

        # List items in this rarity
        find "$rarity_dir" -name "*.md" -type f | while read -r file; do
            basename "$file" .md
        done | sort | sed 's/^/- [[/' | sed 's/$/]]/'

        echo ""
    done
}

function list_monsters {
    local dir="$1"

    echo "# Monsters A-Z"

    current_letter=""

    find "$dir" -name "*.md" -type f | while read -r file; do
        if ! grep -q "^_.*Beast" "$file"; then
            basename "$file" .md
        fi
    done | sort | while read -r monster; do
        first_letter="${monster:0:1}"
        first_letter_upper="${first_letter^^}"

        if [ "$first_letter_upper" != "$current_letter" ]; then
            current_letter="$first_letter_upper"
            echo ""
            echo "## $current_letter"
            echo ""
        fi

        echo "- [[$monster]]"
    done
}

function list_animals {
    local dir="$1"

    echo "# Animals A-Z"

    current_letter=""

    find "$dir" -name "*.md" -type f | while read -r file; do
        if grep -q "^_.*Beast" "$file"; then
            basename "$file" .md
        fi
    done | sort | while read -r animal; do
        first_letter="${animal:0:1}"
        first_letter_upper="${first_letter^^}"

        if [ "$first_letter_upper" != "$current_letter" ]; then
            current_letter="$first_letter_upper"
            echo ""
            echo "## $current_letter"
            echo ""
        fi

        echo "- [[$animal]]"
    done
}

main "$@"
