#!/usr/bin/env python

import argparse
import re
import sys

from lib.spells import get_spell_list, get_next_unemphasised_spell
from lib.magic_items import magic_items
from lib.tables import realign_table

spell_list = get_spell_list()
spell_matcher = get_next_unemphasised_spell(spell_list)

ABILITIES = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
NUMERIC_PROPERTIES = ['AC', 'Initiative', 'HP', 'Speed', 'CR']
PROPERTIES = [
    'Skills', 'Resistances', 'Immunities', 'Senses', 'Languages',
    'Vulnerabilities'
]
ALL_PROPERTIES = NUMERIC_PROPERTIES + PROPERTIES + ABILITIES
MODIFIER_CHARS = '+-−0123456789'


def get_table_headers(lines, index):
    if not lines[index].startswith('|'):
        return None

    start = index
    while start > 0 and lines[start - 1].startswith('|'):
        start -= 1

    separator = start + 1
    if (
        separator >= len(lines)
        or '-' not in lines[separator]
        or index <= separator
    ):
        return None

    return [cell.strip() for cell in lines[start].split('|')[1:-1]]


def clean_whitespace(lines, index):
    # why <br>s for the love of...
    spaces = lines[index].replace('<br>', ' ')
    spaces = re.sub(r'[\t\r\f\v\u00a0\u2000-\u200b\u2028\u2029\u3000]', ' ', spaces)
    if spaces != lines[index]:
        lines[index] = spaces
        return 0
    return None


def clean_wrap_blank_lines(lines, index):
    # remove consecutive blank lines
    if (
        index < len(lines) - 1
        and lines[index] == ''
        and lines[index + 1] == ''
    ):
        del lines[index + 1]
        return -1
    return None


def clean_unicode_chars(lines, index):
    # usable characters over clever typographic characters
    replacements = {
        '\u0336': '—',  # "combining long stroke overlay" to em-dash
        '\u2212': '-',  # "minus sign" to hyphen
        '\u2013': '-',  # "en-dash" to hyphen
        '•': '-',       # bullet to hyphen
        '½': ' 1/2',    # vulgar fractions
        '⅓': ' 1/3',
        '¼': ' 1/4',
        '¾': ' 3/4',
        '⅔': ' 2/3',
        '⅕': ' 1/5',
        '⅖': ' 2/5',
        '⅗': ' 3/5',
        '⅘': ' 4/5',
        '⅙': ' 1/6',
        '⅚': ' 5/6',
        '⅐': ' 1/7',
        '⅛': ' 1/8',
        '⅜': ' 3/8',
        '⅝': ' 5/8',
        '⅞': ' 7/8',
    }

    for old, new in replacements.items():
        lines[index] = lines[index].replace(old, new)
    return 0


def clean_space_out_emdashes(lines, index):
    # "situations—particularly combat—the" -> "situations — particularly combat — the"
    # (visually distinct in a text editor, no hair space exists in Markdown)
    line = lines[index]
    if '—' in line:
        lines[index] = re.sub(r'(\w)—(\w)', r'\1 — \2', line)
    return 0


def clean_escape_square_brackets(lines, index):
    # "Blinded [Condition]" -> "Blinded \[Condition\]"
    lines[index] = re.sub(r'(?<!\\)\[', r'\\[', lines[index])
    lines[index] = re.sub(r'(?<!\\)\]', r'\\]', lines[index])
    return 0


def clean_table_alignment(lines, index):
    return realign_table(lines, index)


def clean_midsentence_pagebreak(lines, index):
    # rejoin paragraphs split by pagebreaks
    if lines[index] and lines[index][0].islower():
        previous = index - 1
        while previous >= 0 and lines[previous] == '':
            previous -= 1

        if previous >= 0 and lines[previous]:
            if (
                lines[previous][-1].islower()
                or lines[previous][-1] == ','
            ):
                lines[previous] = (
                    lines[previous] + ' ' + lines[index]
                )
                del lines[previous+1:index+1]
                return -(index - previous)
    return None


