from textwrap import dedent

from update_vault import process_magic_item_wikilinks
from . import TestFilter


class TestProcessMagicItemWikilinks(TestFilter):
    def test_unprocessed_text(self):
        text = dedent("""\
            ### Potion of Mind Reading

            _Potion, Rare_

            When you drink this potion, you gain the effect of the _Detect Thoughts_ spell (save DC 13) for 10 minutes (no Concentration required).

            This potion's dense, purple liquid has an ovoid cloud of pink floating in it.
        """)

        assert text == self.run_text_through_processor(
            process_magic_item_wikilinks,
            text
        )

    def test_processed_text(self):
        text = dedent("""\
            This concoction looks, smells, and tastes like a _Potion of Healing_ or another beneficial potion. However, it is actually poison masked by illusion magic. _Identify_ reveals its true nature.
        """)
        expected = dedent("""\
            This concoction looks, smells, and tastes like a [[Potion of Healing]] or another beneficial potion. However, it is actually poison masked by illusion magic. _Identify_ reveals its true nature.
        """)

        assert expected == self.run_text_through_processor(
            process_magic_item_wikilinks,
            text,
        )
        assert expected == self.run_text_through_processor(
            process_magic_item_wikilinks,
            expected,
        )
