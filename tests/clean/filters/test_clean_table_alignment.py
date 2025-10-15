from textwrap import dedent
from clean_srd import clean_table_alignment
from . import TestFilter


class TestCleanTableAlignment(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            General rules govern each part of the game. For example, the combat rules tell you that melee attacks use Strength and ranged attacks use Dexterity. That's a general rule, and a general rule is in effect as long as something in the game doesn't explicitly say otherwise.

            The game also includes elements—class features, feats, weapon properties, spells, magic items, monster abilities, and the like—that sometimes contradict a general rule. When an exception and a general rule disagree, the exception wins. For example, if a feature says you can make melee attacks using your Charisma, you can do so, even though that statement disagrees with the general rule.
        """)

        assert text == self.run_text_through_filter(clean_table_alignment, text)

    def test_filtering(self):
        text = dedent("""\
            |       | Proficiency |                             |
            |-------|-------------|-----------------------------|
            | Level | Bonus       | Features                    |
            | 1st   | +2          | Fighting    Style,  Second  Wind |
            | 2nd   | +2          | Action  Surge   (one    use)      |
            | 3rd   | +2          | Martial Archetype           |
        """)
        expected = dedent("""\
            |       | Proficiency   |                             |
            |-------|---------------|-----------------------------|
            | Level | Bonus         | Features                    |
            | 1st   | +2            | Fighting Style, Second Wind |
            | 2nd   | +2            | Action Surge (one use)      |
            | 3rd   | +2            | Martial Archetype           |
        """)

        assert expected == self.run_text_through_filter(clean_table_alignment, text)
