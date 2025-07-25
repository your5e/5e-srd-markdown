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
    diff -u <(echo "$output") <(echo "$expected_output")
    [ "$status" -eq 1 ]
}

@test "processes clean SRD content without errors" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: The Barbarian, 19: possible table run-on error
        EOF
    )

    run python clean_srd.py "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$output") <(echo "$expected_output")
    [ "$status" -eq 0 ]

    diff -u "$BATS_TEST_TMPDIR/srd.md" tests/clean/expected/srd.md
    diff -u "$BATS_TEST_TMPDIR/breakdown.txt" tests/clean/expected/breakdown.txt
}
