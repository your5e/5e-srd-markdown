#!/usr/bin/env python

import argparse
import re
from pathlib import Path

from lib.spells import spells
from lib.magic_items import magic_items
from lib.conditions import conditions
from lib.tables import realign_table


def proper_nouns_to_wikilinks(line, nouns, filename):
    potential_matches = re.findall(r'_([^_]+)_', line)
    for text in potential_matches:
        first_letter = text[0].lower()
        if first_letter in nouns:
            for noun in nouns[first_letter]:
                if text.lower() == noun.lower():
                    link = re.sub(
                        r'[^a-zA-Z0-9]',
                        '_',
                        noun.lower()
                    ).strip('_')

                    if link != filename:
                        link_text = f'[[{link}|{noun}]]'
                        if line.startswith('|'):
                            link_text = f'[[{link}\\|{noun}]]'
                        line = re.sub(
                            re.escape(f'_{text}_'),
                            link_text,
                            line,
                            flags=re.IGNORECASE
                        )
                        break

    return line


def process_spell_wikilinks(lines, index, filename):
    if (
        lines[index].startswith('#')
        or '_' not in lines[index]
    ):
        return None

    result = proper_nouns_to_wikilinks(lines[index], spells, filename)
    if result != lines[index]:
        lines[index] = result
        return 0
    return None


def process_magic_item_wikilinks(lines, index, filename):
    if (
        lines[index].startswith('#')
        or '_' not in lines[index]
    ):
        return None

    result = proper_nouns_to_wikilinks(lines[index], magic_items, filename)
    if result != lines[index]:
        lines[index] = result
        return 0
    return None


def process_condition_wikilinks(lines, index, filename):
    if (
        lines[index].startswith('#')
        or not any(char.isalpha() for char in lines[index])
        or '**Condition Immunities**' in lines[index]
    ):
        return None

    line = ''
    seen = set()
    for part in re.split(r'(\[\[[^\]]+\]\])', lines[index]):
        # ignore existing wikilinks
        if not part.startswith('[['):
            for condition in conditions:
                if condition not in seen:
                    pattern = r'\b' + re.escape(condition) + r'\b'
                    if re.search(pattern, part, flags=re.IGNORECASE):
                        part = re.sub(
                            pattern,
                            f'[[{condition}]]',
                            part,
                            flags=re.IGNORECASE,
                            count=1,
                        )
                        seen.add(condition)
        line = line + part

    if line != lines[index]:
        lines[index] = line
        return 0
    return None


def process_table_alignment(lines, index, filename):
    return realign_table(lines, index)


def process_vault_file(lines, filename, ignore_lines):
    PROCESSORS = [
        process_spell_wikilinks,
        process_magic_item_wikilinks,
        process_condition_wikilinks,
        process_table_alignment,
    ]

    for processor in PROCESSORS:
        # changing the lines array necessitates restart, so track line
        last_index = -1

        while True:
            result = None
            for index, line in enumerate(lines):
                if index <= last_index:
                    continue

                if lines[index] in ignore_lines:
                    continue

                result = processor(lines, index, filename)
                if result is not None:
                    last_index = index + result
                    if result != 0:
                        break

            if result is None:
                break

    return '\n'.join(lines) + '\n'


def update_vault(source_dir, dest_dir, show_progress=False, ignore_file=None):
    def _progress_bar(filename, index, end='\r'):
        if show_progress:
            filename_width = 54
            if len(filename) > filename_width:
                side_chars = (filename_width - 2) // 2
                filename = f"{filename[:side_chars]}..{filename[-side_chars:]}"
            filled = int(round(min(index / len(files), 1.0) * 100, 1) / 2)
            bar = (
                '█' * filled
                + '░' * (50 - filled)  # 50 character bar
            )
            print(
                f"{filename:{filename_width}} {index:4}/{len(files):4} [{bar}]",
                end=end,
                flush=True
            )

    ignore_lines = set()
    if ignore_file:
        with open(ignore_file, 'r', encoding='utf-8') as handle:
            ignore_lines = set(
                line.strip()
                    for line in handle
                        if line.strip()
            )

    source_path = Path(source_dir)
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")
    files = list(source_path.rglob('*.md'))

    dest_path = Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)

    for index, markdown in enumerate(files):
        with open(markdown, 'r', encoding='utf-8') as handle:
            lines = handle.read().splitlines()

        source = markdown.relative_to(source_path)
        dest = dest_path / source
        dest.parent.mkdir(parents=True, exist_ok=True)
        if show_progress:
            _progress_bar(str(source), index)

        with open(dest, 'w', encoding='utf-8') as handle:
            handle.write(process_vault_file(lines, source.stem, ignore_lines))

    if show_progress:
        _progress_bar("complete", len(files), '\n')

    # report files no longer in source
    source_files = {f.relative_to(source_path) for f in files}
    dest_files = {f.relative_to(dest_path) for f in dest_path.rglob('*.md')}
    for removed_file in dest_files - source_files:
        print(f"{removed_file}: no longer in source directory")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown fragments to Obsidian vault'
    )
    parser.add_argument(
        'source',
        help='Source directory containing Markdown',
    )
    parser.add_argument(
        'vault',
        help='Obsidian vault',
    )
    parser.add_argument(
        '--progress',
        action='store_true',
        help='Show progress bar',
    )
    parser.add_argument(
        '--ignore',
        help='Source lines to ignore during conversion',
    )
    args = parser.parse_args()

    update_vault(args.source, args.vault, args.progress, args.ignore)


if __name__ == "__main__":
    main()
