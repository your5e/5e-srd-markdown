from textwrap import dedent

from update_vault import process_spell_wikilinks
from . import TestFilter


class TestProcessSpellWikilinks(TestFilter):
    def test_unprocessed_text(self):
        text = dedent("""\
            _**Mucus Cloud.**_ While underwater, the aboleth is surrounded by mucus. _Constitution Saving Throw:_ DC 14, each creature in a 5-foot Emanation originating from the aboleth at the end of the aboleth's turn. _Failure:_ The target is cursed. Until the curse ends, the target's skin becomes slimy, the target can breathe air and water, and it can't regain Hit Points unless it is underwater.
        """)

        assert text == self.run_text_through_processor(
            process_spell_wikilinks,
            text
        )

    def test_processed_text(self):
        text = dedent("""\
            ## Cantrips (Level 0 Cleric Spells)

            | Spell             | School        | Special   |
            |-------------------|---------------|-----------|
            | _Guidance_        | Divination    | C         |
            | _Light_           | Evocation     | —         |
            | _Mending_         | Transmutation | —         |
            | _Resistance_      | Abjuration    | C         |
            | _Sacred Flame_    | Evocation     | —         |
            | _Spare the Dying_ | Necromancy    | —         |
            | _Thaumaturgy_     | Transmutation | —         |
        """)
        expected = dedent("""\
            ## Cantrips (Level 0 Cleric Spells)

            | Spell             | School        | Special   |
            |-------------------|---------------|-----------|
            | [[Guidance]]        | Divination    | C         |
            | [[Light]]           | Evocation     | —         |
            | [[Mending]]         | Transmutation | —         |
            | [[Resistance]]      | Abjuration    | C         |
            | [[Sacred Flame]]    | Evocation     | —         |
            | [[Spare the Dying]] | Necromancy    | —         |
            | [[Thaumaturgy]]     | Transmutation | —         |
        """)

        assert expected == self.run_text_through_processor(
            process_spell_wikilinks,
            text
        )
        assert expected == self.run_text_through_processor(
            process_spell_wikilinks,
            expected
        )
