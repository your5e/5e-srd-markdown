#!/usr/bin/env bats

@test "check clean" {
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

@test "check for vault changes" {
    run python update_vault.py \
            --ignore dnd/51/ignore_vault.txt \
                dnd/51/markdown \
                dnd/51/obsidian_vault
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "zero files changed" {
    run git status --porcelain
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}
