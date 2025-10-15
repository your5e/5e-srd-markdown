#!/usr/bin/env bats

@test "no arguments shows usage" {
    run ./check_headers.sh
    diff -u <(echo "$output") <(echo "Usage: headers.sh [-e] file|directory [file|directory ...]")
    [ "$status" -eq 1 ]
}

@test "file not found" {
    run ./check_headers.sh nonexistent.md
    diff -u <(echo "$output") <(echo "nonexistent.md: file not found")
    [ "$status" -eq 1 ]
}

@test "valid file" {
    run ./check_headers.sh tests/headers/valid.md
    [ -z "$output" ]
    [ "$status" -eq 0 ]
}

@test "first line level 1 header" {
    run ./check_headers.sh tests/headers/sublevels.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "Warning: tests/headers/sublevels.md, 1: doesn't start with level 1 header")

    run ./check_headers.sh tests/headers/no_headers.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "Warning: tests/headers/no_headers.md, 1: doesn't start with level 1 header")

    run ./check_headers.sh tests/headers/empty.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "Warning: tests/headers/empty.md, 1: doesn't start with level 1 header")

    run ./check_headers.sh tests/headers/whitespace.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "Warning: tests/headers/whitespace.md, 1: doesn't start with level 1 header")

    run ./check_headers.sh tests/headers/preamble.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "Warning: tests/headers/preamble.md, 1: doesn't start with level 1 header")
}

@test "file with multiple level 1 headers" {
    run ./check_headers.sh tests/headers/multiple.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "Warning: tests/headers/multiple.md, 9: multiple level 1 headers")
}

@test "file with header jump" {
    run ./check_headers.sh tests/headers/jumps.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "Warning: tests/headers/jumps.md, 9: expected level 3 header")
}

@test "inconsistent spacing" {
    expected=$(sed -e 's/^        //' <<'        EOF'
        Warning: tests/headers/spacing.md, 5: invalid spacing in header
        Warning: tests/headers/spacing.md, 9: invalid spacing in header
        Warning: tests/headers/spacing.md, 13: invalid spacing in header
        Warning: tests/headers/spacing.md, 17: expected level 2 header
        Warning: tests/headers/spacing.md, 21: no text in header
        EOF
    )

    run ./check_headers.sh tests/headers/spacing.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "$expected")
}

@test "checks all inputs" {
    expected=$(sed -e 's/^        //' <<'        EOF'
        Warning: tests/headers/jumps.md, 9: expected level 3 header
        Warning: tests/headers/multiple.md, 9: multiple level 1 headers
        Warning: tests/headers/spacing.md, 5: invalid spacing in header
        Warning: tests/headers/spacing.md, 9: invalid spacing in header
        Warning: tests/headers/spacing.md, 13: invalid spacing in header
        Warning: tests/headers/spacing.md, 17: expected level 2 header
        Warning: tests/headers/spacing.md, 21: no text in header
        EOF
    )

    run ./check_headers.sh \
        tests/headers/jumps.md \
        tests/headers/multiple.md \
        tests/headers/spacing.md
    [ "$status" -eq 1 ]
    diff -u <(echo "$output") <(echo "$expected")
}

@test "directory traversal" {
    expected=$(sed -e 's/^        //' <<'        EOF'
        Warning: tests/headers/empty.md, 1: doesn't start with level 1 header
        Warning: tests/headers/jumps.md, 9: expected level 3 header
        Warning: tests/headers/multiple.md, 9: multiple level 1 headers
        Warning: tests/headers/no_headers.md, 1: doesn't start with level 1 header
        Warning: tests/headers/preamble.md, 1: doesn't start with level 1 header
        Warning: tests/headers/progression.md, 1: doesn't start with level 1 header
        Warning: tests/headers/regression.md, 1: doesn't start with level 1 header
        Warning: tests/headers/spacing.md, 13: invalid spacing in header
        Warning: tests/headers/spacing.md, 17: expected level 2 header
        Warning: tests/headers/spacing.md, 21: no text in header
        Warning: tests/headers/spacing.md, 5: invalid spacing in header
        Warning: tests/headers/spacing.md, 9: invalid spacing in header
        Warning: tests/headers/statblock.md, 1: doesn't start with level 1 header
        Warning: tests/headers/statblock_error.md, 1: doesn't start with level 1 header
        Warning: tests/headers/sublevels.md, 1: doesn't start with level 1 header
        Warning: tests/headers/whitespace.md, 1: doesn't start with level 1 header
        EOF
    )

    run ./check_headers.sh tests/headers/
    [ "$status" -eq 1 ]
    diff -u <(echo "$output" | sort) <(echo "$expected")
}
