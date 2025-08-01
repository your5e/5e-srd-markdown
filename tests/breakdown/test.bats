#!/usr/bin/env bats

setup() {
    export TEST_DIR="tests/breakdown"

    cp "$TEST_DIR/source.md" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/breakdown.txt" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/breakdown_invalid.txt" "$BATS_TEST_TMPDIR/"
}

@test "script with no arguments should show usage" {
    run ./breakdown.sh
    diff -u <(echo "Usage: breakdown.sh [-e] [-m pattern] [-q] file.md [breakdown.txt]") <(echo "$output")
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
        14-20 > sections/section_two.md
        23-27 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
    [ "$status" -eq 0 ]
}

@test "extract sections with default command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        14-20 > sections/section_two.md
        23-27 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
    [ "$status" -eq 0 ]
}

@test "extract and replace sections" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        14-20 > sections/section_two.md
        23-27 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh "$BATS_TEST_TMPDIR/source.md"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/expected/replaced.md "$BATS_TEST_TMPDIR/source.md"
    [ "$status" -eq 0 ]
}

@test "invalid ranges" {
    expected=$(sed -e 's/^        //' <<'        EOF'
        8-10 sections/section_overlap.md - overlaps with sections/section_one.md
        11-11 sections/section_overlap.md - duplicate filename
        21-10 reversed.md - descending line numbers
        20-20 sections/line_twenty.md - not in numerical order
        400-500 out_of_range.md - lines beyond the source
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown_invalid.txt"
    diff -u <(echo "$expected") <(echo "$output")

    diff -q $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
    [ ! -d "$BATS_TEST_TMPDIR/sections" ]
    [ "$status" -eq 1 ]
}

@test "extract only matching files with pattern" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        23-27 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e -m "(one|three)" "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ ! -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
    [ "$status" -eq 0 ]
}
