#!/usr/bin/env bats

UNAME="$(uname)"

function timestamp {
    local file="$1"
    if [ "$UNAME" = 'Darwin' ]; then
        stat -f %m "$file"
    else
        stat -c %Y "$file"
    fi
}


setup() {
    export TEST_DIR="tests/breakdown"

    cp "$TEST_DIR/source.md" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/altered_source.md" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/breakdown.txt" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/breakdown_invalid.txt" "$BATS_TEST_TMPDIR/"
}

@test "script with no arguments should show usage" {
    run ./breakdown.sh
    diff -u <(echo "Usage: breakdown.sh [-e] [-i] [-m pattern] [-q] file.md [breakdown.txt]") <(echo "$output")
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

@test "identical content is not written" {
    current_time=$(date +%s)
    rsync -a --times "$TEST_DIR/expected/" "$BATS_TEST_TMPDIR/sections/"

    timestamp_one=$(timestamp "$BATS_TEST_TMPDIR/sections/section_one.md")
    timestamp_two=$(timestamp "$BATS_TEST_TMPDIR/sections/section_two.md")
    timestamp_three=$(timestamp "$BATS_TEST_TMPDIR/sections/section_three.md")
    sleep 1

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "") <(echo "$output")

    # timestamps shouldn't change because identical content should skip updates
    [ "$timestamp_one" -eq "$(timestamp "$BATS_TEST_TMPDIR/sections/section_one.md")" ]
    [ "$timestamp_two" -eq "$(timestamp "$BATS_TEST_TMPDIR/sections/section_two.md")" ]
    [ "$timestamp_three" -eq "$(timestamp "$BATS_TEST_TMPDIR/sections/section_three.md")" ]

    [ "$status" -eq 0 ]
}

@test "-i treats files as identical when only headers change" {
    rsync -a --times tests/breakdown/altered/ "$BATS_TEST_TMPDIR/sections/"

    run ./breakdown.sh -i "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "") <(echo "$output")

    diff -u tests/breakdown/altered/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u tests/breakdown/altered/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u tests/breakdown/altered/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    [ "$status" -eq 0 ]
}

@test "-i fixes header indentation on updated files" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        14-20 > sections/section_two.md
        EOF
    )

    rsync -a --times tests/breakdown/altered/ "$BATS_TEST_TMPDIR/sections/"

    run ./breakdown.sh -i "$BATS_TEST_TMPDIR/altered_source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    diff -u tests/breakdown/altered/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u tests/breakdown/expected/altered_section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u tests/breakdown/altered/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    [ "$status" -eq 0 ]
}
