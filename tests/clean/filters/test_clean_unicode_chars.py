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
        """)

        assert text == self.run_text_through_filter(clean_unicode_chars, text)

    def test_filtering_dashes(self):
        text = dedent("""\
            | Score | Modifier | Score | Modifier |
            |-------|----------|-------|----------|
            | 1     | −5       | 16–17 | +3       |
            | 2–3   | −4       | 18–19 | +4       |
            | 4–5   | −3       | 20–21 | +5       |
            | 6–7   | −2       | 22–23 | +6       |
            | 8–9   | −1       | 24–25 | +7       |
            | 10–11 | +0       | 26–27 | +8       |
        """)
        expected = dedent("""\
            | Score | Modifier | Score | Modifier |
            |-------|----------|-------|----------|
            | 1     | -5       | 16–17 | +3       |
            | 2–3   | -4       | 18–19 | +4       |
            | 4–5   | -3       | 20–21 | +5       |
            | 6–7   | -2       | 22–23 | +6       |
            | 8–9   | -1       | 24–25 | +7       |
            | 10–11 | +0       | 26–27 | +8       |
        """)

        assert expected == self.run_text_through_filter(clean_unicode_chars, text)

    def test_combining_long_stroke_overlay(self):
        text = dedent("""\
            | Level | Bonus       | Features                                                | Known    | Known  | 1st                           | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th |
            | 1st   | +2          | Spellcasting,	Bardic	Inspiration<br>(d6)                | 2        | 4      | 2                             | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   |
            | 2nd   | +2          | Jack	of	All	Trades,	Song	of	Rest<br>(d6)                | 2        | 5      | 3                             | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   | ̶   |
        """)
        expected = dedent("""\
            | Level | Bonus       | Features                                                | Known    | Known  | 1st                           | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th |
            | 1st   | +2          | Spellcasting,	Bardic	Inspiration<br>(d6)                | 2        | 4      | 2                             | —   | —   | —   | —   | —   | —   | —   | —   |
            | 2nd   | +2          | Jack	of	All	Trades,	Song	of	Rest<br>(d6)                | 2        | 5      | 3                             | —   | —   | —   | —   | —   | —   | —   | —   |
        """)

        assert expected == self.run_text_through_filter(clean_unicode_chars, text)
