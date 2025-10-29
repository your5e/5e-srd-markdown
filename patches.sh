#!/usr/bin/env -S bash -euo pipefail

function main {
    local dir="${1:-}"
    local action="${2:-}"

    [ -z "$dir" -o -z "$action" ] \
        && error "Usage: patches.sh <dir> create|apply"

    [ ! -d "$dir" ] \
        && error "Error: Directory $dir does not exist"

    local patches_dir="${dir}_patches"

    case "$action" in
        create) create_patches "$dir" "$patches_dir" ;;
        apply)  apply_patches  "$dir" "$patches_dir" ;;
        *)      error "Error: invalid action '$action'" ;;
    esac
}

function create_patches {
    local dir="$1"
    local patches="$2"

    mkdir -p "$patches"

    local modified_files=$(
        git diff --name-only \
            | grep "^$dir/" \
                || true
    )
    [ -z "$modified_files" ] \
        && exit 0

    for file in $modified_files; do
        local patching=$(
            echo "$file" \
                | sed "s#^$dir/##" \
                | sed 's#\.md$##'
        )

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
    local dir="$1"
    local patches="$2"
    local exit_code=0

    [ ! -d "$patches" ] \
        && exit 0

    local patch_files=$(find "$patches" -name "*.patch")
    [ -z "$patch_files" ] \
        && exit 0

    for file in $patch_files; do
        local patch=$(
            echo "$file" \
                | sed "s#^$patches/##" \
                | sed 's#\.patch$##'
        )

        local target_file="$dir/$patch.md"

        if [ -f "$target_file" ]; then
            local output
            if output=$(patch -R --dry-run -f -r- --no-backup-if-mismatch "$target_file" < "$file" 2>&1); then
                echo "   $patch.md -- already applied"
            elif output=$(patch -f -r- --no-backup-if-mismatch "$target_file" < "$file" 2>&1); then
                echo "== $patch.md"
            else
                error "Failed to apply patch to $target_file:"
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
