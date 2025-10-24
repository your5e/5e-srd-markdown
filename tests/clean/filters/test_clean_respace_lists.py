from textwrap import dedent
from clean_srd import clean_respace_lists
from . import TestFilter


class TestCleanDeindentLists(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\

            - **Saving Throws** Dex +7, Con +16, Wis +9, Cha +13
            - **Skills** Arcana +11, History +11, Perception +16, Stealth +7
            - **Damage Immunities** cold
            - **Senses** blindsight 60 ft., darkvision 120 ft., passive Perception 26
            - **Languages** Common, Draconic
            - **Challenge** 23 (50,000 XP)

        """)

        assert text == self.run_text_through_filter(clean_respace_lists, text)

    def test_filtering(self):
        text = dedent("""\
            - _**Breath Weapons (Recharge 5–6).**_ The dragon uses one of the following breath weapons.
                - **Cold Breath.** The dragon exhales an icy blast in a 90 foot cone. Each creature in that area must make a DC 24 Constitution saving throw, taking 67 (15d8) cold damage on a failed save, or half as much damage on a successful one.
                - **Paralyzing Breath.** The dragon exhales paralyzing gas in a 90-foot cone. Each creature in that area must succeed on a DC 24 Constitution saving throw or be paralyzed for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.
            - _**Change Shape.**_ The dragon magically polymorphs into a humanoid or beast that has a challenge rating no higher than its own, or back into its true form. It reverts to its true form if it dies. Any equipment it is wearing or carrying is absorbed or borne by the new form (the dragon's choice).
            - _**Breath Weapons (Recharge 5–6).**_ The dragon uses one of the following breath weapons.
                - **Fire Breath.** The dragon exhales fire in a 30-foot cone. Each creature in that area must make a DC 17 Dexterity saving throw, taking 55 (10d10) fire damage on a failed save, or half as much damage on a successful one.
                - **Weakening Breath.** The dragon exhales gas in a 30-foot cone. Each creature in that area must succeed on a DC 17 Strength saving throw or have disadvantage on Strength-based attack rolls, Strength checks, and Strength saving throws for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.

        """)
        expected = dedent("""\
            - _**Breath Weapons (Recharge 5–6).**_ The dragon uses one of the following breath weapons.

                - **Cold Breath.** The dragon exhales an icy blast in a 90 foot cone. Each creature in that area must make a DC 24 Constitution saving throw, taking 67 (15d8) cold damage on a failed save, or half as much damage on a successful one.
                - **Paralyzing Breath.** The dragon exhales paralyzing gas in a 90-foot cone. Each creature in that area must succeed on a DC 24 Constitution saving throw or be paralyzed for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.

            - _**Change Shape.**_ The dragon magically polymorphs into a humanoid or beast that has a challenge rating no higher than its own, or back into its true form. It reverts to its true form if it dies. Any equipment it is wearing or carrying is absorbed or borne by the new form (the dragon's choice).
            - _**Breath Weapons (Recharge 5–6).**_ The dragon uses one of the following breath weapons.

                - **Fire Breath.** The dragon exhales fire in a 30-foot cone. Each creature in that area must make a DC 17 Dexterity saving throw, taking 55 (10d10) fire damage on a failed save, or half as much damage on a successful one.
                - **Weakening Breath.** The dragon exhales gas in a 30-foot cone. Each creature in that area must succeed on a DC 17 Strength saving throw or have disadvantage on Strength-based attack rolls, Strength checks, and Strength saving throws for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.

        """)

        assert expected == self.run_text_through_filter(clean_respace_lists, text)
        assert expected == self.run_text_through_filter(clean_respace_lists, expected)
