#!/usr/bin/env bats

setup() {
    export SRD_DIR="$BATS_TEST_TMPDIR"
    cp tests/alter/breakdown.txt "$BATS_TEST_TMPDIR/"
    cp tests/alter/ignore_warnings.txt "$BATS_TEST_TMPDIR/"
}

@test "script with no arguments should show usage" {
    run ./alter_lines.sh

    diff -u <(echo "Usage: alter_lines.sh [-d <dir>] <pattern> <increment>") <(echo "$output" | head -1)
    [ "$status" -eq 1 ]
}

@test "error when directory doesn't exist with -d flag" {
    run ./alter_lines.sh -d nonexistent_dir druid 5

    diff -u <(echo "Error: Directory 'nonexistent_dir' not found") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "error when no directory and SRD_DIR not set" {
    unset SRD_DIR

    run ./alter_lines.sh druid 5

    diff -u <(echo "Error: No directory specified and SRD_DIR environment variable not set") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "error when breakdown file doesn't exist in directory" {
    mkdir -p "$BATS_TEST_TMPDIR/empty_dir"

    run ./alter_lines.sh -d "$BATS_TEST_TMPDIR/empty_dir" druid 5

    diff -u <(echo "Error: '$BATS_TEST_TMPDIR/empty_dir/breakdown.txt' not found") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "error when ignore warnings file doesn't exist in directory" {
    mkdir -p "$BATS_TEST_TMPDIR/partial_dir"
    cp tests/alter/breakdown.txt "$BATS_TEST_TMPDIR/partial_dir/"

    run ./alter_lines.sh -d "$BATS_TEST_TMPDIR/partial_dir" druid 5

    diff -u <(echo "Error: '$BATS_TEST_TMPDIR/partial_dir/ignore_warnings.txt' not found") <(echo "$output")
    diff -u tests/alter/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/alter/ignore_warnings.txt "$BATS_TEST_TMPDIR/ignore_warnings.txt"
    [ "$status" -eq 1 ]
}

@test "error when pattern matches zero lines" {

    run ./alter_lines.sh nonexistent 5

    diff -u <(echo "Error: Pattern 'nonexistent' matches 0 lines in breakdown.txt:") <(echo "$output")
    diff -u tests/alter/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/alter/ignore_warnings.txt "$BATS_TEST_TMPDIR/ignore_warnings.txt"
    [ "$status" -eq 1 ]
}

@test "error when pattern matches multiple lines" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        Error: Pattern 'druid' matches 4 lines in breakdown.txt:
        19:   754   1000  markdown/classes/druid/druid.md
        89:  5273   5407  markdown/classes/druid/druid_spells.md
        189:  7520   7534  markdown/spells/cantrip/druidcraft.md
        1072: 23900  23929  markdown/statblocks/druid.md

        EOF
    )

    run ./alter_lines.sh druid 5

    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u tests/alter/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/alter/ignore_warnings.txt "$BATS_TEST_TMPDIR/ignore_warnings.txt"
    [ "$status" -eq 1 ]
}

@test "adjusts breakdown.txt and ignore_warnings.txt" {
    run ./alter_lines.sh bard_spells 2

    diff -u <(echo "") <(echo "$output")
    diff -u tests/alter/expected/breakdown.txt "$BATS_TEST_TMPDIR/breakdown.txt"
    diff -u tests/alter/expected/ignore_warnings.txt "$BATS_TEST_TMPDIR/ignore_warnings.txt"
    [ "$status" -eq 0 ]
}
