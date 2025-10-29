from textwrap import dedent

from update_vault import process_condition_wikilinks
from . import TestFilter


class TestProcessConditionWikilinks(TestFilter):
    def test_unprocessed_text(self):
        text = dedent("""\
            - _**Multiattack.**_ The veteran makes two longsword attacks. If it has a shortsword drawn, it can also make a shortsword attack.
        """)

        assert text == self.run_text_through_processor(
            process_condition_wikilinks,
            text
        )

    def test_unprocessed_text_file_dependent(self):
        text = dedent("""\
            # Poisoned

            - A poisoned creature has disadvantage on attack rolls and ability checks.
        """)

        assert text == self.run_text_through_processor(
            process_condition_wikilinks,
            text,
            'Conditions/Poisoned.md',
        )

    def test_processed_text(self):
        text = dedent("""\
            - _**Smother.** Melee Weapon Attack:_ +5 to hit, reach 5 ft., one Medium or smaller creature. _Hit:_ The creature is grappled (escape DC 13). Until this grapple ends, the target is restrained, blinded, and at risk of suffocating, and the rug can't smother another target. In addition, at the start of each of the target's turns, the target takes 10 (2d6 + 3) bludgeoning damage.
        """)
        expected = dedent("""\
            - _**Smother.** Melee Weapon Attack:_ +5 to hit, reach 5 ft., one Medium or smaller creature. _Hit:_ The creature is [[Grappled]] (escape DC 13). Until this grapple ends, the target is [[Restrained]], [[Blinded]], and at risk of suffocating, and the rug can't smother another target. In addition, at the start of each of the target's turns, the target takes 10 (2d6 + 3) bludgeoning damage.
        """)

        assert expected == self.run_text_through_processor(
            process_condition_wikilinks,
            text
        )
        assert expected == self.run_text_through_processor(
            process_condition_wikilinks,
            expected
        )

    def test_processed_text_file_dependent(self):
        text = dedent("""\
            # Grappled

            - A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed.
            - The condition ends if the grappler is [[Incapacitated]] (see the condition).
            - The condition also ends if an effect removes the grappled creature from the reach of the grappler or grappling effect, such as when a creature is hurled away by the _thunder-wave_ spell.
        """)

        assert text == self.run_text_through_processor(
            process_condition_wikilinks,
            text,
            'Conditions/Grappled.md',
        )
