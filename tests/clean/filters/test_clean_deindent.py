from textwrap import dedent
from clean_srd import clean_deindent
from . import TestFilter


class TestCleanDeindent(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            - **Saving Throws** Wis +9, Cha +9
            - **Skills** Insight +9, Perception +9
            - **Damage Resistances** radiant; bludgeoning, piercing, and slashing from nonmagical attacks
            - **Condition Immunities** charmed, exhaustion, frightened
            - **Senses** darkvision 120 ft., passive Perception 19
            - **Languages** all, telepathy 120 ft.
            - **Challenge** 10 (5,900 XP)
        """)

        assert text == self.run_text_through_filter(clean_deindent, text)

    def test_filtering(self):
        text = dedent("""\
            # Dragonborn
            _**Breath Weapon.**_ You can use your action to exhale destructive energy. Your draconic ancestry determines the size, shape, and damage type of the exhalation.

                When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.

                After you use your breath weapon, you can't use it again until you complete a short or long rest.

            _**Damage Resistance.**_ You have resistance to the damage type associated with your draconic ancestry.

            # Deva
            - _**Innate Spellcasting.**_ The deva's spellcasting ability is Charisma (spell save DC 17). The deva can innately cast the following spells, requiring only verbal components:

                - At will: _Detect Evil and Good_
                - 1/day each: _Commune_, _Raise Dead_

            - _**Magic Resistance.**_ The deva has advantage on saving throws against spells and other magical effects.
        """)
        expected = dedent("""\
            # Dragonborn
            _**Breath Weapon.**_ You can use your action to exhale destructive energy. Your draconic ancestry determines the size, shape, and damage type of the exhalation.

            When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.

            After you use your breath weapon, you can't use it again until you complete a short or long rest.

            _**Damage Resistance.**_ You have resistance to the damage type associated with your draconic ancestry.

            # Deva
            - _**Innate Spellcasting.**_ The deva's spellcasting ability is Charisma (spell save DC 17). The deva can innately cast the following spells, requiring only verbal components:

            - At will: _Detect Evil and Good_
            - 1/day each: _Commune_, _Raise Dead_

            - _**Magic Resistance.**_ The deva has advantage on saving throws against spells and other magical effects.
        """)

        assert expected == self.run_text_through_filter(clean_deindent, text)
        assert expected == self.run_text_through_filter(clean_deindent, expected)
