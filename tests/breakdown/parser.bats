#!/usr/bin/env bats

source breakdown.sh

@test "refuses line lacking enough arguments" {
    parse_breakdown_line \
        '15 file.md' \
        start end action target_file padding_or_offset offset

    [ "$start" = "" ]
    [ "$end" = "" ]
    [ "$action" = "" ]
    [ "$target_file" = "" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "refuses line with impossible line numbers" {
    parse_breakdown_line \
        '0 2 file.md - 1' \
        start end action target_file padding_or_offset offset

    [ "$start" = "" ]
    [ "$end" = "" ]
    [ "$action" = "" ]
    [ "$target_file" = "" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]

    parse_breakdown_line \
        '-1 0 file.md - 1' \
        start end action target_file padding_or_offset offset

    [ "$start" = "" ]
    [ "$end" = "" ]
    [ "$action" = "" ]
    [ "$target_file" = "" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "parses @ directive" {
    parse_breakdown_line \
        '@adjust 1' \
        start end action target_file padding_or_offset offset

    [ "$start" = "@adjust" ]
    [ "$end" = "1" ]
    [ "$action" = "" ]
    [ "$target_file" = "" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "filename with no params" {
    parse_breakdown_line \
        '5 11 extract simple.md' \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "simple.md" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "clears variables" {
    start="99"
    end="100"
    action="append"
    target_file="old_file.md"
    padding_or_offset="old_padding"
    offset="999"

    parse_breakdown_line \
        '5 11 extract simple.md' \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "simple.md" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "append action" {
    parse_breakdown_line \
        '9 9 append sections/combined.md' \
        start end action target_file padding_or_offset offset

    [ "$start" = "9" ]
    [ "$end" = "9" ]
    [ "$action" = "append" ]
    [ "$target_file" = "sections/combined.md" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "spaces are not significant" {
    parse_breakdown_line \
        '   5    11     extract      simple.md' \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "simple.md" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "both optional params" {
    parse_breakdown_line \
        '5 11 extract sections/section_one.md - 1' \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "sections/section_one.md" ]
    [ "$padding_or_offset" = "-" ]
    [ "$offset" = "1" ]
}

@test "optional offset" {
    parse_breakdown_line \
        '14 20 extract sections/section_two.md 1' \
        start end action target_file padding_or_offset offset

    [ "$start" = "14" ]
    [ "$end" = "20" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "sections/section_two.md" ]
    [ "$padding_or_offset" = "1" ]
    [ "$offset" = "" ]
}

@test "optional padding" {
    parse_breakdown_line \
        '23 27 extract sections/section_three.md -' \
        start end action target_file padding_or_offset offset

    [ "$start" = "23" ]
    [ "$end" = "27" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "sections/section_three.md" ]
    [ "$padding_or_offset" = "-" ]
    [ "$offset" = "" ]
}

@test "quoted filename" {
    parse_breakdown_line \
        '5 11 extract "simple file.md"' \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "simple file.md" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "spaces are significant inside filename" {
    parse_breakdown_line \
        '5   11   extract   "simple   file.md"' \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "simple   file.md" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "quoted filename can contain single quotes" {
    parse_breakdown_line \
        "5  11   extract \"sections/section o'neill.md\" - 1" \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = "sections/section o'neill.md" ]
    [ "$padding_or_offset" = "-" ]
    [ "$offset" = "1" ]
}

@test "parses quoted filename with escaped double quote" {
    parse_breakdown_line \
        '5 11 extract "if \"file\" is your real filename.md"' \
        start end action target_file padding_or_offset offset

    [ "$start" = "5" ]
    [ "$end" = "11" ]
    [ "$action" = "extract" ]
    [ "$target_file" = 'if "file" is your real filename.md' ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "refuses malformed line with unclosed quote" {
    parse_breakdown_line \
        '5 11 extract "file with no closing quote.md' \
        start end action target_file padding_or_offset offset

    [ "$start" = "" ]
    [ "$end" = "" ]
    [ "$action" = "" ]
    [ "$target_file" = "" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}

@test "clears variables with malformed lines" {
    start="99"
    end="100"
    action="append"
    target_file="old_file.md"
    padding_or_offset="-"
    offset="5"

    parse_breakdown_line \
        '5 11 extract "file with no closing quote.md' \
        start end action target_file padding_or_offset offset

    [ "$start" = "" ]
    [ "$end" = "" ]
    [ "$action" = "" ]
    [ "$target_file" = "" ]
    [ "$padding_or_offset" = "" ]
    [ "$offset" = "" ]
}
