from textwrap import dedent
from clean_srd import clean_unicode_chars
from . import TestFilter


class TestCleanUnicodeChars(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            | Score | Modifier | Score | Modifier |
            |-------|----------|-------|----------|
            | 10-11 | +0       | 26-27 | +8       |
            | 12-13 | +1       | 28-29 | +9       |

            A saving throw — also called a save — represents an attempt to avoid or resist a threat. You normally make a saving throw only when a rule requires you to do so, but you can decide to fail the save without rolling. The result of a save is detailed in the effect that allowed it. If a target is forced to make a save and lacks the ability score used by it, the target automatically fails. _See also_ "Playing the Game" ("D20 Tests").
        """)

        assert text == self.run_text_through_filter(clean_unicode_chars, text)

    def test_filtering(self):
        text = dedent("""\
            | Score | Modifier | Score | Modifier |
            |-------|----------|-------|----------|
            | 1     | −5       | 16–17 | +3       |
            | 2–3   | −4       | 18–19 | +4       |
            | 4–5   | −3       | 20–21 | +5       |
            | 6–7   | −2       | 22–23 | +6       |
            | 8–9   | −1       | 24–25 | +7       |
            | 10–11 | +0       | 26–27 | +8       |

            | Level | Bonus       | Features                                                | Known    | Known  | 1st                           | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th |
            | 1st   | +2          | Spellcasting,   Bardic  Inspiration<br>(d6)                | 2        | 4      | 2                             | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   |
            | 2nd   | +2          | Jack    of  All Trades, Song    of  Rest<br>(d6)                | 2        | 5      | 3                             | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   |

            • If you deal damage to the target with an attack roll or a spell, the target takes an extra 1d8 Necrotic damage.

            | Monster Size | Hit Die | Average HP per Die |
            |--------------|---------|--------------------|
            | Tiny         | d4      | 2½                 |
            | Small        | d6      | 3½                 |
            | Medium       | d8      | 4½                 |
            | Large        | d10     | 5½                 |
            | Huge         | d12     | 6½                 |
            | Gargantuan   | d20     | 10½                |
        """)
        expected = dedent("""\
            | Score | Modifier | Score | Modifier |
            |-------|----------|-------|----------|
            | 1     | -5       | 16-17 | +3       |
            | 2-3   | -4       | 18-19 | +4       |
            | 4-5   | -3       | 20-21 | +5       |
            | 6-7   | -2       | 22-23 | +6       |
            | 8-9   | -1       | 24-25 | +7       |
            | 10-11 | +0       | 26-27 | +8       |

            | Level | Bonus       | Features                                                | Known    | Known  | 1st                           | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th |
            | 1st   | +2          | Spellcasting,   Bardic  Inspiration<br>(d6)                | 2        | 4      | 2                             | —   | —   | —   | —   | —   | —   | —   | —   |
            | 2nd   | +2          | Jack    of  All Trades, Song    of  Rest<br>(d6)                | 2        | 5      | 3                             | —   | —   | —   | —   | —   | —   | —   | —   |

            - If you deal damage to the target with an attack roll or a spell, the target takes an extra 1d8 Necrotic damage.

            | Monster Size | Hit Die | Average HP per Die |
            |--------------|---------|--------------------|
            | Tiny         | d4      | 2 1/2                 |
            | Small        | d6      | 3 1/2                 |
            | Medium       | d8      | 4 1/2                 |
            | Large        | d10     | 5 1/2                 |
            | Huge         | d12     | 6 1/2                 |
            | Gargantuan   | d20     | 10 1/2                |
        """)

        assert expected == self.run_text_through_filter(clean_unicode_chars, text)
        assert expected == self.run_text_through_filter(clean_unicode_chars, expected)
