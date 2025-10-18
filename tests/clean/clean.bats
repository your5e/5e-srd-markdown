#!/usr/bin/env bats

setup() {
    cp tests/clean/srd.md "$BATS_TEST_TMPDIR/"
    cp tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/"
}

@test "filter tests pass" {
    run python -m pytest tests/clean/filters
    [ "$status" -eq 0 ]
}

@test "no source, abort" {
    run python clean_srd.py nonexistent.md
    [ "$status" -eq 1 ]
    diff -u <(echo "Error 'nonexistent.md' not found") <(echo "$output")
}

@test "no breakdown file, abort" {
    run python clean_srd.py tests/clean/errors.md nonexistent.txt
    [ "$status" -eq 1 ]
    diff -u <(echo "Error 'nonexistent.txt' not found") <(echo "$output")
}


@test "no warnings file, abort" {
    run python clean_srd.py --warn --ignore-warnings nonexistent_ignore.txt tests/clean/warnings.md
    [ "$status" -eq 1 ]
    diff -u <(echo "Error 'nonexistent_ignore.txt' not found") <(echo "$output")
}

@test "warn flag doesn't modify source file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Warning: # **The Barbarian**, 3: table immediately after header
        Warning: # **The Barbarian**, 3: table has empty header cells
        Warning: # **The Barbarian**, 18: possible table run-on
        Warning: # **The Barbarian**, 18: table has empty header cells
        EOF
    )

    run python clean_srd.py --warn "$BATS_TEST_TMPDIR/srd.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/clean/srd.md "$BATS_TEST_TMPDIR/srd.md"
    diff -u tests/clean/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
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
