from textwrap import dedent
from clean_srd import clean_collapse_adjacent_items
from . import TestFilter


class TestCleanCollapseAdjacentItems(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            *Giant Ancestry.* You are descended from Giants. Choose one of the following benefits—a supernatural boon from your ancestry; you can use the chosen benefit a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest:

            **Cloud's Jaunt (Cloud Giant).** As a Bonus Action, you magically teleport up to 30 feet to an unoccupied space you can see.

            **Fire's Burn (Fire Giant).** When you hit a target with an attack roll and deal damage to it, you can also deal 1d10 Fire damage to that target.

            **Frost's Chill (Frost Giant).** When you hit a target with an attack roll and deal damage to it, you can also deal 1d6 Cold damage to that target and reduce its Speed by 10 feet until the start of your next turn.
        """)

        assert text == self.run_text_through_filter(clean_collapse_adjacent_items, text)

    def test_filtering(self):
        text = dedent("""\

            **Skills** Perception +4

            **Senses** Darkvision 60 ft.; Passive Perception 14
            **Languages** Goblin, Worg
            **CR** 1/2 (XP 100; PB +2)

            - Choose one ability. The target has Disadvantage on ability checks and saving throws made with that ability.
            - The target has Disadvantage on attack rolls against you.
            - In combat, the target must succeed on a Wisdom saving throw at the start of each of its turns or be forced to take the Dodge action on that turn.

            - If you deal damage to the target with an attack roll or a spell, the target takes an extra 1d8 Necrotic damage.

            **Resistances** Cold
            **Immunities** Fire, Poison; Frightened, Poisoned
            **Senses** Darkvision 120 ft. (unimpeded by magical Darkness); Passive Perception 10
            **Languages** Infernal; telepathy 120 ft.

            **CR** 3 (XP 700; PB +2)

        """)
        expected = dedent("""\

            **Skills** Perception +4
            **Senses** Darkvision 60 ft.; Passive Perception 14
            **Languages** Goblin, Worg
            **CR** 1/2 (XP 100; PB +2)

            - Choose one ability. The target has Disadvantage on ability checks and saving throws made with that ability.
            - The target has Disadvantage on attack rolls against you.
            - In combat, the target must succeed on a Wisdom saving throw at the start of each of its turns or be forced to take the Dodge action on that turn.
            - If you deal damage to the target with an attack roll or a spell, the target takes an extra 1d8 Necrotic damage.

            **Resistances** Cold
            **Immunities** Fire, Poison; Frightened, Poisoned
            **Senses** Darkvision 120 ft. (unimpeded by magical Darkness); Passive Perception 10
            **Languages** Infernal; telepathy 120 ft.
            **CR** 3 (XP 700; PB +2)

        """)

        assert expected == self.run_text_through_filter(clean_collapse_adjacent_items, text)
        assert expected == self.run_text_through_filter(clean_collapse_adjacent_items, expected)
