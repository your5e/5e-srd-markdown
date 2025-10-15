from textwrap import dedent
from clean_srd import clean_split_lists
from . import TestFilter


class TestCleanSplitLists(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ## **Hit Points**

            - **Hit Dice:** 1d8 per bard level
            - **Hit Points at 1st Level:** 8 + your Constitution modifier
            - **Hit Points at Higher Levels:** 1d8 (or 5) + your Constitution modifier per bard level after 1st
        """)

        assert text == self.run_text_through_filter(clean_split_lists, text)

    def test_filtering(self):
        text = dedent("""\
            ### Water Elemental

            _Large elemental, neutral_

            - **Armor** Class 14 (natural armor)

            - **Hit Points** 114 (12d10 + 48)

            - **Speed** 30 ft., swim 90 ft.
        """)
        expected = dedent("""\
            ### Water Elemental

            _Large elemental, neutral_

            - **Armor** Class 14 (natural armor)
            - **Hit Points** 114 (12d10 + 48)
            - **Speed** 30 ft., swim 90 ft.
        """)

        assert expected == self.run_text_through_filter(clean_split_lists, text)
