from textwrap import dedent
from clean_srd import clean_single_action_to_list
from . import TestFilter


class TestCleanSingleActionToList(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ### Actions

            - _**Multiattack.**_ The dragon makes three attacks.

            _**Bite.**_ Melee Attack Roll: +11, reach 10 ft.
        """)

        assert text == self.run_text_through_filter(clean_single_action_to_list, text)

    def test_filtering_actions(self):
        text = dedent("""\
            #### Actions

            _**Longsword.**_ Melee Weapon Attack: +3 to hit, reach 5 ft., one target. *Hit:* 5 (1d8 + 1) slashing damage.

            #### **Rug of Smothering**
        """)
        expected = dedent("""\
            #### Actions

            - _**Longsword.**_ Melee Weapon Attack: +3 to hit, reach 5 ft., one target. *Hit:* 5 (1d8 + 1) slashing damage.

            #### **Rug of Smothering**
        """)

        assert expected == self.run_text_through_filter(clean_single_action_to_list, text)

    def test_filtering_traits(self):
        text = dedent("""\
            ### Traits

            _**Legendary Resistance (3/Day).**_ If the dragon fails a saving throw, it can choose to succeed instead.
        """)
        expected = dedent("""\
            ### Traits

            - _**Legendary Resistance (3/Day).**_ If the dragon fails a saving throw, it can choose to succeed instead.
        """)

        assert expected == self.run_text_through_filter(clean_single_action_to_list, text)

    def test_filtering_reactions(self):
        text = dedent("""\
            ### Reactions

            _**Parry.**_ The knight adds 2 to its AC against one melee attack that would hit it.
        """)
        expected = dedent("""\
            ### Reactions

            - _**Parry.**_ The knight adds 2 to its AC against one melee attack that would hit it.
        """)

        assert expected == self.run_text_through_filter(clean_single_action_to_list, text)
