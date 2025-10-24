#!/usr/bin/env python

import argparse
import re
from pathlib import Path

from lib.spells import get_spell_list
from lib.magic_items import magic_items
from lib.conditions import conditions
from lib.monsters import monsters
from lib.glossary import get_glossary_terms
from lib.tables import realign_table

spell_list = get_spell_list()
glossary_terms = sorted(get_glossary_terms(), key=len, reverse=True)


def find_matching_noun(text, nouns, filename):
    first_letter = text[0].lower()
    if first_letter not in nouns:
        return None

    for noun in nouns[first_letter]:
        if text.lower() == noun.lower():
            if noun != filename:
                return noun
    return None


def replace_markup_with_link(part, marked_text, wrapper, link_text):
    return re.sub(
        re.escape(wrapper.format(marked_text)),
        link_text,
        part,
        flags=re.IGNORECASE
    )


def italic_nouns_to_wikilinks(lines, index, nouns, filename):
    if lines[index].startswith('#') or '_' not in lines[index]:
        return None

    line = lines[index]
    result = ''
    for part in re.split(r'(\[\[[^\]]+\]\])', line):
        if not part.startswith('[['):
            potential_matches = re.findall(r'_([^_]+)_', part)
            for text in potential_matches:
                noun = find_matching_noun(text, nouns, filename)
                if noun:
                    link_text = '[[{}]]'.format(noun)
                    part = replace_markup_with_link(
                        part, text, '_{}_', link_text
                    )
        result = result + part

    if result != lines[index]:
        lines[index] = result
        return 0
    return None


def process_spell_wikilinks(lines, index, filename):
    return italic_nouns_to_wikilinks(lines, index, spell_list, filename)


def process_magic_item_wikilinks(lines, index, filename):
    return italic_nouns_to_wikilinks(lines, index, magic_items, filename)