def clean_remove_mistaken_headers(lines, index):
    # "#### **Duration:** Instantaneous" -> "**Duration:** Instantaneous"
    removed = re.sub(
        r'^#+\s+((?:\*\*[^*]+\*\*\s+\S.*)|(?:\*[^*]+\*))$',
        r'\1',
        lines[index]
    )
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
    if not (lines[index].startswith('**') and ' **' in lines[index]):
        return None

    parts = re.split(r'\s+(?=\*\*[^*]+\*\*)', lines[index])
    lines[index] = parts[0].strip()

    for i, part in enumerate(parts[1:], 1):
        lines.insert(index + i, part.strip())

    return len(parts) - 1


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

        if current >= index:
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
    return _wrapup_matching_lines(
        lines,
        index,
        r'^(\*\*)?(Cantrips|At [Ww]ill|[0-9]+[a-z]* level|[0-9]+/[Dd]ay[^:]*):?',
        ''
    )


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
    potential_matches = re.findall(
        r'(?<![\*_])([\*_])(?!\*)([a-zA-Z][^*_]*?)\1(?!\*)',
        lines[index],
    )

    for marker, text in potential_matches:
        # grouped by first letter to speed up matching
        first_letter = text[0].lower()
        for names in [spell_list, magic_items]:
            if first_letter in names:
                for name in names[first_letter]:
                    # punctuation moves outside of the emphasis
                    pattern = (
                        re.escape(marker)
                        + re.escape(name.lower())
                        + r'([.,:;!?]*)'
                        + re.escape(marker)
                    )
                    replacement = f'_{name}_\\1'
                    lines[index] = re.sub(
                        pattern,
                        replacement,
                        lines[index],
                        flags=re.IGNORECASE
                    )

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
    lines[index] = re.sub(r'(?<!\\)(?<!\*)\*([^*]+)\*(?!\*)', r'_\1_', lines[index])
    return 0


def clean_collapse_adjacent_items(lines, index):
    # pull up adjacent "**Skills**" and "- List item"
    if (
        index + 2 < len(lines)
        and lines[index + 1] == ''
        and (
            (
                lines[index].startswith('**')
                and lines[index + 2].startswith('**')
                and not (
                    lines[index].endswith('.')
                    and not lines[index].endswith('ft.')
                )
            )
            or (
                lines[index].startswith('- ')
                and lines[index + 2].startswith('- ')
            )
        )
    ):
        del lines[index + 1]
        return -1
    return None


def clean_italic_to_bold_italic(lines, index):
    # "_Multiattack._ The dragon makes..." -> "_**Multiattack.**_ The dragon makes..."
    if match := re.match(r'^(_[A-Z][^_]*\._)(\s+\S.*)', lines[index]):
        emphasised = match.group(1)[1:-1]     # remove underscores
        lines[index] = f'_**{emphasised}**_{match.group(2)}'
        return 0
    return None


def clean_pluralise_component(lines, index):
    lines[index] = lines[index].replace('**Component:**', '**Components:**')
    return 0


def clean_bold_periods(lines, index):
    # "*Bite***.** *Melee Attack..." -> "*Bite.* *Melee Attack..."
    if '***.** ' in lines[index]:
        lines[index] = lines[index].replace('***.** ', '.* ')
        return 0
    return None


def clean_detabulate_mixed_stats(lines, index):
    # strip the mess of confused stats and ability scores table into a list,
    # (the ability scores will be converted back to a table in another filter)
    if not lines[index].startswith('|'):
        return None

    separator_index = index + 1
    if (
        separator_index >= len(lines)
        or not lines[separator_index].startswith('|-')
    ):
        return None

    table_rows = [lines[index]]
    current_index = separator_index + 1
    while current_index < len(lines) and lines[current_index].startswith('|'):
        table_rows.append(lines[current_index])
        current_index += 1

    abilities_pattern = r'\b(' + '|'.join(ABILITIES) + r')(\d)'
    table_text = ' '.join(table_rows)
    table_text = table_text.replace('|', ' ')
    table_text = re.sub(abilities_pattern, r'\1 \2', table_text)
    table_text = table_text.replace('MOD SAVE', '')
    table_text = re.sub(r'\s+', ' ', table_text).strip()
    words = table_text.split()

    properties_present = 0
    for prop in NUMERIC_PROPERTIES + PROPERTIES:
        if prop in words:
            prop_index = words.index(prop)
            if prop in NUMERIC_PROPERTIES:
                if (
                    prop_index + 1 < len(words)
                    and words[prop_index + 1][0] in MODIFIER_CHARS
                ):
                    properties_present += 1
            else:
                properties_present += 1

    abilities_present = len([
         ability for ability in ABILITIES
            if re.search(rf'\b{ability}\s', table_text)
    ])

    if not (abilities_present == 6 or properties_present >= 2):
        return None

    output_lines = []
    word_index = 0
    while word_index < len(words):
        word = words[word_index]
        matched = False

        for keyword in ALL_PROPERTIES:
            if word == keyword:
                matched = True
                parts = [word]
                word_index += 1

                if keyword in NUMERIC_PROPERTIES + PROPERTIES:
                    # "Skills Arcana +8, Athletics +14", "Speed 30 ft., Fly 60 ft."
                    # properties consume everything until next keyword
                    while (
                        word_index < len(words)
                        and words[word_index] not in (ALL_PROPERTIES)
                    ):
                        parts.append(words[word_index])
                        word_index += 1

                else:
                    # "Str 29 +9 +14" -- abilities consume numeric values
                    while (
                        word_index < len(words)
                        and words[word_index][0] in MODIFIER_CHARS
                    ):
                        parts.append(words[word_index])
                        word_index += 1

                content = ' '.join(parts[1:])
                output_lines.append(f'**{keyword}** {content}')
                break

        if not matched:
            word_index += 1

    lines[index:current_index] = output_lines
    return len(output_lines) - (current_index - index)


