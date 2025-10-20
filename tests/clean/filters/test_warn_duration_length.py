from textwrap import dedent
from clean_srd import warn_duration_length
from . import TestFilter


class TestWarnDurationLength(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            ### Spirit Guardians

            _Level 3 Conjuration (Cleric)_

            - **Casting Time:** Action
            - **Range:** Self
            - **Components:** V, S, M (a prayer scroll)
            - **Duration:** Concentration, up to 10 minutes

            Protective spirits flit around you in a 15-foot Emanation for the duration. If you are good or neutral, their spectral form appears angelic or fey (your choice). If you are evil, they appear fiendish.
        """)

        assert not self.check_text_for_warning(warn_duration_length, text)

    def test_warning(self):
        text = dedent("""\
            #### Fire-Casting Statue

            _Deadly Trap (Levels 1-4)_

            - **Trigger:** A creature moves onto a pressure plate
            - **Duration:** Instantaneous, and the trap resets at the start of the next turn
        """)

        assert self.check_text_for_warning(warn_duration_length, text)
