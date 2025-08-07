#!/usr/bin/env bats

setup() {
    TEST_VAULT="$BATS_TEST_TMPDIR/test_root/obsidian_vault"
    TEST_PATCHES="$BATS_TEST_TMPDIR/test_root/obsidian_patches"

    mkdir -p "$TEST_VAULT/classes/druid"
    cp "$BATS_TEST_DIRNAME/input/druid.md" "$TEST_VAULT/classes/druid/"
    mkdir -p "$TEST_VAULT/statblocks"
    cp "$BATS_TEST_DIRNAME/input/goblin.md" "$TEST_VAULT/statblocks/"

    mkdir -p "$TEST_PATCHES/classes/druid"
    cp "$BATS_TEST_DIRNAME/patches/druid.patch" "$TEST_PATCHES/classes/druid/"
    mkdir -p "$TEST_PATCHES/statblocks"
    cp "$BATS_TEST_DIRNAME/patches/goblin.patch" "$TEST_PATCHES/statblocks/"

    cp vault_patches.sh "$BATS_TEST_TMPDIR"
    chmod +x "$BATS_TEST_TMPDIR/vault_patches.sh"

    cd "$BATS_TEST_TMPDIR"
    git init --quiet
    git config user.email "test@example.com"
    git config user.name "Test User"
    git config commit.gpgsign false
    git config tag.gpgsign false
    git add .
    git commit --quiet -m "Initial test files"
}

@test "show usage" {
    expected_output=$(sed -e 's/^        //' <<"        EOF"
        Usage: vault_patches.sh create|apply <dir>
        EOF
    )

    run ./vault_patches.sh
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "show error with invalid action" {
    expected_output=$(sed -e 's/^        //' <<"        EOF"
        Error: invalid action 'invalid'
        EOF
    )

    run ./vault_patches.sh invalid test_root
    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}

@test "no patches in clean repo" {
    run ./vault_patches.sh create test_root
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "no patches with new file" {
    echo "A new file shouldn't create a patch." \
        >> "$TEST_VAULT/statblocks/sample_monster.md"

    run ./vault_patches.sh create test_root
    diff -u <(echo "") <(echo "$output")
    [ "$status" -eq 0 ]
}

@test "create patches" {
    expected_output=$(sed -e 's/^        //' <<"        EOF"
        ++ classes/druid/druid.patch
        EOF
    )

    # change the file to make a patch
    rm -rf "$TEST_PATCHES/classes/druid"
    cp "$BATS_TEST_DIRNAME/expected/druid.md" "$TEST_VAULT/classes/druid/druid.md"

    run ./vault_patches.sh create test_root

    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u "$BATS_TEST_DIRNAME/patches/druid.patch" "$TEST_PATCHES/classes/druid/druid.patch"
    [ "$status" -eq 0 ]
}

@test "apply both patches" {
    expected_output=$(sed -e 's/^        //' <<"        EOF"
        == classes/druid/druid.md
        == statblocks/goblin.md
        EOF
    )

    run ./vault_patches.sh apply test_root

    diff -u <(echo "$expected_output") <(echo "$output")
    diff -u "$BATS_TEST_DIRNAME/expected/druid.md" "$TEST_VAULT/classes/druid/druid.md"
    diff -u "$BATS_TEST_DIRNAME/expected/goblin.md" "$TEST_VAULT/statblocks/goblin.md"
    [ "$status" -eq 0 ]
}


@test "apply fails when original file missing" {
    expected_output=$(sed -e 's/^        //' <<"        EOF"
           classes/druid/druid.md -- missing
        == statblocks/goblin.md
        EOF
    )

    rm "$TEST_VAULT/classes/druid/druid.md"

    run ./vault_patches.sh apply test_root

    diff -u <(echo "$expected_output") <(echo "$output")
    [ "$status" -eq 1 ]
}
