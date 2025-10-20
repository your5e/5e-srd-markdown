from textwrap import dedent
from clean_srd import warn_empty_table_header
from . import TestFilter


class TestWarnEmptyTableHeader(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            |                  |   Str. |   Dex. |   Con. |   Int. |   Wis. |   Cha. |
            |------------------|--------|--------|--------|--------|--------|--------|
            | **Score**        |     21 |     15 |     22 |     15 |     16 |     20 |
            | **Modifier**     |     +5 |     +2 |     +6 |     +2 |     +3 |     +5 |
            | **Saving Throw** |     +5 |     +6 |     +6 |     +2 |     +7 |     +5 |
        """)

        assert not self.check_text_for_warning(warn_empty_table_header, text)

    def test_warning(self):
        text = dedent("""\
            |        |   |    | MOD SAVE |          |    | MOD SAVE |          |    | MOD SAVE |
            |--------|---|----|----------|----------|----|----------|----------|----|----------|
            | Str 16 |   | +3 | +3       | Dex 10   | +0 | +0       | Con 10   | +0 | +0       |
            | Int    | 3 | −4 | −4       | Wis<br>3 | −4 | −4       | Cha<br>1 | −5 | −5       |
        """)

        assert self.check_text_for_warning(warn_empty_table_header, text)