def clean_retabulate_ability_scores(lines, index):
    # **Str** 14 +2 +2 **Dex** ... -> | Str | 14 |...
    abilities_pattern = (
        r'^\*\*(' + '|'.join(ABILITIES) + r')\*\*\s+\d+\s+[+-]?\d+\s+[+-]?\d+'
    )
    if not re.match(abilities_pattern, lines[index]):
        return None

    scores = []
    mods = []
    saves = []
    current = index

    while current < len(lines):
        line = lines[current]
        if re.match(abilities_pattern, line):
            # "**Str** 19 +4 +4"
            parts = line.split()
            scores.append(parts[1])
            mods.append(parts[2])
            saves.append(parts[3])
            current += 1
        else:
            break
    if len(scores) != 6:
        return None

    # consume a trailing blank
    if current < len(lines) and lines[current] == '':
        current += 1

    # preserve a leading blank
    start = index
    if index > 0 and lines[index - 1] == '':
        start = index - 1

    lines_to_replace = current - start
    del lines[start:current]

    lines[start:start] = [
        '',
        '| | Str. | Dex. | Con. | Int. | Wis. | Cha. |',
        '|--|--|--|--|--|--|--|',
        f'| **Score** | {" | ".join(scores)} |',
        f'| **Modifier** | {" | ".join(mods)} |',
        f'| **Saving Throw** | {" | ".join(saves)} |',
        '',
    ]

    return 7 - lines_to_replace


def clean_reorder_stats(lines, index):
    # "**Speed** 30 ft." doesn't come first
    stat_order = NUMERIC_PROPERTIES[:4]
    if not any(lines[index].startswith(f'**{stat}**') for stat in stat_order):
        return None

    current = index
    while current < len(lines):
        if any(lines[current].startswith(f'**{stat}**') for stat in stat_order):
            current += 1
        elif (
            lines[current] == ''
            and current + 1 < len(lines)
            and any(lines[current + 1].startswith(f'**{stat}**') for stat in stat_order)
        ):
            current += 1
        else:
            break

    sorted_stats = sorted(
        [line for line in lines[index:current] if line],
        key=lambda s: next(
            (i for i, stat in enumerate(stat_order) if s.startswith(f'**{stat}**')),
            len(stat_order)
        )
    )

    lines[index:current] = sorted_stats
    return len(sorted_stats) - (current - index)


def clean_remove_mod_save(lines, index):
    # "**Speed** 30 ft. MOD SAVE MOD SAVE MOD SAVE" -> "**Speed** 30 ft."
    # "MOD SAVE MOD SAVE MOD SAVE **Str** 3 −4 −4" -> "**Str** 3 −4 −4"
    while 'MOD SAVE' in lines[index]:
        lines[index] = lines[index].replace('MOD SAVE', '', 1).strip()
        lines[index] = re.sub(r'\s+', ' ', lines[index])
    return 0


