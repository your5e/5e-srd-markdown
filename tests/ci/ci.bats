#!/usr/bin/env bats

@test "check 5.1 cleaning" {
    skip "FIXME: the 5.1 SRD cleaning is out of date"

    run python clean_srd.py \
        --warn \
        --ignore-warnings dnd/51/ignore_warnings.txt \
        --clean-lines dnd/51/clean_lines.txt \
            dnd/51/SRD_CC_v5.1.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "check rebuild" {
    skip "FIXME: the 5.1 SRD cleaning is out of date"

    run ./rebuild.sh dnd/51/breakdown.md dnd/51/SRD_CC_v5.1.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "check for 5.1 vault changes" {
    skip "FIXME: the 5.1 SRD needs to be updated to use proper filenames"

    run python update_vault.py \
            --ignore dnd/51/ignore_vault.txt \
                dnd/51/markdown \
                dnd/51/obsidian_vault
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
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
        Magic Items/List of Magic Items by A-Z.md: no longer in source directory
        Magic Items/List of Magic Items by Rarity.md: no longer in source directory
        Monsters/List of Animals by A-Z.md: no longer in source directory
        Monsters/List of Monsters by A-Z.md: no longer in source directory
        Spells/List of Spells by A-Z.md: no longer in source directory
        Spells/List of Spells by Level.md: no longer in source directory
        System Reference Document v5.2.1.md: no longer in source directory
        EOF
    )

    run python update_vault.py \
            --profile dnd521 \
                dnd/521/markdown \
                dnd/521/obsidian_vault
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "zero files changed" {
    run git status --porcelain
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}
