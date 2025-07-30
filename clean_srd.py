#!/usr/bin/env python

import argparse
import re
import sys
from tabulate import tabulate

from lib.spells import spells
from lib.magic_items import magic_items


def check_duration_length(line):
    # "**Duration:** Concentration, up to 1 minute Squirming, ebony tentacles..."
    duration_match = re.search(r'\*\*Duration:\*\*\s+(.+)', line)
    if duration_match:
        duration_content = duration_match.group(1)
        if len(duration_content.split()) > 5:
            return f"Duration value has more than 5 words, likely contains description: '{line}'"


def check_srd(lines):
    TESTS_TABLE = [
        check_duration_length,
    ]

    error_messages = []
    for index, line in enumerate(lines):
        for checker in TESTS_TABLE:
            message = checker(line)
            if message:
                context = 'file'
                for prev in range(index - 1, -1, -1):
                    if lines[prev].startswith('#'):
                        context = lines[prev]
                        break
                error_messages.append(f"{context}, {index}:\n{message}\n")
    if error_messages:
        raise ValueError('\n'.join(error_messages))


def clean_whitespace(lines, index):
    # why <br>s for the love of...
    spaces = lines[index].replace('<br>', ' ')
    spaces = re.sub(r'[\t\r\f\v\u00a0\u2000-\u200b\u2028\u2029\u3000]', ' ', spaces)
    if spaces != lines[index]:
        lines[index] = spaces
        return 0
    return None


def clean_unicode_chars(lines, index):
    # usable characters over clever typographic characters
    replacements = {
        '\u0336': '—',  # "combining long stroke overlay" to em-dash
        '\u2212': '-',  # "minus sign" to hyphen
    }

    original = lines[index]
    for old, new in replacements.items():
        lines[index] = lines[index].replace(old, new)
    if lines[index] != original:
        return 0
    return None


def clean_table_alignment(lines, index):
    if not lines[index].startswith('|'):    # not a table
        return None
    if index > 1 and lines[index-1] != '':  # not start of table
        return None
    if not all(                             # doesn't look like a table
        re.match(r'^:?-+:?$', cell.strip())
            for cell in lines[index+1].split('|')[1:-1]
    ):
        return None

    headers = [re.sub(r' +', ' ', cell.strip()) for cell in lines[index].split('|')[1:-1]]
    table_end = index

    while True:
        # find the end of the table
        while table_end < len(lines) - 1 and lines[table_end + 1].startswith('|'):
            table_end += 1

        # look for the same table to continue after a page break
        if table_end+3 < len(lines) and lines[table_end+3].startswith('|'):
            cells = [cell for cell in lines[table_end+3].split('|')[1:-1]]
            if len(cells) != len(headers):
                break
            if all('--' in cell for cell in cells):
                break
            table_end += 3
        else:
            break

    rows = []
    for line in lines[index+2:table_end+1]:
        cells = [
            re.sub(r' +', ' ', cell.strip())
                for cell in line.split('|')[1:-1]
        ]
        # ensure number of cells matches headers
        cells = (cells + [''] * len(headers))[:len(headers)]
        if any(cell for cell in cells):
            rows.append(cells)

    # remove columns where every cell is empty
    remove = []
    for column in range(len(headers)):
        if not headers[column] and all(not row[column] for row in rows):
            remove.append(column)
    for column in reversed(remove):
        del headers[column]
        for row in rows:
            del row[column]

    aligned = tabulate(rows, headers=headers, tablefmt='github').split('\n')
    for i, new_line in enumerate(aligned):
        lines[index + i] = new_line

    difference = len(aligned) - (table_end - index + 1)
    if difference < 0:
        del lines[index + len(aligned):index + len(aligned) - difference]
    return difference


def clean_midsentence_pagebreak(lines, index):
    # rejoin paragraphs split by pagebreaks
    if index > 1 and lines[index] and lines[index][0].islower():
        if lines[index - 1] == '' and lines[index - 2][-1].islower():
            lines[index - 2] = lines[index - 2] + ' ' + lines[index]
            del lines[index-1:index+1]
            return -2
    return None


def clean_remove_mistaken_headers(lines, index):
    # "#### **Duration:** Instantaneous" -> "**Duration:** Instantaneous"
    removed = re.sub(r'^#+\s+((?:\*\*[^*]+\*\*\s+\S.*)|(?:\*[^*]+\*))$', r'\1', lines[index])
    if removed != lines[index]:
        lines[index] = removed
        return 0
    return None


def clean_remove_header_bold(lines, index):
    # "### **High Elf**" -> "### High Elf"
    header_pattern = r'^(#+)\s*\*\*([^*]+)\*\*\s*$'
    if re.match(header_pattern, lines[index]):
        lines[index] = re.sub(header_pattern, r'\1 \2', lines[index])
        return 0
    return None


