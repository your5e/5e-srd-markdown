#!/usr/bin/env bats

setup() {
    cp tests/clean51/srd.md "$BATS_TEST_TMPDIR/"
    cp tests/clean51/cleaned.md "$BATS_TEST_TMPDIR/"
    cp tests/clean51/breakdown.txt "$BATS_TEST_TMPDIR/"
    cp tests/clean51/breakdown.cleaned.txt "$BATS_TEST_TMPDIR/"
    cp tests/clean51/clean.txt "$BATS_TEST_TMPDIR/"
}

@test "processes clean SRD content without errors" {
    skip "FIXME: the 5.1 SRD needs to be updated to use proper filenames"

    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # The Barbarian, 12: table immediately after header
        Warning: # The Barbarian, 12: table has empty header cells
        Warning: # The Barbarian, 27: possible table run-on
        Warning: # The Barbarian, 27: table has empty header cells
        Warning: ## Equipment, 71: em-dash not surrounded by spaces
        Warning: ## Equipment, 71: table has empty header cells
        Warning: #### Black Pudding, 128: table has empty data cells
        Warning: #### Traits, 249: possible mistaken mid-paragraph italic: 'Charge (Boar or Hybrid Form Only).'
        Warning: ##### Arctic, 275: table immediately after header
        EOF
    )

    run python clean_srd.py \
            --profile dnd51 \
            --clean-lines "$BATS_TEST_TMPDIR/clean.txt" \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean51/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean51/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "clean can be run twice with no extraneous changes" {
    skip "FIXME: the 5.1 SRD needs to be updated to use proper filenames"

    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # The Barbarian, 12: table immediately after header
        Warning: # The Barbarian, 12: table has empty header cells
        Warning: # The Barbarian, 27: possible table run-on
        Warning: # The Barbarian, 27: table has empty header cells
        Warning: ## Equipment, 71: em-dash not surrounded by spaces
        Warning: ## Equipment, 71: table has empty header cells
        Warning: #### Black Pudding, 128: table has empty data cells
        Warning: #### Traits, 249: possible mistaken mid-paragraph italic: 'Charge (Boar or Hybrid Form Only).'
        Warning: ##### Arctic, 275: table immediately after header
        EOF
    )

    run python clean_srd.py \
            --profile dnd51 \
            --clean-lines "$BATS_TEST_TMPDIR/clean.txt" \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean51/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean51/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    # run again, nothing should change
    run python clean_srd.py \
            --profile dnd51 \
            --clean-lines "$BATS_TEST_TMPDIR/clean.txt" \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean51/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean51/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "cleans already cleaned to new standard" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # The Barbarian, 15: table immediately after header
        Warning: # The Barbarian, 15: table has empty header cells
        Warning: # The Barbarian, 30: possible table run-on
        Warning: # The Barbarian, 30: table has empty header cells
        Warning: ## Equipment, 74: table has empty header cells
        Warning: #### Traits, 293: possible mistaken mid-paragraph italic: 'Charge (Boar or Hybrid Form Only).'
        Warning: ##### Arctic, 325: table immediately after header
        EOF
    )

    run python clean_srd.py \
            --profile dnd51 \
            "$BATS_TEST_TMPDIR/cleaned.md"
    diff -u tests/clean51/expected/v2.md "$BATS_TEST_TMPDIR/cleaned.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}
