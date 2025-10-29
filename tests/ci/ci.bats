#!/usr/bin/env bats

@test "check 5.1 cleaning" {
    run python clean_srd.py \
        --warn \
        --ignore-warnings dnd/51/ignore_warnings.txt \
        --clean-lines dnd/51/clean_lines.txt \
            dnd/51/SRD_CC_v5.1.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "check rebuild" {
    run ./rebuild.sh dnd/51/breakdown.md dnd/51/SRD_CC_v5.1.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "check for 5.1 vault changes" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        == Conditions/Conditions.md
        About the vault.md: no longer in source directory
        Magic Items/List of Magic Items by A-Z.md: no longer in source directory
        Magic Items/List of Magic Items by Rarity.md: no longer in source directory
        Monsters/List of Animals by A-Z.md: no longer in source directory
        Monsters/List of NPCs by A-Z.md: no longer in source directory
        Spells/List of Spells by A-Z.md: no longer in source directory
        Spells/List of Spells by Level.md: no longer in source directory
        System Reference Document v5.1.md: no longer in source directory
        EOF
    )

    run make vault-dnd51
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    # clean up any patches
    git restore dnd/51/markdown
}

@test "check 5.2.1 cleaning" {
    run python clean_srd.py \
        --warn \
        --ignore-warnings dnd/521/ignore_warnings.txt \
            dnd/521/SRD_CC_v5.2.1.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "check 5.2.1 rebuild" {
    run ./rebuild.sh dnd/521/breakdown.md dnd/521/SRD_CC_v5.2.1.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "check for 5.2.1 vault changes" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        About the vault.md: no longer in source directory
        Magic Items/List of Magic Items by A-Z.md: no longer in source directory
        Magic Items/List of Magic Items by Rarity.md: no longer in source directory
        Monsters/List of Animals by A-Z.md: no longer in source directory
        Monsters/List of Monsters by A-Z.md: no longer in source directory
        Spells/List of Spells by A-Z.md: no longer in source directory
        Spells/List of Spells by Level.md: no longer in source directory
        System Reference Document v5.2.1.md: no longer in source directory
        EOF
    )


    run make vault-dnd521
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    # clean up any patches
    git restore dnd/521/obsidian_vault
}

@test "zero files changed" {
    status_output=$(git status --porcelain)
    diff_output=$(git diff)

    combined_output="$status_output"
    if [ -n "$status_output" ]; then
        combined_output="$status_output

Diff:
$diff_output"
    fi

    diff -u <(echo "") <(echo "$combined_output")
}