def clean_leading_emphasis(lines, index):
    # "*Some words.* More words..." but in the PDF rendered bold italic
    if index > 1 and lines[index - 1].strip() != "":
        return None

    bold_italics = re.sub(r'^\*([^*]+\.)\*', r'_**\1**_', lines[index])
    if bold_italics != lines[index]:
        lines[index] = bold_italics
        return 0
    return None


def clean_statblock_attack_emphasis(lines, index):
    # "*[Words.] [Words] Attack:*" -> "_**[Words.]** [Words] Attack:_"
    attack = re.sub(r'^\*([^*]+\.)\s+([^*]+Attack:)\*', r'_**\1** \2_', lines[index])
    if attack != lines[index]:
        lines[index] = attack
        return 0
    return None


def clean_unwrap_consecutive_bold(lines, index):
    # **Hit Dice**, **Hit Points**, ... -- sometimes on one line
    if lines[index].startswith('**') and ' **' in lines[index]:
        bold_words = re.findall(r'\*\*([^*]+)\*\*', lines[index])
        if not all(word[0].isupper() for word in bold_words if word):
            return None

        parts = re.split(r'\s+(?=\*\*[^*]+\*\*)', lines[index])
        difference = -1
        if index < len(lines)-1 and lines[index+1] == '':
            del lines[index+1]
            difference = -2
        del lines[index]

        # maintain index by inserting the parts backwards
        for i in range(len(parts)-1, -1, -1):
            lines[index:index] = [parts[i].strip(), '']
            difference += 2

        return difference
    return None


def _wrapup_matching_lines(lines, index, pattern, indent=''):
    if re.match(pattern, lines[index]):
        current = index
        while current < len(lines) - 2:
            if (
                lines[current + 1] == ''
                and re.match(pattern, lines[current + 2])
            ):
                del lines[current + 1]
                current += 1
            else:
                break

        if current > index:
            for line in range(index, current+1):
                lines[line] = f"{indent}- {lines[line]}"
            return index - current
    return None


def clean_wrapup_feature_lists(lines, index):
    # "_**words.**_ ... \n _**words.**_ ..." -- listify
    return _wrapup_matching_lines(lines, index, r'^_\*\*[^*]+\.\*\*')


def clean_wrapup_attribute_lists(lines, index):
    # **Hit Dice** ... \n **Hit Points** ... -- listify
    return _wrapup_matching_lines(lines, index, r'^\*\*[^*]+\*\*')


def clean_statblock_spells_to_list(lines, index):
    # "Cantrips", "1st level (4 slots)", "3/day" -- listify
    return _wrapup_matching_lines(lines, index, r'^(Cantrips|At will|[0-9]+[a-z]* level|[0-9]+/day)', '    ')


def clean_single_action_to_list(lines, index):
    # "_**" alone after a header, still a list (of one)
    if (
        lines[index].startswith('_**')
        and lines[index - 1] == ''
        and lines[index - 2].startswith('#')
        and (
            lines[index - 2].endswith('Actions')
            or lines[index - 2].endswith('Traits')
            or lines[index - 2].endswith('Reactions')
        )
    ):
        lines[index] = '- ' + lines[index]
        return 0
    return None


def clean_statblock_spellcasting_marker(lines, index):
    # "_**Spellcasting.**_" before a list of spells
    if re.match(r'^_\*\*(?:Innate\s+)?Spellcasting\.\*\*_', lines[index]):
        if (
            index + 2 < len(lines)
            and lines[index + 1] == ''
            and lines[index + 2].startswith('    - ')
        ):
            lines[index] = '- ' + lines[index]
            return 0
    return None


def clean_canonicalise_proper_nouns(lines, index):
    # *speak with dead.* -> _Speak with Dead_.
    original = lines[index]

    potential_matches = re.findall(r'\*([a-zA-Z][^*]*?)\*', lines[index])
    for match in potential_matches:
        # grouped by first letter to speed up matching
        first_letter = match[0].lower()
        for names in [spells, magic_items]:
            if first_letter in names:
                for name in names[first_letter]:
                    # punctuation moves outside of the emphasis
                    pattern = r'(?<!\*)\*\b' + re.escape(name.lower()) + r'\b([.,:;!?]*)\*(?!\*)'
                    replacement = f'_{name}_\\1'
                    lines[index] = re.sub(pattern, replacement, lines[index], flags=re.IGNORECASE)

    if lines[index] != original:
        return 0
    return None


def clean_add_traits_header(lines, index):
    # add Traits after CR for visual separation
    if (
        lines[index].startswith('**Challenge**')
        and index + 2 < len(lines)
        and lines[index + 1] == ''
        and not lines[index + 2].startswith('#')
    ):
        lines[index + 1:index + 1] = ['', '#### Traits']
        return 2
    return None


def clean_italic_emphasis_markers(lines, index):
    # *word* -> _word_
    italics = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'_\1_', lines[index])
    if italics != lines[index]:
        lines[index] = italics
        return 0
    return None


