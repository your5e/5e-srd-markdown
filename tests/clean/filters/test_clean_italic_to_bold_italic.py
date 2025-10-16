from textwrap import dedent
from clean_srd import clean_italic_to_bold_italic
from . import TestFilter


class TestCleanItalicToBoldItalic(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ### Legendary Actions

            _Legendary Action Uses: 3 (4 in Lair). Immediately after another creature's turn, the dragon can expend a use to take one of the following actions. The dragon regains all expended uses at the start of each of its turns._
        """)

        assert text == self.run_text_through_filter(clean_italic_to_bold_italic, text)

    def test_filtering(self):
        text = dedent("""\
            _Multiattack._ The dragon makes three attacks: one with its bite and two with its claws.

            _Bite._ Melee Attack Roll: +11, reach 10 ft. Hit: 17 (2d10 + 6) Piercing damage.

            _Legendary Resistance (3/Day)._ If the dragon fails a saving throw, it can choose to succeed instead.

            _Magic Resistance._ The dragon has advantage on saving throws against spells and other magical effects.
        """)
        expected = dedent("""\
            _**Multiattack.**_ The dragon makes three attacks: one with its bite and two with its claws.

            _**Bite.**_ Melee Attack Roll: +11, reach 10 ft. Hit: 17 (2d10 + 6) Piercing damage.

            _**Legendary Resistance (3/Day).**_ If the dragon fails a saving throw, it can choose to succeed instead.

            _**Magic Resistance.**_ The dragon has advantage on saving throws against spells and other magical effects.
        """)

        assert expected == self.run_text_through_filter(clean_italic_to_bold_italic, text)
