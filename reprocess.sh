#!/usr/bin/env -S bash -euo pipefail

function main {
    skip_restore=0
    skip_cleaning=0
    skip_breakdown=0
    skip_diff=0
    skip_vault=0
    breakdown_flags=""
    ignore_warnings=""

    while getopts "abcdfhrv" opt; do
        case "$opt" in
            a)  breakdown_flags="${breakdown_flags} -a"
                ;;
            b)  skip_breakdown=1
                ;;
            c)  skip_cleaning=1
                ;;
            d)  skip_diff=1
                ;;
            f)  breakdown_flags="${breakdown_flags} -f"
                ;;
            h)  breakdown_flags="${breakdown_flags} -c"
                ;;
            r)  skip_restore=1
                ;;
            v)  skip_vault=1
                ;;
            *)  usage
                ;;
        esac
    done
    shift $((OPTIND-1))

    [ $# -lt 2 ] \
        && usage

    srd_path="$1"
    directory=$(dirname "$srd_path")
    breakdown_txt="${directory}/breakdown.txt"
    breakdown_md="${directory}/breakdown.md"
    tag="${directory//\//}"

    profile="$2"

    [ $# -ge 3 ] \
        && ignore_warnings="--ignore-warnings ${directory}/$3"

    if [ $skip_restore -eq 0 ]; then
        status "{green}Restoring the files"
        git restore "$srd_path" "$breakdown_txt" "$breakdown_md"
    fi

    if [ $skip_cleaning -eq 0 ]; then
        status -l "{green}Cleaning the SRD"
        python clean_srd.py \
            --progress \
            --profile "$profile" \
            $ignore_warnings \
                "$srd_path" "$breakdown_txt"
        cp "$srd_path" "$breakdown_md"
    fi

    if [ $skip_breakdown -eq 0 ]; then
        status -l "{green}Breaking down the files"
        ./breakdown.sh $breakdown_flags "$breakdown_md"
        status -c ''
    fi

    if [ $skip_diff -eq 0 ]; then
        status -l "{green}Comparing the SRD to the individual Markdown"
        diff -u "$srd_path" <(./rebuild.sh "$breakdown_md")
    fi

    if [ $skip_vault -eq 0 ]; then
        status -l "{green}Making the vault"
        make vault-$tag
    fi
}

function usage {
    sed -e 's/^        //' >&2 <<-EOF
        Usage: reprocess.sh [-a] [-b] [-c] [-d] [-f] [-h] [-r] [-v]
                            <srd_file> <profile> [ignore_warnings]

        Options:
          -b  Skip running breakdown.sh
          -c  Skip running clean_srd.py
          -d  Skip diff/rebuild comparison
          -r  Skip git restore
          -v  Skip making vault

        Options for breakdown.sh:
          -a  Always update files even when the content hasn't changed
          -f  Disable automatic header fixing
          -h  Disable header progression checks
	EOF
    exit 1
}

main "$@"
