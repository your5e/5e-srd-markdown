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
    expected_output=$(sed -e 's/^        //' <<"        EOF"

        breakdown.sh [-a] [-c] [-e] [-f] [-h] [-m pattern] [-q] [-s] file.md [breakdown.txt]
        EOF
    )

    run ./breakdown.sh
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "error when source file doesn't exist" {
    expected_output=$(sed -e 's/^        //' <<-EOF
        Error: Source file '${BATS_TEST_TMPDIR}/nonexistent.md' not found

        breakdown.sh [-a] [-c] [-e] [-f] [-h] [-m pattern] [-q] [-s] file.md [breakdown.txt]
	EOF
    )

    run ./breakdown.sh "$BATS_TEST_TMPDIR/nonexistent.md" "$BATS_TEST_TMPDIR/test_commands.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "error when command file doesn't exist" {
    expected_output=$(sed -e 's/^        //' <<-EOF
        Error: Command file '${BATS_TEST_TMPDIR}/nonexistent_commands.txt' not found

        breakdown.sh [-a] [-c] [-e] [-f] [-h] [-m pattern] [-q] [-s] file.md [breakdown.txt]
	EOF
    )

    run ./breakdown.sh "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/nonexistent_commands.txt"
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "extract sections with explicit command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
         5-11 >  sections/section_one.md
        14-20 >  sections/section_two.md
        23-27 >  sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e -f -c "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
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

@test "extract sections with default flags and explicit command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
         5-11 >  sections/section_one.md
        14-20 >  sections/section_two.md
        23-27 >  sections/section_three.md
              #  sections/section_one.md
              #  sections/section_two.md
              #  sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/fixed_section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/fixed_section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/fixed_section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
    [ "$status" -eq 0 ]
}

@test "extract sections with default command file" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
         5-11 >  sections/section_one.md
        14-20 >  sections/section_two.md
        23-27 >  sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e -f -c "$BATS_TEST_TMPDIR/source.md"
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

@test "extract sections with default flags" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
         5-11 >  sections/section_one.md
        14-20 >  sections/section_two.md
        23-27 >  sections/section_three.md
              #  sections/section_one.md
              #  sections/section_two.md
              #  sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e "$BATS_TEST_TMPDIR/source.md"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/fixed_section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/fixed_section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/fixed_section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/source.md "$BATS_TEST_TMPDIR/source.md"
    [ "$status" -eq 0 ]
}

@test "extract and replace sections" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
         5-11 >  sections/section_one.md
        14-20 >  sections/section_two.md
        23-27 >  sections/section_three.md
        EOF
    )

    run ./breakdown.sh -f -c "$BATS_TEST_TMPDIR/source.md"
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

@test "extract and replace sections with default flags" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
         5-11 >  sections/section_one.md
        14-20 >  sections/section_two.md
        23-27 >  sections/section_three.md
              #  sections/section_one.md
              #  sections/section_two.md
              #  sections/section_three.md
        EOF
    )

    run ./breakdown.sh "$BATS_TEST_TMPDIR/source.md"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/fixed_section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/fixed_section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u $TEST_DIR/expected/fixed_section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    diff -u $TEST_DIR/expected/fixed_replaced.md "$BATS_TEST_TMPDIR/source.md"
    [ "$status" -eq 0 ]
}

