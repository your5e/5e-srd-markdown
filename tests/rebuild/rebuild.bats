#!/usr/bin/env bats

source ./rebuild.sh

@test "without enough arguments" {
    run ./rebuild.sh
    diff -u <(echo "Usage: rebuild.sh <markdown_with_includes> [comparison_file]") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "nonexistent input files" {
    run ./rebuild.sh nonexistent.md
    diff -u <(echo "Error: 'nonexistent.md' not found") <(echo "$output")
    [ "$status" -eq 1 ]

    run ./rebuild.sh nonexistent.md tests/breakdown/expected/replaced.md
    diff -u <(echo "Error: 'nonexistent.md' not found") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "identical files" {
    run ./rebuild.sh tests/rebuild/input_raw.md tests/rebuild/expected/output.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "includes processed" {
    run ./rebuild.sh tests/rebuild/input.md tests/rebuild/expected/output.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "nested includes processed" {
    run ./rebuild.sh tests/rebuild/nested.md tests/rebuild/expected/output.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "missing includes" {
    run ./rebuild.sh tests/rebuild/missing.md tests/rebuild/expected/output.md
    diff -u <(echo "Error: 'tests/rebuild/missing.md' includes 'nonexistent.md': not found") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "shows diff" {
    expected_output=$(sed -e 's/^        //' <<'        EOF'
        @@ -10,14 +10,6 @@
         Line 4 of section one.
         Line 5 of section one.
         
        -## Section Two
        -
        -This is the content of section two.
        -It also has multiple lines.
        -Line 3 of section two.
        -Line 4 of section two.
        -Line 5 of section two.
        -
         ## Section Three
         
         This is the content of section three.
        EOF
    )

    run ./rebuild.sh tests/rebuild/input_broken.md tests/rebuild/expected/output.md
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "adjust header depth" {
    run adjust_header_depth tests/rebuild/sections/section_one.md 1
    diff -u tests/rebuild/expected/section_one.md <(echo "$output")
    [ "$status" -eq 0 ]

    run adjust_header_depth tests/rebuild/sections/section_two.md 2
    diff -u tests/rebuild/expected/section_two.md <(echo "$output")
    [ "$status" -eq 0 ]

    run adjust_header_depth tests/rebuild/sections/section_three.md -1
    diff -u tests/rebuild/expected/section_three.md <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "includes processed with header adjustment" {
    run ./rebuild.sh tests/rebuild/input_adjust.md tests/rebuild/expected/output.md
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "output to stdout" {
    run ./rebuild.sh tests/rebuild/input.md
    # Should output the processed file content, not be empty
    [ "$status" -eq 0 ]
    [ -n "$output" ]
}

