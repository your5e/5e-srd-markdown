from textwrap import dedent
from clean_srd import clean_delistify_actions
from . import TestFilter


class TestCleanDelistifyActions(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            #### Magic Missile

            _1st-level evocation_

            - **Casting Time:** 1 action
            - **Range:** 120 feet
            - **Components:** V, S
            - **Duration:** Instantaneous
        """)

        assert text == self.run_text_through_filter(clean_delistify_actions, text)

    def test_filtering(self):
        text = dedent("""\
            ### High Elf

            As a high elf, you have a keen mind and a mastery of at least the basics of magic. In many fantasy gaming worlds, there are two kinds of high elves. One type is haughty and reclusive, believing themselves to be superior to non-elves and even other elves. The other type is more common and more friendly, and often encountered among humans and other races.

            - _**Ability Score Increase.**_ Your Intelligence score increases by 1.
            - _**Elf Weapon Training.**_ You have proficiency with the longsword, shortsword, shortbow, and longbow.
            - _**Cantrip.**_ You know one cantrip of your choice from the wizard spell list. Intelligence is your spellcasting ability for it.
            - _**Extra Language.**_ You can speak, read, and write one extra language of your choice.

            ### Vrock

            #### Traits

            - _**Magic Resistance.**_ The vrock has advantage on saving throws against spells and other magical effects.

            #### Actions

            - _**Multiattack.**_ The vrock makes two attacks: one with its beak and one with its talons.
            - _**Beak.** Melee Weapon Attack:_ +6 to hit, reach 5 ft., one target. _Hit:_ 10 (2d6 + 3) piercing damage.
            - _**Talons.** Melee Weapon Attack:_ +6 to hit, reach 5 ft., one target. _Hit:_ 14 (2d10 + 3) slashing damage.
            - _**Spores (Recharge 6).**_ A 15-foot-radius cloud of toxic spores extends out from the vrock. The spores spread around corners. Each creature in that area must succeed on a DC 14 Constitution saving throw or become poisoned. While poisoned in this way, a target takes 5 (1d10) poison damage at the start of each of its turns. A target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. Emptying a vial of holy water on the target also ends the effect on it.
            - _**Stunning Screech (1/Day).**_ The vrock emits a horrific screech. Each creature within 20 feet of it that can hear it and that isn't a demon must succeed on a DC 14 Constitution saving throw or be stunned until the end of the vrock's next turn.
        """)
        expected = dedent("""\
            ### High Elf

            As a high elf, you have a keen mind and a mastery of at least the basics of magic. In many fantasy gaming worlds, there are two kinds of high elves. One type is haughty and reclusive, believing themselves to be superior to non-elves and even other elves. The other type is more common and more friendly, and often encountered among humans and other races.

            _**Ability Score Increase.**_ Your Intelligence score increases by 1.

            _**Elf Weapon Training.**_ You have proficiency with the longsword, shortsword, shortbow, and longbow.

            _**Cantrip.**_ You know one cantrip of your choice from the wizard spell list. Intelligence is your spellcasting ability for it.

            _**Extra Language.**_ You can speak, read, and write one extra language of your choice.

            ### Vrock

            #### Traits

            _**Magic Resistance.**_ The vrock has advantage on saving throws against spells and other magical effects.

            #### Actions

            _**Multiattack.**_ The vrock makes two attacks: one with its beak and one with its talons.

            _**Beak.** Melee Weapon Attack:_ +6 to hit, reach 5 ft., one target. _Hit:_ 10 (2d6 + 3) piercing damage.

            _**Talons.** Melee Weapon Attack:_ +6 to hit, reach 5 ft., one target. _Hit:_ 14 (2d10 + 3) slashing damage.

            _**Spores (Recharge 6).**_ A 15-foot-radius cloud of toxic spores extends out from the vrock. The spores spread around corners. Each creature in that area must succeed on a DC 14 Constitution saving throw or become poisoned. While poisoned in this way, a target takes 5 (1d10) poison damage at the start of each of its turns. A target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. Emptying a vial of holy water on the target also ends the effect on it.

            _**Stunning Screech (1/Day).**_ The vrock emits a horrific screech. Each creature within 20 feet of it that can hear it and that isn't a demon must succeed on a DC 14 Constitution saving throw or be stunned until the end of the vrock's next turn.
        """)

        assert expected == self.run_text_through_filter(clean_delistify_actions, text)
        assert expected == self.run_text_through_filter(clean_delistify_actions, expected)
