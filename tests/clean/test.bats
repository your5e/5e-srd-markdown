#!/usr/bin/env bats

setup() {
    cp tests/clean/srd.md "$BATS_TEST_TMPDIR/"
    cp tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/"
}

@test "detects errors and quits" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        ## **Black Tentacles**, 6:
        Duration value has more than 5 words, likely contains description: '**Duration:** Concentration, up to 1 minute Squirming, ebony tentacles fill a 20-foot square on ground that you can see within range. For the'
        EOF
    )

    run python clean_srd.py tests/clean/errors.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "no source, abort" {
    run python clean_srd.py nonexistent.md
    [ "$status" -eq 1 ]
    diff -u <(echo "Error 'nonexistent.md' not found") <(echo "$output")
    diff -u tests/clean/srd.md "$BATS_TEST_TMPDIR/srd.md"
}

@test "no breakdown file, abort" {
    run python clean_srd.py tests/clean/errors.md nonexistent.txt
    [ "$status" -eq 1 ]
    diff -u <(echo "Error 'nonexistent.txt' not found") <(echo "$output")
    diff -u tests/clean/srd.md "$BATS_TEST_TMPDIR/srd.md"
}


@test "no warnings file, abort" {
    run python clean_srd.py --warn --ignore-warnings nonexistent_ignore.txt tests/clean/warnings.md
    [ "$status" -eq 1 ]
    diff -u <(echo "Error 'nonexistent_ignore.txt' not found") <(echo "$output")
}

@test "processes clean SRD content without errors" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # The Barbarian, 12: table immediately after header
        Warning: # The Barbarian, 27: possible table run-on
        Warning: #### Traits, 249: possible mistaken mid-paragraph italic: 'Charge (Boar or Hybrid Form Only).'
        EOF
    )

    run python clean_srd.py "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    [ "$status" -eq 0 ]

    diff -u tests/clean/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
}

@test "clean can be run twice with no extraneous changes" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # The Barbarian, 12: table immediately after header
        Warning: # The Barbarian, 27: possible table run-on
        Warning: #### Traits, 249: possible mistaken mid-paragraph italic: 'Charge (Boar or Hybrid Form Only).'
        EOF
    )

    run python clean_srd.py "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    [ "$status" -eq 0 ]

    diff -u tests/clean/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    # run again, nothing should change
    run python clean_srd.py "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    [ "$status" -eq 0 ]

    diff -u tests/clean/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
}

@test "warn flag doesn't modify source file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # **The Barbarian**, 15: table immediately after header
        Warning: # **The Barbarian**, 30: possible table run-on
        Warning: ## **Equipment**, 86: possible table run-on
        Warning: #### **Black Pudding**, 135: unusual Unicode characters: U+2212
        Warning: #### **Black Pudding**, 149: unusual Unicode characters: U+2212
        Warning: #### **Actions**, 159: unusual Unicode characters: U+2212
        Warning: #### **Hyena**, 231: unusual Unicode characters: U+2212
        Warning: ## **Wereboar**, 253: unusual Unicode characters: U+2212
        EOF
    )

    run python clean_srd.py --warn "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    # Source file should remain unchanged from original
    diff -u tests/clean/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
}

@test "detects various formatting warnings" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # List style changes, 6: inconsistent list formatting (emphasis type mismatch)
        Warning: # Table run-on, 18: possible table run-on
        Warning: # Mid-paragraph italic, 30: possible mistaken mid-paragraph italic: 'Ram, Portable.'
        Warning: # Mid-paragraph italic, 33: possible mistaken mid-paragraph italic: 'Claw. Melee Weapon Attack:'
        Warning: # Unusual unicode, 40: unusual Unicode characters: U+2212
        Warning: # Unusual unicode, 42: unusual Unicode characters: U+2075
        Warning: #### d100 Communication, 50: table immediately after header
        EOF
    )

    run python clean_srd.py --warn tests/clean/warnings.md
    [ "$status" -eq 0 ]
    diff -u <(echo "$expected_output") <(echo "$output")
}

@test "ignores warnings when ignore file is present" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # Mid-paragraph italic, 30: possible mistaken mid-paragraph italic: 'Ram, Portable.'
        Warning: #### d100 Communication, 50: table immediately after header
        EOF
    )

    run python clean_srd.py \
        --warn \
        --ignore-warnings tests/clean/ignored.txt \
            tests/clean/warnings.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}
