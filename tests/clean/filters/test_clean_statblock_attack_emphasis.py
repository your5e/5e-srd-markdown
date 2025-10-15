from textwrap import dedent
from clean_srd import clean_statblock_attack_emphasis
from . import TestFilter


class TestCleanStatblockAttackEmphasis(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            **Challenge** 10 (5,900 XP)

            *Amphibious.* The aboleth can breathe air and water.
        """)

        assert text == self.run_text_through_filter(clean_statblock_attack_emphasis, text)

    def test_filtering(self):
        text = dedent("""\
            #### **Actions**

            *Multiattack.* The aboleth makes three tentacle attacks. *Tentacle. Melee Weapon Attack:* +9 to hit, reach 10 ft., one target. *Hit:* 12 (2d6 + 5) bludgeoning damage. If the target is a creature, it must succeed on a DC 14 Constitution saving throw or become diseased. The disease has no effect for 1 minute and can be removed by any magic that cures disease. After 1 minute, the diseased creature's skin becomes translucent and slimy, the creature can't regain hit points unless it is underwater, and the disease can be removed only by *heal* or another disease-curing spell of 6th level or higher. When the creature is outside a body of water, it takes 6 (1d12) acid damage every 10 minutes unless moisture is applied to the skin before 10 minutes have passed.

            *Tail. Melee Weapon Attack:* +9 to hit, reach 10 ft. one target. *Hit:* 15 (3d6 + 5) bludgeoning damage.
        """)
        expected = dedent("""\
            #### **Actions**

            *Multiattack.* The aboleth makes three tentacle attacks. *Tentacle. Melee Weapon Attack:* +9 to hit, reach 10 ft., one target. *Hit:* 12 (2d6 + 5) bludgeoning damage. If the target is a creature, it must succeed on a DC 14 Constitution saving throw or become diseased. The disease has no effect for 1 minute and can be removed by any magic that cures disease. After 1 minute, the diseased creature's skin becomes translucent and slimy, the creature can't regain hit points unless it is underwater, and the disease can be removed only by *heal* or another disease-curing spell of 6th level or higher. When the creature is outside a body of water, it takes 6 (1d12) acid damage every 10 minutes unless moisture is applied to the skin before 10 minutes have passed.

            _**Tail.** Melee Weapon Attack:_ +9 to hit, reach 10 ft. one target. *Hit:* 15 (3d6 + 5) bludgeoning damage.
        """)

        assert expected == self.run_text_through_filter(clean_statblock_attack_emphasis, text)
