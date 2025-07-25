#!/usr/bin/env python

import argparse
import re
import sys
from tabulate import tabulate


def header_to_text(text):
    # "#### **Black Tentacles**" -> "Black Tentacles"
    return text.lstrip('#').strip().strip('*').strip()


def check_duration_length(line):
    # "**Duration:** Concentration, up to 1 minute Squirming, ebony tentacles..."
    duration_match = re.search(r'\*\*Duration:\*\*\s+(.+)', line)
    if duration_match:
        duration_content = duration_match.group(1)
        if len(duration_content.split()) > 5:
            return f"Duration value has more than 5 words, likely contains description: '{line}'"


def check_srd(lines):
    TESTS_TABLE = {
        # match on          check with
        '**Duration':       check_duration_length,
    }

    error_messages = []
    for index, line in enumerate(lines):
        for match, checker in TESTS_TABLE.items():
            if match in line:
                message = checker(line)
                if message:
                    context = 'file'
                    for prev in range(index - 1, -1, -1):
                        if lines[prev].startswith('#'):
                            context = header_to_text(lines[prev])
                            break
                    error_messages.append(f"{context}, {index}:\n{message}\n")
    if error_messages:
        raise ValueError('\n'.join(error_messages))


def warn_table_runon(lines, index):
    # for when a table is split across pages in the PDF
    if (
            index > 2
        and lines[index-1] == ''
        and '|' in lines[index-2]
    ):
        return "possible table run-on error"
    return None


def warn_srd(lines):
    WARN_TABLE = {
        # match on          check with
        '|':                warn_table_runon,
    }

    for index, line in enumerate(lines):
        for match, checker in WARN_TABLE.items():
            if match in line:
                message = checker(lines, index)
                if message:
                    context = 'file'
                    for prev in range(index - 1, -1, -1):
                        if lines[prev].startswith('#'):
                            context = header_to_text(lines[prev])
                            break
                    print(f"Warning: {context}, {index + 1}: {message}", file=sys.stderr)


def clean_whitespace(lines, index):
    spaces = re.sub(r'[^\S\n]+', ' ', lines[index])
    brs = spaces.replace('<br>', ' ')
    if brs != lines[index]:
        lines[index] = brs
        return 0
    return None


def clean_table_alignment(lines, index):
    if not lines[index].startswith('|'):    # not a table
        return None
    if index > 1 and lines[index-1] != '':  # not start of table
        return None
    if not all(
        re.match(r'^:?-+:?$', cell.strip())
            for cell in lines[index+1].split('|')[1:-1]
    ):                                      # doesn't look like a table
        return None

    table_end = index
    while table_end < len(lines) - 1 and lines[table_end + 1].startswith('|'):
        table_end += 1

    rows = []
    for line in lines[index+2:table_end+1]:
        cells = [
            cell.strip()
                for cell in line.split('|')[1:-1]
        ]
        if not cells:
            continue
        if any(cell.strip() for cell in cells):
            rows.append(cells)

    aligned = tabulate(
            rows,
            headers=[
                cell.strip()
                    for cell in lines[index].split('|')[1:-1]
            ],
            tablefmt='github'
        ).split('\n')
    for i, new_line in enumerate(aligned):
        lines[index + i] = new_line

    difference = len(aligned) - (table_end - index + 1)
    if difference < 0:
        for _ in range(-difference):
            lines.pop(index + len(aligned))

    return difference


def clean_srd(lines, breakdown_data):
    CONVERSIONS_TABLE = [
        clean_whitespace,
        clean_table_alignment,
    ]

    changes = 0
    for cleaner in CONVERSIONS_TABLE:
        for index, line in enumerate(lines):
            result = cleaner(lines, index)
            if result is not None:
                changes += 1
                if breakdown_data is not None:
                    update_breakdown_data(breakdown_data, index, result)

    if changes > 0:
        return '\n'.join(lines + [''])
    return None


def load_breakdown_data(breakdown_file):
    breakdown_data = []
    with open(breakdown_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                rest = line.find(parts[1]) + len(parts[1])
                breakdown_data.append([
                    int(parts[0]),
                    int(parts[1]),
                    line[rest:].rstrip('\n'),
                ])
            else:
                breakdown_data.append(line.rstrip('\n'))

    return breakdown_data


def update_breakdown_data(breakdown_data, change_line, adjustment):
    for entry in breakdown_data:
        if isinstance(entry, list):
            if entry[0] >= change_line:
                entry[0] += adjustment
            if entry[1] >= change_line:
                entry[1] += adjustment


def write_breakdown_data(breakdown_file, breakdown_data):
    with open(breakdown_file, 'w', encoding='utf-8') as f:
        for entry in breakdown_data:
            if isinstance(entry, list):
                f.write(f"{entry[0]:>6} {entry[1]:>6}{entry[2]}\n")
            else:
                f.write(f"{entry}\n")


def main():
    parser = argparse.ArgumentParser(description='Clean SRD markdown format')
    parser.add_argument('markdown', help='Input markdown file')
    parser.add_argument('breakdown_file', nargs='?', help='Optional breakdown file to update')
    parser.add_argument('--debug', action='store_true', help='Print changes to stdout instead of modifying file')
    args = parser.parse_args()

    try:
        if args.markdown == '-':
            lines = sys.stdin.read().splitlines()
        else:
            with open(args.markdown, 'r', encoding='utf-8') as handle:
                lines = handle.read().splitlines()

        breakdown_data = None
        if args.breakdown_file:
            breakdown_data = load_breakdown_data(args.breakdown_file)

        check_srd(lines)
        warn_srd(lines)
        cleaned = clean_srd(lines, breakdown_data)

        if cleaned:
            if args.debug or args.markdown == '-':
                print(cleaned, end='')
            else:
                with open(args.markdown, 'w', encoding='utf-8') as handle:
                    handle.write(cleaned)
                if args.breakdown_file and breakdown_data:
                    write_breakdown_data(args.breakdown_file, breakdown_data)


    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
