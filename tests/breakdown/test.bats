#!/usr/bin/env bats

setup() {
    export TEST_DIR="tests/breakdown"

    cp "$TEST_DIR/source.md" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/breakdown.txt" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/breakdown_invalid.txt" "$BATS_TEST_TMPDIR/"
}

@test "script with no arguments should show usage" {
    run ./breakdown.sh
    diff -u <(echo "Usage: breakdown.sh [-e] [-m pattern] file.md [breakdown.txt]") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "error when source file doesn't exist" {
    run ./breakdown.sh "$BATS_TEST_TMPDIR/nonexistent.md" "$BATS_TEST_TMPDIR/test_commands.txt"
    diff -u <(echo "Error: Source file '$BATS_TEST_TMPDIR/nonexistent.md' not found") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "error when command file doesn't exist" {
    run ./breakdown.sh "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/nonexistent_commands.txt"
    diff -u <(echo "Error: Command file '$BATS_TEST_TMPDIR/nonexistent_commands.txt' not found") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "extract sections with explicit command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        13-19 > sections/section_two.md
        21-25 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
}

@test "extract sections with default command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        13-19 > sections/section_two.md
        21-25 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
}

@test "extract and replace sections" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        13-19 > sections/section_two.md
        21-25 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh "$BATS_TEST_TMPDIR/source.md"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/expected/replaced.md "$BATS_TEST_TMPDIR/source.md"
}

@test "invalid ranges" {
    expected=$(sed -e 's/^        //' <<'        EOF'
        9-15 sections/section_overlap.md overlaps with sections/section_one.md
        13-19 sections/section_two.md overlaps with sections/section_overlap.md
        20-20 sections/section_overlap.md duplicates 9-15
        21-10 reversed.md has descending line numbers
        400-500 out_of_range.md has lines larger than the source file
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown_invalid.txt"
    diff -u <(echo "$expected") <(echo "$output")
    [ "$status" -eq 1 ]

    diff -q $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
    [ ! -d "$BATS_TEST_TMPDIR/sections" ]
}

@test "extract only matching files with pattern" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        21-25 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e -m "(one|three)" "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 0 ]

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ ! -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
}
