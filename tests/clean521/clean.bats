#!/usr/bin/env bats

setup() {
    cp tests/clean521/srd.md "$BATS_TEST_TMPDIR/"
    cp tests/clean521/breakdown.txt "$BATS_TEST_TMPDIR/"
}


@test "processes clean D&D 521 SRD content without errors" {
    run python clean_srd.py \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"

    diff -u tests/clean521/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean521/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}
