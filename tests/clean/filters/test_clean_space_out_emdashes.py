from textwrap import dedent
from clean_srd import clean_space_out_emdashes
from . import TestFilter


class TestCleanSpaceOutEmdashes(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            The three main pillars of D&D play are social interaction, exploration, and combat. Whichever one you're experiencing, the game unfolds according to this basic pattern:
        """)

        assert text == self.run_text_through_filter(clean_space_out_emdashes, text)

    def test_filtering(self):
        text = dedent("""\
            This pattern holds during every game session (each time you sit down to play D&D), whether the adventurers are talking to a noble, exploring a ruin, or fighting a dragon. In certain situations—particularly combat—the action is more structured, and everyone takes turns.
        """)
        expected = dedent("""\
            This pattern holds during every game session (each time you sit down to play D&D), whether the adventurers are talking to a noble, exploring a ruin, or fighting a dragon. In certain situations — particularly combat — the action is more structured, and everyone takes turns.
        """)

        assert expected == self.run_text_through_filter(clean_space_out_emdashes, text)
        assert expected == self.run_text_through_filter(clean_space_out_emdashes, expected)
