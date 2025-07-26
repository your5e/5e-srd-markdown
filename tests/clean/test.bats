#!/usr/bin/env bats

setup() {
    cp tests/clean/srd.md "$BATS_TEST_TMPDIR/"
    cp tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/"
}

@test "detects errors and quits" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Black Tentacles, 6:
        Duration value has more than 5 words, likely contains description: '**Duration:** Concentration, up to 1 minute Squirming, ebony tentacles fill a 20-foot square on ground that you can see within range. For the'
        EOF
    )

    run python clean_srd.py tests/clean/errors.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "processes clean SRD content without errors" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: The Barbarian, 18: possible table run-on
        EOF
    )

    run python clean_srd.py "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    diff -u tests/clean/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
}

@test "warn flag doesn't modify source file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: The Barbarian, 18: possible table run-on
        EOF
    )

    run python clean_srd.py --warn "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    # Source file should remain unchanged from original
    diff -u tests/clean/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
}