def clean_srd(lines, breakdown_data, show_progress=False):
    def _progress_bar(end):
        if show_progress:
            filled = int(round(min(index / len(lines), 1.0) * 100, 1) / 2)
            bar = (
                '█' * filled
                + '░' * (50 - filled)
            )
            print(f"- {cleaner.__name__:40} {index:6} [{bar}]", end=end)

    CONVERSIONS_TABLE = [
        # common problems
        clean_whitespace,
        clean_unicode_chars,
        clean_table_alignment,
        clean_midsentence_pagebreak,

        # PDF->MD mistakes
        clean_remove_mistaken_headers,
        clean_remove_header_bold,
        clean_unwrap_consecutive_bold,

        # 5.1 SRD specific formatting
        clean_add_traits_header,
        clean_leading_emphasis,
        clean_statblock_attack_emphasis,
        clean_wrapup_feature_lists,
        clean_wrapup_attribute_lists,
        clean_statblock_spells_to_list,
        clean_single_action_to_list,
        clean_statblock_spellcasting_marker,

        # sanitation
        clean_canonicalise_proper_nouns,

        # markdown preferences
        clean_italic_emphasis_markers,
    ]

    changes = 0
    for cleaner in CONVERSIONS_TABLE:
        # changing the lines array necessitates restart, so track line
        last_index = -1

        while True:
            result = None
            for index, line in enumerate(lines):
                if index <= last_index:
                    continue

                _progress_bar('\r')

                result = cleaner(lines, index)
                if result is not None:
                    last_index = index + result
                    changes += 1
                    if result != 0:
                        if breakdown_data is not None:
                            update_breakdown_data(breakdown_data, index, result)
                    break

            if result is None:
                break

        _progress_bar('\n')

    if changes > 0:
        return '\n'.join(lines + [''])
    return None


def warn_table_runon(lines, index):
    # probably a table split across pages, but marker gave it new headers
    if '|' not in lines[index]:
        return None
    if (
            index > 2
        and lines[index-1] == ''
        and '|' in lines[index-2]
    ):
        if len(lines[index].split('|')[1:-1]) == len(lines[index-2].split('|')[1:-1]):
            return "possible table run-on"


def warn_midpara_italics(lines, index):
    # look for mid-paragraph italics that could be a source wrapping error
    matches = re.findall(r'[\w.].*?_([A-Z][^_]*[:\.])_', lines[index])
    for match in matches:
        if (
            not match.startswith("**")
            and match != "Player's Handbook."
            and match != "Hit:"
        ):
            return f"possible mistaken mid-paragraph italic: '{match}'"
    return None


def warn_inconsistent_list_formatting(lines, index):
    # detect changes in list item emphasis formatting within a section
    if index == 0:
        return None

    emphasis = re.match(r'^- [_\*]+', lines[index])
    if not emphasis:
        return None

    previous_emphasis = re.match(r'^- [_\*]+', lines[index-1])
    if not previous_emphasis:
        return None
    elif emphasis.group() != previous_emphasis.group():
        return "inconsistent list formatting (emphasis type mismatch)"

    return None


def warn_unusual_unicode(lines, index):
    # let's not be too clever
    unusual_chars = set()
    for char in lines[index]:
        if ord(char) >= 0x2070:
            unusual_chars.add(f"U+{ord(char):04X}")
    if unusual_chars:
        return f"unusual Unicode characters: {', '.join(sorted(unusual_chars))}"


def warn_srd(lines):
    WARN_TABLE = [
        warn_table_runon,
        warn_midpara_italics,
        warn_inconsistent_list_formatting,
        warn_unusual_unicode,
    ]

    for index, line in enumerate(lines):
        for checker in WARN_TABLE:
            message = checker(lines, index)
            if message:
                context = 'file'
                for prev in range(index - 1, -1, -1):
                    if lines[prev].startswith('#'):
                        context = lines[prev]
                        break
                print(f"Warning: {context}, {index + 1}: {message}", file=sys.stderr)


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
    parser.add_argument('--warn', action='store_true', help='Only run warning checks, skip cleaning and error checks')
    parser.add_argument('--progress', action='store_true', help='Show progress through the file')
    args = parser.parse_args()

    try:
        if args.markdown == '-':
            lines = sys.stdin.read().splitlines()
        else:
            with open(args.markdown, 'r', encoding='utf-8') as handle:
                lines = handle.read().splitlines()

        cleaned = False
        if not args.warn:
            breakdown_data = None
            if args.breakdown_file:
                breakdown_data = load_breakdown_data(args.breakdown_file)

            check_srd(lines)
            cleaned = clean_srd(lines, breakdown_data, args.progress)

        warn_srd(lines)

        if cleaned:
            if args.debug or args.markdown == '-':
                print(cleaned, end='')
            else:
                with open(args.markdown, 'w', encoding='utf-8') as handle:
                    handle.write(cleaned)
                if args.breakdown_file and breakdown_data:
                    write_breakdown_data(args.breakdown_file, breakdown_data)


    except FileNotFoundError as e:
        print(f"Error '{e.filename}' not found")
        sys.exit(1)

    except Exception as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
