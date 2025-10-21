#!/usr/bin/env bats

@test "5.1 srd spells look right" {
    run tests/srd/check_spell_format.sh dnd/51/markdown/spells
    diff -u <(echo "$output") <(echo "")
    [ "$status" -eq 0 ]
}

@test "5.1 srd statblocks look right" {
    run tests/srd/check_statblock_format.sh dnd/51/markdown/statblocks
    diff -u <(echo "$output") <(echo "")
    [ "$status" -eq 0 ]
}

@test "5.2.1 srd spells look right" {
    run tests/srd/check_spell_format.sh dnd/521/markdown/Spells/*/*
    diff -u <(echo "$output") <(echo "")
    [ "$status" -eq 0 ]
}

@test "5.2.1 srd statblocks look right" {
    run tests/srd/check_statblock_format.sh dnd/521/markdown/Monsters
    diff -u <(echo "$output") <(echo "")
    [ "$status" -eq 0 ]
}
