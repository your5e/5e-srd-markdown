#!/usr/bin/env bats

setup() {
    cp tests/clean/srd.md "$BATS_TEST_TMPDIR/"
    cp tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/"
    cp tests/clean/clean.txt "$BATS_TEST_TMPDIR/"
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
            --clean-lines "$BATS_TEST_TMPDIR/clean.txt" \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "clean can be run twice with no extraneous changes" {
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
            --clean-lines "$BATS_TEST_TMPDIR/clean.txt" \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    # run again, nothing should change
    run python clean_srd.py \
            --clean-lines "$BATS_TEST_TMPDIR/clean.txt" \
            "$BATS_TEST_TMPDIR/srd.md" \
            "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/clean/expected/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "warn flag doesn't modify source file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # **The Barbarian**, 15: table immediately after header
        Warning: # **The Barbarian**, 15: table has empty header cells
        Warning: # **The Barbarian**, 30: possible table run-on
        Warning: # **The Barbarian**, 30: table has empty header cells
        Warning: ## **Equipment**, 71: em-dash not surrounded by spaces
        Warning: ## **Equipment**, 71: table has empty header cells
        Warning: ## **Equipment**, 84: table has empty data cells
        Warning: ## **Equipment**, 86: possible table run-on
        Warning: #### **Black Pudding**, 135: unusual Unicode characters: U+2212
        Warning: #### **Black Pudding**, 135: table has empty data cells
        Warning: #### **Black Pudding**, 150: unusual Unicode characters: U+2212
        Warning: #### **Actions**, 160: unusual Unicode characters: U+2212
        Warning: #### **Giant Centipede**, 206: table has empty header cells
        Warning: #### **Giant Centipede**, 208: table has empty data cells
        Warning: #### **Hyena**, 230: table has empty header cells
        Warning: #### **Hyena**, 232: unusual Unicode characters: U+2212
        Warning: #### **Hyena**, 232: table has empty data cells
        Warning: ## **Wereboar**, 252: table has empty header cells
        Warning: ## **Wereboar**, 254: unusual Unicode characters: U+2212
        Warning: ## **Wereboar**, 254: table has empty data cells
        Warning: ##### Arctic, 296: table immediately after header
        EOF
    )

    run python clean_srd.py --warn "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/clean/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    [ "$status" -eq 0 ]
}

@test "detects various formatting warnings" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # List style changes, 6: inconsistent list formatting (emphasis type mismatch)
        Warning: # Table run-on, 18: possible table run-on
        Warning: # Table run-on, 18: table has empty header cells
        Warning: # Mid-paragraph italic, 30: possible mistaken mid-paragraph italic: 'Ram, Portable.'
        Warning: # Mid-paragraph italic, 33: possible mistaken mid-paragraph italic: 'Claw. Melee Weapon Attack:'
        Warning: # Unusual unicode, 40: unusual Unicode characters: U+2212
        Warning: # Unusual unicode, 42: unusual Unicode characters: U+2075
        Warning: #### d100 Communication, 50: table immediately after header
        EOF
    )

    run python clean_srd.py --warn tests/clean/warnings.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "ignores warnings when ignore file is present" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # Table run-on, 18: table has empty header cells
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
