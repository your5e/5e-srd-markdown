#!/usr/bin/env bats

setup() {
    export TEST_DIR="tests/breakdown"
    export TEMP_DIR="$(mktemp -d)"

    cp "$TEST_DIR/source.md" "$TEMP_DIR/"
    cp "$TEST_DIR/breakdown.txt" "$TEMP_DIR/"
    cp "$TEST_DIR/breakdown_invalid.txt" "$TEMP_DIR/"
}

teardown() {
    rm -rf "$TEMP_DIR"
}

@test "script with no arguments should show usage" {
    run ./breakdown.sh
    diff -u <(echo "$output") <(echo "Usage: breakdown.sh [-e] file.md [breakdown.txt]")
    [ "$status" -eq 1 ]
}

@test "error when source file doesn't exist" {
    run ./breakdown.sh "$TEMP_DIR/nonexistent.md" "$TEMP_DIR/test_commands.txt"
    diff -u <(echo "$output") <(echo "Error: Source file '$TEMP_DIR/nonexistent.md' not found")
    [ "$status" -eq 1 ]
}

@test "error when command file doesn't exist" {
    run ./breakdown.sh "$TEMP_DIR/source.md" "$TEMP_DIR/nonexistent_commands.txt"
    diff -u <(echo "$output") <(echo "Error: Command file '$TEMP_DIR/nonexistent_commands.txt' not found")
    [ "$status" -eq 1 ]
}

@test "extract sections with explicit command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        13-19 > sections/section_two.md
        21-25 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$TEMP_DIR/source.md" "$TEMP_DIR/breakdown.txt"
    diff -u <(echo "$output") <(echo "$expected_output")
    [ "$status" -eq 0 ]

    [ -f "$TEMP_DIR/sections/section_one.md" ]
    [ -f "$TEMP_DIR/sections/section_two.md" ]
    [ -f "$TEMP_DIR/sections/section_three.md" ]

    diff -u "$TEMP_DIR/sections/section_one.md" $TEST_DIR/expected/section_one.md
    diff -u "$TEMP_DIR/sections/section_two.md" $TEST_DIR/expected/section_two.md
    diff -u "$TEMP_DIR/sections/section_three.md" $TEST_DIR/expected/section_three.md
    diff -u "$TEMP_DIR/source.md" $TEST_DIR/source.md
}

@test "extract sections with default command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        13-19 > sections/section_two.md
        21-25 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$TEMP_DIR/source.md"
    diff -u <(echo "$output") <(echo "$expected_output")
    [ "$status" -eq 0 ]

    [ -f "$TEMP_DIR/sections/section_one.md" ]
    [ -f "$TEMP_DIR/sections/section_two.md" ]
    [ -f "$TEMP_DIR/sections/section_three.md" ]

    diff -u "$TEMP_DIR/sections/section_one.md" $TEST_DIR/expected/section_one.md
    diff -u "$TEMP_DIR/sections/section_two.md" $TEST_DIR/expected/section_two.md
    diff -u "$TEMP_DIR/sections/section_three.md" $TEST_DIR/expected/section_three.md
    diff -u "$TEMP_DIR/source.md" $TEST_DIR/source.md
}

@test "extract and replace sections" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        5-11 > sections/section_one.md
        13-19 > sections/section_two.md
        21-25 > sections/section_three.md
        EOF
    )

    run ./breakdown.sh "$TEMP_DIR/source.md"
    diff -u <(echo "$output") <(echo "$expected_output")
    [ "$status" -eq 0 ]

    [ -f "$TEMP_DIR/sections/section_one.md" ]
    [ -f "$TEMP_DIR/sections/section_two.md" ]
    [ -f "$TEMP_DIR/sections/section_three.md" ]

    diff -u "$TEMP_DIR/sections/section_one.md" $TEST_DIR/expected/section_one.md
    diff -u "$TEMP_DIR/sections/section_two.md" $TEST_DIR/expected/section_two.md
    diff -u "$TEMP_DIR/sections/section_three.md" $TEST_DIR/expected/section_three.md
    diff -u "$TEMP_DIR/source.md" $TEST_DIR/expected/replaced.md
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

    run ./breakdown.sh -e "$TEMP_DIR/source.md" "$TEMP_DIR/breakdown_invalid.txt"
    diff -u <(echo "$output") <(echo "$expected")
    [ "$status" -eq 1 ]

    diff -q "$TEMP_DIR/source.md" $TEST_DIR/source.md
    [ ! -d "$TEMP_DIR/sections" ]
}
