from textwrap import dedent
from clean_srd import warn_inconsistent_list_formatting
from . import TestFilter


class TestWarnInconsistentListFormatting(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            - **Immunities** Lightning, Thunder
            - **Senses** Darkvision 120 ft.; Passive Perception 13
            - **Languages** Primordial (Auran)
            - **CR** 11 (XP 7,200; PB +4)
        """)

        assert not self.check_text_for_warning(warn_inconsistent_list_formatting, text)

    def test_warning(self):
        text = dedent("""\
            - **Immunities** Lightning, Thunder
            - *Senses* Darkvision 120 ft.; Passive Perception 13
            - **Languages** Primordial (Auran)
            - **CR** 11 (XP 7,200; PB +4)
        """)

        assert self.check_text_for_warning(warn_inconsistent_list_formatting, text)
