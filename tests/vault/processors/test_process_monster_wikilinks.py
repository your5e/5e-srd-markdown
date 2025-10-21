from textwrap import dedent

from update_vault import process_monster_wikilinks
from . import TestFilter


class TestProcessMonsterWikilinks(TestFilter):
    def test_unprocessed_text(self):
        text = dedent("""\
            _**Skull.**_ An **Avatar of Death** (see the accompanying stat block) appears in an unoccupied space as close to you as possible. The avatar targets only you with its attacks, appearing as a ghostly skeleton clad in a tattered black robe and carrying a spectral scythe. The avatar disappears when it drops to 0 Hit Points or you die. If an ally of yours deals damage to the avatar, that ally summons another **Avatar of Death**. The new avatar appears in an unoccupied space as close to that ally as possible and targets only that ally with its attacks. You and your allies can each summon only one avatar as a consequence of this draw. A creature slain by an avatar can't be restored to life.
        """)

        assert text == self.run_text_through_processor(
            process_monster_wikilinks,
            text
        )

    def test_processed_text(self):
        text = dedent("""\
            - **-** 1 **Bugbear Warrior** (200 XP)
            - **-** 2 **Giant Wasps** (100 XP each), for 200 XP total
            - **-** 6 **Giant Rats** (25 XP each), for 150 XP total

            _**Knight.**_ You gain the service of a **Knight**, who magically appears in an unoccupied space you choose within 30 feet of yourself. The knight has the same alignment as you and serves you loyally until death, believing the two of you have been drawn together by fate. Work with your GM to create a name and backstory for this NPC. The GM can use a different stat block to represent the knight, as desired.
        """)
        expected = dedent("""\
            - **-** 1 **[[Bugbear Warrior]]** (200 XP)
            - **-** 2 **[[Giant Wasp]]s** (100 XP each), for 200 XP total
            - **-** 6 **[[Giant Rat]]s** (25 XP each), for 150 XP total

            _**Knight.**_ You gain the service of a **[[Knight]]**, who magically appears in an unoccupied space you choose within 30 feet of yourself. The knight has the same alignment as you and serves you loyally until death, believing the two of you have been drawn together by fate. Work with your GM to create a name and backstory for this NPC. The GM can use a different stat block to represent the knight, as desired.
        """)

        assert expected == self.run_text_through_processor(
            process_monster_wikilinks,
            text
        )
        assert expected == self.run_text_through_processor(
            process_monster_wikilinks,
            expected
        )
