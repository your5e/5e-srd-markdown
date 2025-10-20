from textwrap import dedent
from clean_srd import warn_table_after_header
from . import TestFilter


class TestWarnTableAfterHeader(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            **Creating Spell Slots**

            |   Spell Slot Level |   Sorcery Point Cost |   Min. Sorcerer Level |
            |--------------------|----------------------|-----------------------|
            |                  1 |                    2 |                     2 |
            |                  2 |                    3 |                     3 |
            |                  3 |                    5 |                     5 |
            |                  4 |                    6 |                     7 |
            |                  5 |                    7 |                     9 |
        """)

        assert not self.check_text_for_warning(warn_table_after_header, text)

    def test_warning(self):
        text = dedent("""\
            ##### Creating Spell Slots

            |   Spell Slot Level |   Sorcery Point Cost |   Min. Sorcerer Level |
            |--------------------|----------------------|-----------------------|
            |                  1 |                    2 |                     2 |
            |                  2 |                    3 |                     3 |
            |                  3 |                    5 |                     5 |
            |                  4 |                    6 |                     7 |
            |                  5 |                    7 |                     9 |
        """)

        assert self.check_text_for_warning(warn_table_after_header, text)
