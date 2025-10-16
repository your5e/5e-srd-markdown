from textwrap import dedent
from clean_srd import clean_reorder_stats
from . import TestFilter


class TestCleanReorderStats(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            **AC** 16
            **Initiative** +10 (20)
            **HP** 97 (15d8 + 30)
            **Speed** 30 ft.
        """)

        assert text == self.run_text_through_filter(clean_reorder_stats, text)

    def test_filtering(self):
        text = dedent("""\
            **HP** 27 (5d10)
            **Speed** 10 ft.

            **AC** 12
            **Initiative** +4 (14)

            |        |   | MOD SAVE |    |          |    | MOD SAVE |        | MOD SAVE |    |
        """)
        expected = dedent("""\
            **AC** 12
            **Initiative** +4 (14)
            **HP** 27 (5d10)
            **Speed** 10 ft.

            |        |   | MOD SAVE |    |          |    | MOD SAVE |        | MOD SAVE |    |
        """)

        assert expected == self.run_text_through_filter(clean_reorder_stats, text)
