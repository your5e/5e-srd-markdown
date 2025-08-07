#!/usr/bin/env -S bash -euo pipefail

function main {
    local action="${1:-}"
    local root_dir="${2:-}"

    [ -z "$action" -o -z "$root_dir" ] \
        && error "Usage: vault_patches.sh create|apply <dir>"

    local vault="$root_dir/obsidian_vault"
    local patches="$root_dir/obsidian_patches"

    [ ! -d "$vault" ] \
        && error "Error: Vault directory $vault does not exist"

    case "$action" in
        create) create_patches "$vault" "$patches" ;;
        apply)  apply_patches  "$vault" "$patches" ;;
        *)      error "Error: invalid action '$action'" ;;
    esac
}

function create_patches {
    local vault="$1"
    local patches="$2"

    mkdir -p "$patches"

    local modified_files=$(
        git diff --name-only \
            | grep "^$vault/" \
                || true
    )
    [ -z "$modified_files" ] \
        && exit 0

    for file in $modified_files; do
        local patching=$(
            echo "$file" \
                | sed "s#^$vault/##" \
                | sed 's#\.md$##'
        )

        # create simplified patch
        mkdir -p $(dirname "$patches/$patching")
        {
            echo "--- $patching.md"
            echo "+++ $patching.md"
            git diff "$file" | sed -n '/^@@/,$p'
        } > "$patches/$patching.patch"

        echo "++ $patching.patch"
    done
}

function apply_patches {
    local vault="$1"
    local patches="$2"
    local exit_code=0

    [ ! -d "$patches" ] \
        && error "Error: '$patches' does not exist"

    local patch_files=$(find "$patches" -name "*.patch")
    [ -z "$patch_files" ] \
        && exit 0

    for file in $patch_files; do
        local patch=$(
            echo "$file" \
                | sed "s#^$patches/##" \
                | sed 's#\.patch$##'
        )

        local patching="$vault/$patch.md"
        if [ -f "$patching" ]; then
            local output
            if output=$(patch "$patching" < "$file" 2>&1); then
                echo "== $patch.md"
            else
                error "Failed to apply patch to $patching:"
                echo "$output"
            fi
        else
            echo "   $patch.md -- missing"
            exit_code=1
        fi
    done

    exit $exit_code
}

function error {
    echo "$1" >&2
    exit "${2:-1}"
}

main "$@"
