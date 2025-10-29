from textwrap import dedent
from clean_srd import clean_recalculate_saving_throws
from . import TestFilter


class TestCleanRecalculateSavingThrows(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            - **Speed** 0 ft., fly 50 ft. (hover)

            **Str** 12 +1 +1
            **Dex** 15 +2 +4
            **Con** 11 +0 +0
            **Int** 1 -5 -5
            **Wis** 5 -3 -3
            **Cha** 1 -5 -5

            - **Damage Immunities** poison, psychic
        """)

        assert text == self.run_text_through_filter(clean_recalculate_saving_throws, text)

    def test_filtering(self):
        text = dedent("""\
            - **Speed** 0 ft., fly 50 ft. (hover)

            **Str** 12 +1 +1
            **Dex** 15 +2 +2
            **Con** 11 +0 +0
            **Int** 1 -5 -5
            **Wis** 5 -3 -3
            **Cha** 1 -5 -5

            - **Saving Throws** Dex +4
            - **Damage Immunities** poison, psychic

            # Vrock
            - **Speed** 40 ft., fly 60 ft.

            **Str** 17 +3 +3
            **Dex** 15 +2 +2
            **Con** 18 +4 +4
            **Int** 8 -1 -1
            **Wis** 13 +1 +1
            **Cha** 8 -1 -1

            - **Saving Throws** Dex +5, Wis +4, Cha +2
            - **Damage Resistances** cold, fire, lightning; bludgeoning, piercing, and slashing from nonmagical attacks
        """)
        expected = dedent("""\
            - **Speed** 0 ft., fly 50 ft. (hover)

            **Str** 12 +1 +1
            **Dex** 15 +2 +4
            **Con** 11 +0 +0
            **Int** 1 -5 -5
            **Wis** 5 -3 -3
            **Cha** 1 -5 -5

            - **Damage Immunities** poison, psychic

            # Vrock
            - **Speed** 40 ft., fly 60 ft.

            **Str** 17 +3 +3
            **Dex** 15 +2 +5
            **Con** 18 +4 +4
            **Int** 8 -1 -1
            **Wis** 13 +1 +4
            **Cha** 8 -1 +2

            - **Damage Resistances** cold, fire, lightning; bludgeoning, piercing, and slashing from nonmagical attacks
        """)

        assert expected == self.run_text_through_filter(clean_recalculate_saving_throws, text)
        assert expected == self.run_text_through_filter(clean_recalculate_saving_throws, expected)
