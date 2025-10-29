from textwrap import dedent
from clean_srd import clean_reitalicise_attack_actions
from . import TestFilter


class TestCleanReitaliciseAttackActions(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            _**Corrosive Form.**_ A creature that touches the pudding or hits it with a melee attack while within 5 feet of it takes 4 (1d8) acid damage. Any nonmagical weapon made of metal or wood that hits the pudding corrodes. After dealing damage, the weapon takes a permanent and cumulative -1 penalty to damage rolls. If its penalty drops to -5, the weapon is destroyed. Nonmagical ammunition made of metal or wood that hits the pudding is destroyed after dealing damage.
        """)

        assert text == self.run_text_through_filter(clean_reitalicise_attack_actions, text)

    def test_filtering(self):
        text = dedent("""\
            _**Pseudopod.** Melee Weapon Attack:_ +5 to hit, reach 5 ft., one target. _Hit:_ 6 (1d6 + 3) bludgeoning damage plus 18 (4d8) acid damage. In addition, nonmagical armor worn by the target is partly dissolved and takes a permanent and cumulative -1 penalty to the AC it offers. The armor is destroyed if the penalty reduces its AC to 10.
        """)
        expected = dedent("""\
            _**Pseudopod.**_ _Melee Weapon Attack:_ +5 to hit, reach 5 ft., one target. _Hit:_ 6 (1d6 + 3) bludgeoning damage plus 18 (4d8) acid damage. In addition, nonmagical armor worn by the target is partly dissolved and takes a permanent and cumulative -1 penalty to the AC it offers. The armor is destroyed if the penalty reduces its AC to 10.
        """)

        assert expected == self.run_text_through_filter(clean_reitalicise_attack_actions, text)
        assert expected == self.run_text_through_filter(clean_reitalicise_attack_actions, expected)
