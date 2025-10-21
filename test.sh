#!/usr/bin/env -S bash -euo pipefail

trap 'exit 130' INT
failed=0

function main {
    run_tests tests/alter
    run_tests tests/breakdown
    run_tests tests/clean
    run_tests tests/clean51
    run_tests tests/clean521
    run_tests tests/headers
    run_tests tests/rebuild
    run_tests tests/vault
    run_tests tests/vault521
}

function run_tests {
    echo "$1:"

    bats "$1" \
        || failed=1

    echo ''
}

main "$@"
exit $failed
