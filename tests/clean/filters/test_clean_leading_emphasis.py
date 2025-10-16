from textwrap import dedent
from clean_srd import clean_leading_emphasis
from . import TestFilter


class TestCleanLeadingEmphasis(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            #### **Actions**

            *Hooves. Melee Weapon Attack:* +6 to hit, reach 5 ft., one target. *Hit:* 13 (2d8 + 4) bludgeoning damage plus 7 (2d6) fire damage.
        """)

        assert text == self.run_text_through_filter(clean_leading_emphasis, text)

    def test_filtering(self):
        text = dedent("""\
            **Challenge** 3 (700 XP)

            *Confer Fire Resistance.* The nightmare can grant resistance to fire damage to anyone riding it.

            *Illumination.* The nightmare sheds bright light in a 10 foot radius and dim light for an additional 10 feet.

            *Using a Higher-Level Spell Slot.* If you cast this spell using a level 4 spell slot, you can maintain Concentration on it for up to 10 minutes. If you use a level 5+ spell slot, the spell doesn't require Concentration, and the duration becomes 8 hours (level 5–6 slot) or 24 hours (level 7–8 slot). If you use a level 9 spell slot, the spell lasts until dispelled.
        """)
        expected = dedent("""\
            **Challenge** 3 (700 XP)

            _**Confer Fire Resistance.**_ The nightmare can grant resistance to fire damage to anyone riding it.

            _**Illumination.**_ The nightmare sheds bright light in a 10 foot radius and dim light for an additional 10 feet.

            _**Using a Higher-Level Spell Slot.**_ If you cast this spell using a level 4 spell slot, you can maintain Concentration on it for up to 10 minutes. If you use a level 5+ spell slot, the spell doesn't require Concentration, and the duration becomes 8 hours (level 5–6 slot) or 24 hours (level 7–8 slot). If you use a level 9 spell slot, the spell lasts until dispelled.
        """)

        assert expected == self.run_text_through_filter(clean_leading_emphasis, text)
