#!/usr/bin/env bats

setup() {
    mkdir -p "$BATS_TEST_TMPDIR/vault"
    cp -r "tests/vault/input" "$BATS_TEST_TMPDIR/source"
    cp "tests/vault/expected/removed.md" "$BATS_TEST_TMPDIR/vault/"
}

teardown() {
    rm -rf "$BATS_TEST_TMPDIR/vault" "$BATS_TEST_TMPDIR/source"
}

@test "filter tests pass" {
    run python -m pytest tests/vault/processors
    [ "$status" -eq 0 ]
}

@test "update_vault.py converts files" {
    skip "FIXME: the 5.1 SRD needs to be updated to use proper filenames"

    expected_output=$(sed -e 's/^        //' <<'        EOF'
        removed.md: no longer in source directory
        EOF
    )

    run python update_vault.py \
        --profile dnd51 \
        --ignore $BATS_TEST_TMPDIR/source/ignore.txt \
            "$BATS_TEST_TMPDIR/source" \
            "$BATS_TEST_TMPDIR/vault"

    diff -u <(echo "$expected_output") <(echo "$output")
    [ -f "$BATS_TEST_TMPDIR/vault/removed.md" ]

    while IFS= read -r -d '' original; do
        filename=$(basename "$original")

        # correctly updated
        diff -u "tests/vault/expected/$filename" "$BATS_TEST_TMPDIR/vault/$filename"

        # didn't modify original source
        diff -u "$original" "$BATS_TEST_TMPDIR/source/$filename"
    done < <(find tests/vault/input -name "*.md" -print0)

    [ "$status" -eq 0 ]
}
