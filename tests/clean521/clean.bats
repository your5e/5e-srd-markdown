#!/usr/bin/env bats

setup() {
    cp tests/clean521/srd.md "$BATS_TEST_TMPDIR/"
    cp tests/clean521/breakdown.txt "$BATS_TEST_TMPDIR/"
}


@test "processes clean D&D 521 SRD content without errors" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: #### Arid Land, 15: table immediately after header
        Warning: #### Polar Land, 24: table immediately after header
        Warning: #### Temperate Land, 33: table immediately after header
        Warning: #### Tropical Land, 42: table immediately after header
        EOF
    )

    run python clean_srd.py \
            --profile 521 \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"

    diff -u tests/clean521/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean521/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "clean can be run twice with no extraneous changes" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: #### Arid Land, 15: table immediately after header
        Warning: #### Polar Land, 24: table immediately after header
        Warning: #### Temperate Land, 33: table immediately after header
        Warning: #### Tropical Land, 42: table immediately after header
        EOF
    )

    run python clean_srd.py \
            --profile 521 \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean521/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean521/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    # run again, nothing should change
    run python clean_srd.py \
            --profile 521 \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean521/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean521/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}
