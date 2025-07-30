#!/usr/bin/env bats

@test "check rebuild" {
    run python clean_srd.py \
        --ignore-warnings dnd/51/ignore_warnings.txt \
            dnd/51/SRD_CC_v5.1.md \
            dnd/51/breakdown.txt
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]

    run cp dnd/51/SRD_CC_v5.1.md dnd/51/breakdown.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]

    run ./breakdown.sh -q dnd/51/breakdown.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]

    run ./compare.sh dnd/51/breakdown.md dnd/51/SRD_CC_v5.1.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]

    run git status --porcelain
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}
