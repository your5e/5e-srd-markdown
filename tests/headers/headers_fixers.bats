#!/usr/bin/env bats

@test "statblock - must start with header" {
    cp tests/headers/no_headers.md "$BATS_TEST_TMPDIR"

    expected_output="Warning: ${BATS_TEST_TMPDIR}/no_headers.md, 1: first line must be a header"

    run ./fix_statblock_headers.sh "$BATS_TEST_TMPDIR/no_headers.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/headers/no_headers.md "$BATS_TEST_TMPDIR/no_headers.md"
    [ "$status" -eq 1 ]
}

@test "statblock - fix known headers" {
    cp tests/headers/statblock.md "$BATS_TEST_TMPDIR"

    run ./fix_statblock_headers.sh "$BATS_TEST_TMPDIR/statblock.md"
    diff -u <(echo '') <(echo "$output")
    diff -u tests/headers/expected/statblock.md "$BATS_TEST_TMPDIR/statblock.md"
    [ "$status" -eq 0 ]
}

@test "statblock - don't fix unknown headers" {
    cp tests/headers/statblock.md "$BATS_TEST_TMPDIR"
    cp tests/headers/statblock_error.md "$BATS_TEST_TMPDIR"

    expected_output="Warning: ${BATS_TEST_TMPDIR}/statblock_error.md, 35: check header 'Spellcasting'"

    run ./fix_statblock_headers.sh "$BATS_TEST_TMPDIR/statblock_error.md" "$BATS_TEST_TMPDIR/statblock.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/headers/statblock_error.md "$BATS_TEST_TMPDIR/statblock_error.md"
    diff -u tests/headers/expected/statblock.md "$BATS_TEST_TMPDIR/statblock.md"
    [ "$status" -eq 1 ]
}

@test "generic - fix headers that flow" {
    cp tests/headers/progression.md "$BATS_TEST_TMPDIR"

    run ./fix_headers.sh "$BATS_TEST_TMPDIR/progression.md"
    diff -u <(echo '') <(echo "$output")
    diff -u tests/headers/expected/progression.md "$BATS_TEST_TMPDIR/progression.md"
    [ "$status" -eq 0 ]
}

@test "generic - headers must progress" {
    expected_output="Warning: ${BATS_TEST_TMPDIR}/regression.md, 26: header too low"

    cp tests/headers/regression.md "$BATS_TEST_TMPDIR"

    run ./fix_headers.sh "$BATS_TEST_TMPDIR/regression.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/headers/regression.md "$BATS_TEST_TMPDIR/regression.md"
    [ "$status" -eq 1 ]
}

@test "generic - must start with header" {
    expected_output="Warning: ${BATS_TEST_TMPDIR}/no_headers.md, 1: first line must be a header"

    cp tests/headers/no_headers.md "$BATS_TEST_TMPDIR"

    run ./fix_headers.sh "$BATS_TEST_TMPDIR/no_headers.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/headers/no_headers.md "$BATS_TEST_TMPDIR/no_headers.md"
    [ "$status" -eq 1 ]
}

@test "generic - valid file no changes" {
    cp tests/headers/valid.md "$BATS_TEST_TMPDIR"

    run ./fix_headers.sh "$BATS_TEST_TMPDIR/valid.md"
    diff -u <(echo '') <(echo "$output")
    diff -u tests/headers/valid.md "$BATS_TEST_TMPDIR/valid.md"
    [ "$status" -eq 0 ]
}

@test "generic - jumps file unchanged" {
    cp tests/headers/jumps.md "$BATS_TEST_TMPDIR"

    run ./fix_headers.sh "$BATS_TEST_TMPDIR/jumps.md"
    diff -u <(echo '') <(echo "$output")
    diff -u tests/headers/jumps.md "$BATS_TEST_TMPDIR/jumps.md"
    [ "$status" -eq 0 ]
}

@test "generic - statblock file errors" {
    expected_output=$(sed -e 's/^        //' <<-EOF
        Warning: ${BATS_TEST_TMPDIR}/statblock.md, 28: header too low
        Warning: ${BATS_TEST_TMPDIR}/statblock.md, 36: header too low
		EOF
    )

    cp tests/headers/statblock.md "$BATS_TEST_TMPDIR"

    run ./fix_headers.sh "$BATS_TEST_TMPDIR/statblock.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/headers/statblock.md "$BATS_TEST_TMPDIR/statblock.md"
    [ "$status" -eq 1 ]
}
