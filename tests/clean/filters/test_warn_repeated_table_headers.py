from textwrap import dedent
from clean_srd import warn_repeated_table_headers
from . import TestFilter


class TestWarnRepeatedTableHeaders(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            | Dragon   | Damage Type   |
            |----------|---------------|
            | Black    | Acid          |
            | Blue     | Lightning     |
            | Brass    | Fire          |
            | Bronze   | Lightning     |
            | Copper   | Acid          |
            | Gold     | Fire          |
            | Green    | Poison        |
            | Red      | Fire          |
            | Silver   | Cold          |
            | White    | Cold          |
        """)

        assert not self.check_text_for_warning(warn_repeated_table_headers, text)

    def test_warning(self):
        text = dedent("""\
            | Dragon | Damage Type | Dragon | Damage Type |
            |--------|-------------|--------|-------------|
            | Black  | Acid        | Gold   | Fire        |
            | Blue   | Lightning   | Green  | Poison      |
            | Brass  | Fire        | Red    | Fire        |
            | Bronze | Lightning   | Silver | Cold        |
            | Copper | Acid        | White  | Cold        |
        """)

        assert self.check_text_for_warning(warn_repeated_table_headers, text)
