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

    def test_processed_text(self):
        text = dedent("""\
            - _**Smother.** Melee Weapon Attack:_ +5 to hit, reach 5 ft., one Medium or smaller creature. _Hit:_ The creature is grappled (escape DC 13). Until this grapple ends, the target is restrained, blinded, and at risk of suffocating, and the rug can't smother another target. In addition, at the start of each of the target's turns, the target takes 10 (2d6 + 3) bludgeoning damage.
        """)
        expected = dedent("""\
            - _**Smother.** Melee Weapon Attack:_ +5 to hit, reach 5 ft., one Medium or smaller creature. _Hit:_ The creature is [[grappled]] (escape DC 13). Until this grapple ends, the target is [[restrained]], [[blinded]], and at risk of suffocating, and the rug can't smother another target. In addition, at the start of each of the target's turns, the target takes 10 (2d6 + 3) bludgeoning damage.
        """)

        assert expected == self.run_text_through_processor(
            process_condition_wikilinks,
            text
        )
        assert expected == self.run_text_through_processor(
            process_condition_wikilinks,
            expected
        )