def clean_actions_emphasis(lines, index):
    # "*Name.* Description." -> "_**Name.**_ Description."
    pattern = r'^\*([^*]+)\*(.*)'
    match = re.match(pattern, lines[index])
    if not match:
        return None

    header = None
    for i in range(index - 1, -1, -1):
        if lines[i].startswith('#'):
            header = lines[i]
            break

    if not header or not any(
        title in header
            for title in ['Traits', 'Actions', 'Legendary Actions', 'Reactions']
    ):
        return None

    action_name = match.group(1)
    description = match.group(2)

    if action_name.startswith('Legendary Action Uses'):
        return None

    if '.' in action_name:
        parts = action_name.split('.', 1)
        ability_name = parts[0] + '.'
        additional_text = parts[1].strip() if parts[1].strip() else ''

        if additional_text:
            # "*Rend. Melee Attack Roll:* ..." -> "_**Rend.**_ *Melee Attack Roll:* ..."
            lines[index] = f'_**{ability_name}**_ *{additional_text}*{description}'
        else:
            # "*Amphibious.* ..." -> "_**Amphibious.**_ ..."
            lines[index] = f'_**{ability_name}**_{description}'
        return 0

    return None


def clean_spell_list_emphasis(lines, index):
    # "| Chill Touch | Necromancy |" -> "| *Chill Touch* | Necromancy |"
    if (
        not lines[index].startswith('|')
        or index < 2
    ):
        return None

    headers = get_table_headers(lines, index)
    if headers is None:
        return None

    columns = [
        i for i, header in enumerate(headers)
            if 'Spell' in header
    ]
    if not columns:
        return None

    cells = lines[index].split('|')
    for column in columns:
        cell_index = column + 1
        if len(cells) <= cell_index:
            continue
        cell_content = cells[cell_index].strip()
        if '*' not in cell_content and '_' not in cell_content:
            cells[cell_index] = spell_matcher.sub(r'*\1*', cell_content)
        else:
            cells[cell_index] = cell_content
    lines[index] = '|'.join(cells)
    return 0


def clean_decost_headers(lines, index):
    if match := re.match(r'^(#.*?)\s+\(([^)]*(?:[GCSEP]P|Free)[^)]*)\)$', lines[index]):
        lines[index] = match.group(1)
        if lines[index+2].startswith('**'):
            lines.insert(index+2, f"**Cost:** {match.group(2)}")
            return 1
        else:
            lines.insert(index+2, '')
            lines.insert(index+2, f"**Cost:** {match.group(2)}")
            return 2
    return None