@test "invalid ranges" {
    expected=$(sed -e 's/^        //' <<'        EOF'
        1-3  - missing action
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
         5-11 >  sections/section_one.md
        23-27 >  sections/section_three.md
              #  sections/section_one.md
              #  sections/section_three.md
        EOF
    )

    run ./breakdown.sh -e -m "(one|three)" "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    [ -f "$BATS_TEST_TMPDIR/sections/section_one.md" ]
    [ ! -f "$BATS_TEST_TMPDIR/sections/section_two.md" ]
    [ -f "$BATS_TEST_TMPDIR/sections/section_three.md" ]

    diff -u $TEST_DIR/expected/fixed_section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u $TEST_DIR/expected/fixed_section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
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

@test "treat files as identical when only headers change" {
    rsync -a --times tests/breakdown/altered/ "$BATS_TEST_TMPDIR/sections/"

    run ./breakdown.sh "$BATS_TEST_TMPDIR/source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "") <(echo "$output")

    diff -u tests/breakdown/altered/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u tests/breakdown/altered/section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u tests/breakdown/altered/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    [ "$status" -eq 0 ]
}

@test "fix header indentation on updated files" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        14-20 >  sections/section_two.md
              #  sections/section_two.md
        EOF
    )

    rsync -a --times tests/breakdown/altered/ "$BATS_TEST_TMPDIR/sections/"

    run ./breakdown.sh "$BATS_TEST_TMPDIR/altered_source.md" "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    diff -u tests/breakdown/altered/section_one.md "$BATS_TEST_TMPDIR/sections/section_one.md"
    diff -u tests/breakdown/expected/altered_section_two.md "$BATS_TEST_TMPDIR/sections/section_two.md"
    diff -u tests/breakdown/altered/section_three.md "$BATS_TEST_TMPDIR/sections/section_three.md"
    [ "$status" -eq 0 ]
}

@test "append sections to existing files" {
    cp "$TEST_DIR/append_source.md" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/append_breakdown.txt" "$BATS_TEST_TMPDIR/"

    expected_output=$(sed -e 's/^        //' <<'        EOF'
         4-4  >  sections/combined.md
         9-9  >> sections/combined.md
        14-14 >> sections/combined.md
        EOF
    )

    run ./breakdown.sh -f -c "$BATS_TEST_TMPDIR/append_source.md" "$BATS_TEST_TMPDIR/append_breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    diff -u tests/breakdown/expected/combined.md "$BATS_TEST_TMPDIR/sections/combined.md"
    diff -u tests/breakdown/expected/append_modified_source.md "$BATS_TEST_TMPDIR/append_source.md"
    [ "$status" -eq 0 ]
}

@test "append sections with default flags warns" {
    cp "$TEST_DIR/append_source.md" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/append_breakdown.txt" "$BATS_TEST_TMPDIR/"

    expected_output=$(sed -e 's/^        //' <<-EOF
         4-4  >  sections/combined.md
         9-9  >> sections/combined.md
        14-14 >> sections/combined.md
        Warning: ${BATS_TEST_TMPDIR}/sections/combined.md, 1: first line must be a header
        Warning: ${BATS_TEST_TMPDIR}/sections/combined.md, 1: doesn't start with level 1 header
              #  sections/combined.md
	EOF
    )

    run ./breakdown.sh "$BATS_TEST_TMPDIR/append_source.md" "$BATS_TEST_TMPDIR/append_breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    diff -u tests/breakdown/expected/combined.md "$BATS_TEST_TMPDIR/sections/combined.md"
    diff -u tests/breakdown/expected/append_modified_source.md "$BATS_TEST_TMPDIR/append_source.md"
    [ "$status" -eq 0 ]
}

@test "append sections with headers should fix headers only once" {
    cp "$TEST_DIR/append_headers_source.md" "$BATS_TEST_TMPDIR/"
    cp "$TEST_DIR/append_headers_breakdown.txt" "$BATS_TEST_TMPDIR/"

    expected_output=$(sed -e 's/^        //' <<'        EOF'
         4-9  >  sections/headers_combined.md
        13-17 >> sections/headers_combined.md
              #  sections/headers_combined.md
        EOF
    )

    run ./breakdown.sh -c "$BATS_TEST_TMPDIR/append_headers_source.md" "$BATS_TEST_TMPDIR/append_headers_breakdown.txt"
    diff -u <(echo "$expected_output") <(echo "$output")

    diff -u tests/breakdown/expected/headers_combined.md "$BATS_TEST_TMPDIR/sections/headers_combined.md"
    [ "$status" -eq 0 ]
}

