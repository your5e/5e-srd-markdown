#!/usr/bin/env -S bash -euo pipefail

exit_code=0

find "$1" -name "*.md" -type f | while read -r file; do
    metadata="$(sed -n '5,8p' "$file")"
    for item in 'Casting Time' 'Range' 'Components' 'Duration'; do
        if ! grep -q "^- \*\*$item:\*\*" <(echo "$metadata"); then
            echo "$file: missing $metadata"
            exit_code=1
        fi
    done
done
exit $exit_code