def clean_srd(
    lines,
    breakdown_data,
    show_progress=False,
    clean_lines=None,
    profile=None,
):
    global spell_list, spell_matcher

    if profile:
        spell_list = get_spell_list(profile)
        spell_matcher = get_next_unemphasised_spell(spell_list)

    def _progress_bar(end):
        if show_progress:
            filled = int(round(min(index / len(lines), 1.0) * 100, 1) / 2)
            bar = (
                '█' * filled
                + '░' * (50 - filled)
            )
            print(f"- {cleaner.__name__:40} {index:6} [{bar}]", end=end)

    DND_51_CONVERSIONS_TABLE = [        # noqa: F841
        # common problems
        clean_whitespace,
        clean_wrap_blank_lines,
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
        clean_collapse_adjacent_items,

        # sanitation
        clean_canonicalise_proper_nouns,

        # markdown preferences
        clean_italic_emphasis_markers,
    ]

    CONVERSIONS_TABLE = [
        # basic cleanliness
        clean_whitespace,
        clean_unicode_chars,
        clean_midsentence_pagebreak,
        clean_pluralise_component,
        clean_space_out_emdashes,
        clean_escape_square_brackets,

        # clean marker_single formatting choices
        clean_remove_mistaken_headers,
        clean_remove_header_bold,
        clean_bold_periods,
        clean_actions_emphasis,

        # clean up after the *endless* table mistakes
        clean_remove_mod_save,
        clean_detabulate_mixed_stats,
        clean_unwrap_consecutive_bold,
        clean_reorder_stats,
        clean_collapse_adjacent_items,
        clean_retabulate_ability_scores,

        # probably 521 specific
        clean_decost_headers,
        clean_spell_list_emphasis,
        clean_statblock_spells_to_list,

        # final formatting pass
        clean_table_alignment,
        clean_italic_emphasis_markers,
        clean_italic_to_bold_italic,
        clean_collapse_adjacent_items,
        clean_wrap_blank_lines,
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

                if clean_lines and line in clean_lines:
                    continue

                result = cleaner(lines, index)
                if result is not None:
                    last_index = index + result
                    changes += 1
                    if result != 0:
                        if breakdown_data is not None:
                            update_breakdown_data(breakdown_data, index+1, result)
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


def warn_midparagraph_italics(lines, index):
    # look for mid-paragraph italics that could be a source wrapping error
    excluded = [
        "Player's Handbook.",
        "Hit:",

        # SRD 5.2.1
        "Miss:",
        "Hit or Miss:",
        "Choose A or B:",
        "Melee Attack Roll:",
        "Ranged Attack Roll:",
        "Melee or Ranged Attack Roll:",
        "Trigger:",
        "Response:",
        "Failure:",
        "Success:",
        "Successful Save:",
        "Failure or Success:",
        "First Failure:",
        "Second Failure:",
        "Additional Effects:",
        "Failed Save:",
    ]
    matches = re.findall(r'[\w.].*?_([A-Z][^_]*[:\.])_', lines[index])
    for match in matches:
        if (
            not match.startswith("**")
            and match not in excluded
            and not re.search(r'^(?:Response - )?\w+ Saving Throw:$', match)
        ):
            return f"possible mistaken mid-paragraph italic: '{match}'"
    return None


def warn_inconsistent_list_formatting(lines, index):
    # detect changes in list item emphasis formatting within a section
    if index == 0:
        return None

    emphasis = re.match(r'^- [_\*]+', lines[index])
    previous_emphasis = re.match(r'^- [_\*]+', lines[index-1])
    if (
        emphasis
        and previous_emphasis
        and emphasis.group() != previous_emphasis.group()
    ):
        return "inconsistent list formatting (emphasis type mismatch)"

    return None


def warn_table_after_header(lines, index):
    # table immediately after header might mean the header is part of the table
    if (
        index > 1
        and lines[index].startswith('|')
        and lines[index - 1] == ''
        and lines[index - 2].startswith('#')

        # ignore known tables
        and not re.search(r'Level \d+ \w+ Spells', lines[index - 2])
        and not re.search(r'Core \w+ Traits', lines[index - 2])
    ):
        return "table immediately after header"

    return None


def warn_bullet_characters(lines, index):
    bullets = [
        '•', '▪', '▫', '‣', '⁃', '◦', '∙',  # alternative bullet-like markers
        '‒', '–', '—', '―', '⁻', '−',       # other types of hyphens
    ]

    line = lines[index].lstrip()
    if line and any(line.startswith(char) for char in bullets):
        return "bullet (instead of Markdown list?)"
    return None


def warn_em_dash_spacing(lines, index):
    line = lines[index]
    if '—' in line:
        # Check for em-dash not surrounded by spaces
        for i, char in enumerate(line):
            if char == '—':
                has_space_before = i == 0 or line[i-1] == ' '
                has_space_after = i == len(line)-1 or line[i+1] == ' '
                if not (has_space_before and has_space_after):
                    return "em-dash not surrounded by spaces"
    return None


def warn_unusual_unicode(lines, index):
    # let's not be too clever
    unusual_chars = set()
    for char in lines[index]:
        if ord(char) >= 0x2070:
            unusual_chars.add(f"U+{ord(char):04X}")
    if unusual_chars:
        return f"unusual Unicode characters: {', '.join(sorted(unusual_chars))}"


def warn_empty_table_header(lines, index):
    # "|   | Bonus |  |  |" - likely has headers spread across lines
    if (
        lines[index].startswith('|')
        and index > 0
        and not lines[index - 1].startswith('|')
    ):
        cells = [cell.strip() for cell in lines[index].split('|')[1:-1]]
        if any(not cell for cell in cells):
            # ignore empty first cell on statblocks header
            if cells[0] == '' and all(
                f'{ability}.' in lines[index]
                    for ability in ABILITIES
            ):
                return None
            return "table has empty header cells"
    return None


def warn_empty_table_cells(lines, index):
    # "|data| |more data|" - empty cells in table rows
    if (
        lines[index].startswith('|')
        and index > 0
        and lines[index - 1].startswith('|')
    ):
        cells = [cell.strip() for cell in lines[index].split('|')[1:-1]]
        if not all(cell for cell in cells):
            return "table has empty data cells"
    return None


def warn_duration_length(lines, index):
    # "**Duration:** Concentration, up to 1 minute Squirming, ebony tentacles..."
    if lines[index].startswith('**Duration:**'):
        if len(lines[index].split()) > 6:
            return "duration has more than 5 words"
    return None


def warn_repeated_table_headers(lines, index):
    # "| Spell | Charge Cost | Spell | Charge Cost |"
    if (
        lines[index].startswith('|')
        and index > 0
        and not lines[index - 1].startswith('|')
    ):
        cells = [cell.strip() for cell in lines[index].split('|')[1:-1]]
        if len(cells) >= 2:
            seen = set()
            for cell in cells:
                if cell and cell in seen:
                    return f"table has repeated header: '{cell}'"
                if cell:
                    seen.add(cell)
    return None


def warn_srd(lines, ignore_file=None):
    WARN_TABLE = [
        warn_table_runon,
        warn_midparagraph_italics,
        warn_inconsistent_list_formatting,
        warn_table_after_header,
        warn_bullet_characters,
        warn_em_dash_spacing,
        warn_unusual_unicode,
        warn_empty_table_header,
        warn_empty_table_cells,
        warn_duration_length,
        warn_repeated_table_headers,
    ]

    ignore_patterns = []
    if ignore_file:
        try:
            with open(ignore_file, 'r', encoding='utf-8') as handle:
                ignore_patterns = [
                    line
                        for line in handle.read().splitlines()
                            if line
                ]
        except FileNotFoundError as e:
            print(f"Error '{e.filename}' not found")
            sys.exit(1)

    for index, line in enumerate(lines):
        for checker in WARN_TABLE:
            message = checker(lines, index)
            if message:
                context = 'file'
                for prev in range(index - 1, -1, -1):
                    if lines[prev].startswith('#'):
                        context = lines[prev]
                        break

                warning = f"Warning: {context}, {index + 1}: {message}"
                if not any(pattern in warning for pattern in ignore_patterns):
                    print(warning, file=sys.stderr)


def load_clean_lines(clean_lines_file):
    # lines already in the desired format which this script tries to alter
    clean_lines = []
    with open(clean_lines_file, 'r', encoding='utf-8') as handle:
        for line in handle:
            clean_lines.append(line.strip())
    return clean_lines


def load_breakdown_data(breakdown_file):
    breakdown_data = []
    with open(breakdown_file, 'r', encoding='utf-8') as handle:
        for line in handle:
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
            if entry[0] > change_line:
                entry[0] += adjustment
            if entry[1] >= change_line:
                entry[1] += adjustment


def write_breakdown_data(breakdown_file, breakdown_data):
    with open(breakdown_file, 'w', encoding='utf-8') as handle:
        for entry in breakdown_data:
            if isinstance(entry, list):
                handle.write(f"{entry[0]:>6} {entry[1]:>6}{entry[2]}\n")
            else:
                handle.write(f"{entry}\n")


def main():
    parser = argparse.ArgumentParser(description='Clean SRD markdown format')
    parser.add_argument(
        'markdown',
        help='Input markdown file',
    )
    parser.add_argument(
        'breakdown_file',
        nargs='?',
        help='Optional breakdown file to update',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print changes to stdout instead of modifying file',
    )
    parser.add_argument(
        '--warn',
        action='store_true',
        help='Only run warning checks, skip cleaning and error checks',
    )
    parser.add_argument(
        '--progress',
        action='store_true',
        help='Show progress through the file',
    )
    parser.add_argument(
        '--ignore-warnings',
        help='File containing patterns to ignore warnings',
    )
    parser.add_argument(
        '--clean-lines',
        help='File containing lines to skip during cleaning',
    )
    parser.add_argument(
        '--profile',
        default='dnd521',
        help='SRD profile to use (dnd51, dnd521)',
    )
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
            clean_lines = None
            if args.breakdown_file:
                breakdown_data = load_breakdown_data(args.breakdown_file)
            if args.clean_lines:
                clean_lines = load_clean_lines(args.clean_lines)

            cleaned = clean_srd(
                lines,
                breakdown_data,
                args.progress,
                clean_lines,
                args.profile,
            )

        warn_srd(lines, args.ignore_warnings)

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