def process_monster_wikilinks(lines, index, filename):
    if lines[index].startswith('#') or '**' not in lines[index]:
        return None

    line = lines[index]
    result = ''
    for part in re.split(r'(\[\[[^\]]+\]\])', line):
        if not part.startswith('[['):
            potential_matches = re.findall(r'\*\*([^*]+)\*\*', part)
            for text in potential_matches:
                noun = find_matching_noun(text, monsters, filename)
                if noun:
                    link_text = '**[[{}]]**'.format(noun)
                    part = replace_markup_with_link(
                        part, text, '**{}**', link_text
                    )
                elif text.endswith(('s', 'S')):
                    noun = find_matching_noun(text[:-1], monsters, filename)
                    if noun:
                        link_text = '**[[{}]]s**'.format(noun)
                        part = replace_markup_with_link(
                            part, text, '**{}**', link_text
                        )
        result = result + part

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
    for part in re.split(r'(\[\[[^\]]+\]\]|_\*\*[^*]+\*\*_)', lines[index]):
        if part.startswith('[['):
            # mark conditions in existing wikilinks as seen
            for condition in conditions:
                if condition in part:
                    seen.add(condition)
        elif not part.startswith('_**'):
            # skip feature descriptions
            for condition in conditions:
                if condition not in seen:
                    # skip if condition matches filename
                    if filename and f'{condition.capitalize()}.md' == filename:
                        continue

                    pattern = r'\b' + re.escape(condition) + r'\b'
                    match = re.search(pattern, part, flags=re.IGNORECASE)
                    if match:
                        matched_text = match.group(0)
                        capitalized = matched_text.capitalize()
                        part = re.sub(
                            pattern,
                            f'[[{capitalized}]]',
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


def replace_term_outside_markup(pattern, replacement, line):
    new_line = ''
    found = False
    split_pattern = r'(\[\[[^\]]+\]\]|_\*\*[^*]+\*\*_|\*\*[^*]+\*\*)'
    for part in re.split(split_pattern, line):
        starts_with_markup = (
            part.startswith('[[')
            or part.startswith('_**')
            or part.startswith('**')
        )
        if not starts_with_markup and not found:
            if re.search(pattern, part):
                part = re.sub(pattern, replacement, part, count=1)
                found = True
        new_line = new_line + part
    if found:
        return new_line
    return None


def process_glossary_wikilinks(lines, index, filename):
    if (
        lines[index].startswith('#')                # skip headers
        or lines[index].startswith('|')             # skip tables
        or re.match(r'^_[^_]*_$', lines[index])     # skip feature highlights
        or not any(char.isalpha() for char in lines[index])
        or not glossary_terms
    ):
        return None

    line = lines[index]
    seen = set()

    # mark glossary terms in existing wikilinks as seen
    for part in re.split(r'(\[\[[^\]]+\]\])', line):
        if part.startswith('[['):
            for term in glossary_terms:
                if term in part:
                    seen.add(term)

    # special plural forms processed first
    special_plurals = {
        'Death Saving Throws': 'Death Saving Throw',
        'D20 Tests': 'D20 Test',
    }
    for plural, singular in special_plurals.items():
        if plural not in seen and singular in glossary_terms:
            pattern = r'\b' + re.escape(plural) + r'\b'
            new_line = replace_term_outside_markup(pattern, f'[[{singular}]]s', line)
            if new_line:
                line = new_line
                seen.add(plural)
                seen.add(singular)

    for term in glossary_terms:
        if (
            term == filename
            or term in seen
        ):
            continue

        skip_patterns = {
            # don't link individual terms in compound phrases
            'Action': r'(?<!Legendary )(?<!Bonus )\bAction\b',
            'Attack': r'(?<!Extra )\bAttack\b(?! Roll)',
            'Attack Roll': r'(?<!_Melee )(?<!_Ranged )\bAttack Roll\b',
            'Magic': r'(?<!Pact )\bMagic\b(?! Initiate)',
            'Proficiency': r'\bProficiency\b(?! Bonus)',
            'Resistance': r'(?<!Legendary )\bResistance\b',
            'Save': r'(?<!Death )\bSave\b',
            'Saving Throw': (
                r'(?<!_Intelligence )(?<!_Wisdom )(?<!_Charisma )'
                r'(?<!_Strength )(?<!_Dexterity )(?<!_Constitution )'
                r'\bSaving Throw:_'
            ),

            # don't link in monster statblocks
            'Initiative': r'(?<!- \*\*)\bInitiative\b',
            'Speed': r'(?<!- \*\*)\bSpeed\b',
        }

        if term in skip_patterns:
            pattern = skip_patterns[term]
        else:
            pattern = r'\b' + re.escape(term) + r'\b'

        new_line = replace_term_outside_markup(pattern, f'[[{term}]]', line)
        if new_line:
            line = new_line
            seen.add(term)

    if line != lines[index]:
        lines[index] = line
        return 0
    return None


def process_table_alignment(lines, index, filename):
    return realign_table(lines, index)


def update_vault(
    source_dir, dest_dir, show_progress=False, ignore_file=None, profile='dnd51'
):
    global spell_list, glossary_terms

    spell_list = get_spell_list(profile)
    glossary_terms = sorted(get_glossary_terms(profile), key=len, reverse=True)

    DND51_PROCESSORS = [
        process_spell_wikilinks,
        process_magic_item_wikilinks,
        process_condition_wikilinks,
        process_table_alignment,
    ]

    DND521_PROCESSORS = [
        process_spell_wikilinks,
        process_magic_item_wikilinks,
        process_glossary_wikilinks,
        process_monster_wikilinks,
        process_table_alignment,
    ]

    if profile == 'dnd521':
        processors = DND521_PROCESSORS
    else:
        processors = DND51_PROCESSORS

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

        for processor in processors:
            # changing the lines array necessitates restart, so track line
            last_index = -1

            while True:
                result = None
                for line_index, line in enumerate(lines):
                    if line_index <= last_index:
                        continue

                    if lines[line_index] in ignore_lines:
                        continue

                    result = processor(lines, line_index, source.stem)
                    if result is not None:
                        last_index = line_index + result
                        if result != 0:
                            break

                if result is None:
                    break

        with open(dest, 'w', encoding='utf-8') as handle:
            handle.write('\n'.join(lines) + '\n')

    if show_progress:
        _progress_bar("complete", len(files), '\n')

    # report files no longer in source
    source_files = {f.relative_to(source_path) for f in files}
    dest_files = {f.relative_to(dest_path) for f in dest_path.rglob('*.md')}
    for removed_file in sorted(dest_files - source_files):
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
    parser.add_argument(
        '--profile',
        choices=['dnd51', 'dnd521'],
        help='SRD profile to use (dnd51, dnd521)',
    )
    args = parser.parse_args()

    update_vault(args.source, args.vault, args.progress, args.ignore, args.profile)


if __name__ == "__main__":
    main()
