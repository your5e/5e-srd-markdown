from textwrap import dedent
from clean_srd import clean_actions_emphasis
from . import TestFilter


class TestCleanActionsEmphasis(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ### Actions

            _**Bite.**_ Melee Attack Roll: +11, reach 10 ft.

            Some *emphasized text* in description.
        """)

        assert text == self.run_text_through_filter(clean_actions_emphasis, text)

    def test_filtering(self):
        text = dedent("""\
            # Traits

            *Amphibious.* The dragon can breathe air and water.

            *Legendary Resistance (4/Day, or 5/Day in Lair).* If the dragon fails a saving throw, it can choose to succeed instead.

            # Actions

            *Multiattack.* The dragon makes three Rend attacks. It can replace one attack with a use of Spellcasting to cast *Acid Arrow* (level 4 version).

            *Rend. Melee Attack Roll:* +15, reach 15 ft. *Hit:* 17 (2d8 + 8) Slashing damage plus 9 (2d8) Acid damage.

            *Acid Breath (Recharge 5–6). Dexterity Saving Throw:* DC 22, each creature in a 90-foot-long, 10-footwide Line. *Failure:* 67 (15d8) Acid damage. *Success:* Half damage.

            *Spellcasting.* The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save DC 21, +13 to hit with spell attacks):

            **At Will:** *Acid Arrow* (level 4 version), *Detect Magic*, *Fear*

            **1/Day Each:** *Create Undead*, *Speak with Dead*, *Vitriolic Sphere* (level 5 version)

            # Legendary Actions

            *Legendary Action Uses: 3 (4 in Lair). Immediately after another creature's turn, the dragon can expend a use to take one of the following actions. The dragon regains all expended uses at the start of each of its turns.*

            *Cloud of Insects. Dexterity Saving Throw:* DC 21, one creature the dragon can see within 120 feet. *Failure:* 33 (6d10) Poison damage, and the target has Disadvantage on saving throws to maintain Concentration until the end of its next turn. *Failure or Success:* The dragon can't take this action again until the start of its next turn.

            *Frightful Presence.* The dragon uses Spellcasting to cast *Fear*. The dragon can't take this action again until the start of its next turn.

            *Pounce.* The dragon moves up to half its Speed, and it makes one Rend attack.

        """)
        expected = dedent("""\
            # Traits

            _**Amphibious.**_ The dragon can breathe air and water.

            _**Legendary Resistance (4/Day, or 5/Day in Lair).**_ If the dragon fails a saving throw, it can choose to succeed instead.

            # Actions

            _**Multiattack.**_ The dragon makes three Rend attacks. It can replace one attack with a use of Spellcasting to cast *Acid Arrow* (level 4 version).

            _**Rend.**_ *Melee Attack Roll:* +15, reach 15 ft. *Hit:* 17 (2d8 + 8) Slashing damage plus 9 (2d8) Acid damage.

            _**Acid Breath (Recharge 5–6).**_ *Dexterity Saving Throw:* DC 22, each creature in a 90-foot-long, 10-footwide Line. *Failure:* 67 (15d8) Acid damage. *Success:* Half damage.

            _**Spellcasting.**_ The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save DC 21, +13 to hit with spell attacks):

            **At Will:** *Acid Arrow* (level 4 version), *Detect Magic*, *Fear*

            **1/Day Each:** *Create Undead*, *Speak with Dead*, *Vitriolic Sphere* (level 5 version)

            # Legendary Actions

            *Legendary Action Uses: 3 (4 in Lair). Immediately after another creature's turn, the dragon can expend a use to take one of the following actions. The dragon regains all expended uses at the start of each of its turns.*

            _**Cloud of Insects.**_ *Dexterity Saving Throw:* DC 21, one creature the dragon can see within 120 feet. *Failure:* 33 (6d10) Poison damage, and the target has Disadvantage on saving throws to maintain Concentration until the end of its next turn. *Failure or Success:* The dragon can't take this action again until the start of its next turn.

            _**Frightful Presence.**_ The dragon uses Spellcasting to cast *Fear*. The dragon can't take this action again until the start of its next turn.

            _**Pounce.**_ The dragon moves up to half its Speed, and it makes one Rend attack.

        """)

        assert expected == self.run_text_through_filter(clean_actions_emphasis, text)
        assert expected == self.run_text_through_filter(clean_actions_emphasis, expected)
