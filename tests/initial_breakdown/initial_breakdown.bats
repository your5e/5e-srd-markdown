#!/usr/bin/env bats

@test "generates breakdown from markdown file" {
    run ./initial_breakdown.sh tests/initial_breakdown/srd.md
    diff -u tests/initial_breakdown/expected/breakdown.txt <(echo "$output")
    [ "$status" -eq 0 ]
}
