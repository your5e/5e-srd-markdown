from textwrap import dedent
from clean_srd import warn_empty_table_cells
from . import TestFilter


class TestWarnEmptyTableCells(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            | Item                   | Weight       | Cost     |
            |------------------------|--------------|----------|
            | Acid                   | 1 lb.        | 25 GP    |
            | Alchemist's Fire       | 1 lb.        | 50 GP    |
            | Ammunition             | Varies       | Varies   |
            | Antitoxin              | —            | 50 GP    |
            | Arcane Focus           | Varies       | Varies   |
            | Backpack               | 5 lb.        | 2 GP     |
            | Ball Bearings          | 2 lb.        | 1 GP     |
        """)

        assert not self.check_text_for_warning(warn_empty_table_cells, text)

    def test_warning(self):
        text = dedent("""\
            | Item                   | Weight       | Cost     |
            |------------------------|--------------|----------|
            | Acid                   | 1 lb.        | 25 GP    |
            | Alchemist's Fire       | 1 lb.        | 50 GP    |
            | Ammunition             | Varies       | Varies   |
            | Antitoxin              |              | 50 GP    |
            | Arcane Focus           | Varies       | Varies   |
            | Backpack               | 5 lb.        | 2 GP     |
            | Ball Bearings          | 2 lb.        | 1 GP     |
        """)

        assert self.check_text_for_warning(warn_empty_table_cells, text)
