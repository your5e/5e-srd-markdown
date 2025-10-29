#!/usr/bin/env bats

setup() {
    mkdir -p "$BATS_TEST_TMPDIR/vault"
    cp -r "tests/vault521/input" "$BATS_TEST_TMPDIR/source"
}

teardown() {
    rm -rf "$BATS_TEST_TMPDIR/vault" "$BATS_TEST_TMPDIR/source"
}

@test "update_vault.py converts files" {
    run python update_vault.py \
        --profile dnd521 \
        "$BATS_TEST_TMPDIR/source" "$BATS_TEST_TMPDIR/vault"

    while IFS= read -r -d '' original; do
        filename=$(basename "$original")

        # correctly updated
        diff -u "tests/vault521/expected/$filename" "$BATS_TEST_TMPDIR/vault/$filename"

        # didn't modify original source
        diff -u "$original" "$BATS_TEST_TMPDIR/source/$filename"
    done < <(find tests/vault521/input -name "*.md" -print0)

    [ "$status" -eq 0 ]
}
