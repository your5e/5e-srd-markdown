#!/usr/bin/env bats

@test "without enough arguments" {
    run ./compare.sh
    diff -u <(echo "$output") <(echo "Usage: ./compare.sh <markdown_with_includes> <comparison>")
    [ "$status" -eq 1 ]

    run ./compare.sh nonexistent.md
    diff -u <(echo "$output") <(echo "Usage: ./compare.sh <markdown_with_includes> <comparison>")
    [ "$status" -eq 1 ]
}

@test "nonexistent input files" {
    run ./compare.sh \
        nonexistent.md \
        immaterial
    diff -u <(echo "$output") <(echo "Error: 'nonexistent.md' not found")
    [ "$status" -eq 1 ]

    run ./compare.sh \
        tests/breakdown/expected/replaced.md \
        nonexistent.md
    diff -u <(echo "$output") <(echo "Error: 'nonexistent.md' not found")
    [ "$status" -eq 1 ]
}

@test "identical files" {
    run ./compare.sh \
        tests/breakdown/expected/section_one.md \
        tests/compare/expected/section_one.md
    diff -u <(echo "$output") <(echo "")
    [ "$status" -eq 0 ]
}

@test "includes processed" {
    run ./compare.sh \
        tests/compare/input.md \
        tests/compare/source.md
    diff -u <(echo "$output") <(echo "")
    [ "$status" -eq 0 ]
}

@test "nested includes processed" {
    run ./compare.sh \
        tests/compare/nested.md \
        tests/compare/source.md
    diff -u <(echo "$output") <(echo "")
    [ "$status" -eq 0 ]
}

@test "missing includes" {
    run ./compare.sh \
        tests/compare/missing.md \
        tests/compare/source.md
    diff -u <(echo "$output") <(echo "Error: 'tests/compare/missing.md' includes 'nonexistent.md': not found")
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

    run ./compare.sh \
        tests/compare/input_broken.md \
        tests/compare/source.md
    diff -u <(echo "$output") <(echo "$expected_output")
    [ "$status" -eq 1 ]
}
