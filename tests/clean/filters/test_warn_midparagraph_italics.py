from textwrap import dedent
from clean_srd import warn_midparagraph_italics
from . import TestFilter


class TestWarnMidparagraphItalics(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            Whenever the whirlwind enters a creature's space or a creature enters the whirlwind, that creature is subjected to the following effect. _Strength Saving Throw:_ DC 17 (a creature makes this save only once per turn, and the djinni is unaffected). _Failure:_ While in the whirlwind, the target has the Restrained condition and moves with the whirlwind. At the start of each of its turns, the Restrained target takes 21 (6d6) Thunder damage. At the end of each of its turns, the target repeats the save, ending the effect on itself on a success.
        """)

        assert not self.check_text_for_warning(warn_midparagraph_italics, text)

    def test_warning(self):
        text = dedent("""\
            _**Bite.**_ _Melee Attack Roll:_ +4, reach 5 ft. _Hit:_ 4 (1d4 + 2) Piercing damage. If the target is a creature, it is subjected to the following effect. _Constitution Saving Throw:_ DC 12. _First Failure:_ The target has the Poisoned condition. While Poisoned, the target's Hit Point maximum doesn't return to normal when finishing a Long Rest, and it repeats the save every 24 hours that elapse, ending the effect on itself on a success. _Subsequent Failures:_ The Poisoned target's Hit Point maximum decreases by 5 (1d10).
        """)

        assert self.check_text_for_warning(warn_midparagraph_italics, text)
