from textwrap import dedent
from clean_srd import clean_bold_periods
from . import TestFilter


class TestCleanBoldPeriods(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            _**Bite.**_ Melee Attack Roll: +11, reach 10 ft. Hit: 17 (2d10 + 6) Piercing damage.

            _**Claw.**_ Melee Attack Roll: +11, reach 5 ft. Hit: 13 (2d6 + 6) Slashing damage.
        """)

        assert text == self.run_text_through_filter(clean_bold_periods, text)

    def test_filtering(self):
        text = dedent("""\
            *Bite***.** *Melee Attack Roll:* +5, reach 5 ft. *Hit:* 7 (1d8 + 3) Piercing damage.

            *Claw***.** *Melee Attack Roll:* +5, reach 5 ft. *Hit:* 5 (1d4 + 3) Slashing damage. If the target is a Large or smaller creature, it has the Prone condition.
        """)
        expected = dedent("""\
            *Bite.* *Melee Attack Roll:* +5, reach 5 ft. *Hit:* 7 (1d8 + 3) Piercing damage.

            *Claw.* *Melee Attack Roll:* +5, reach 5 ft. *Hit:* 5 (1d4 + 3) Slashing damage. If the target is a Large or smaller creature, it has the Prone condition.
        """)

        assert expected == self.run_text_through_filter(clean_bold_periods, text)
