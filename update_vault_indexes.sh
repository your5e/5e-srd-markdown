#!/usr/bin/env -S bash -euo pipefail

function main {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <version>" >&2
        exit 1
    fi

    local version="$1"
    local vault_dir="$version/obsidian_vault"
    local markdown_dir="$version/markdown"

    if [ ! -d "$vault_dir" ]; then
        echo "Error: '$vault_dir' not found" >&2
        exit 1
    fi

    list_spells "$markdown_dir/Spells" > "$vault_dir/Spells/List of Spells by A-Z.md"
    list_spells_by_level "$markdown_dir/Spells" > "$vault_dir/Spells/List of Spells by Level.md"
    list_magic_items "$markdown_dir/Magic Items" > "$vault_dir/Magic Items/List of Magic Items by A-Z.md"
    list_magic_items_by_rarity "$markdown_dir/Magic Items" > "$vault_dir/Magic Items/List of Magic Items by Rarity.md"

    if [ "$version" = "dnd/51" ]; then
        list_animals "$markdown_dir/Monsters" > "$vault_dir/Monsters/List of Animals by A-Z.md"
        list_npcs "$markdown_dir/Monsters" > "$vault_dir/Monsters/List of NPCs by A-Z.md"
    else
        list_monsters "$markdown_dir/Monsters" > "$vault_dir/Monsters/List of Monsters by A-Z.md"
        list_animals "$markdown_dir/Monsters" > "$vault_dir/Monsters/List of Animals by A-Z.md"
    fi
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
    for level in "Cantrip" "1st Level" "2nd Level" "3rd Level" "4th Level" "5th Level" "6th Level" "7th Level" "8th Level" "9th Level"; do
        level_dir="$dir/$level"

        if [ ! -d "$level_dir" ]; then
            level="${level/st Level/Level }"
            level="${level/nd Level/Level }"
            level="${level/rd Level/Level }"
            level="${level/th Level/Level }"
            level_dir="$dir/$level"

            if [ ! -d "$level_dir" ]; then
                continue
            fi
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
    local breakdown="${version}/breakdown.md"

    echo "# Animals A-Z"

    current_letter=""

    if [ -f "$breakdown" ] && grep -q "^# Appendix MM-A: Miscellaneous Creatures" "$breakdown"; then
        sed -n '/^# Appendix MM-A: Miscellaneous Creatures/,/^# Appendix MM-B: Nonplayer Characters/p' "$breakdown" | \
            grep '@include' | \
            sed -E 's/.*".*\/([^/]+)\.md"/\1/' | \
            sort
    else
        find "$dir" -name "*.md" -type f | while read -r file; do
            if grep -q "^_.*Beast" "$file"; then
                basename "$file" .md
            fi
        done | sort
    fi | while read -r animal; do
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

function list_npcs {
    local dir="$1"
    local breakdown="${version}/breakdown.md"

    echo "# NPCs A-Z"

    current_letter=""

    sed -n '/^# Appendix MM-B: Nonplayer Characters/,$p' "$breakdown" | \
        grep '@include' | \
        sed -E 's/.*".*\/([^/]+)\.md"/\1/' | \
        sort | while read -r npc; do
        first_letter="${npc:0:1}"
        first_letter_upper="${first_letter^^}"

        if [ "$first_letter_upper" != "$current_letter" ]; then
            current_letter="$first_letter_upper"
            echo ""
            echo "## $current_letter"
            echo ""
        fi

        echo "- [[$npc]]"
    done
}

main "$@"
