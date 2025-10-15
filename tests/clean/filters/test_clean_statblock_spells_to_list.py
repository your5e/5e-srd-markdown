from textwrap import dedent
from clean_srd import clean_statblock_spells_to_list
from . import TestFilter


class TestCleanStatblockSpellsToList(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            - _**Spellcasting.**_ The archmage is an 18th-level spellcaster.

            - **Cantrips (at will):** mage hand, prestidigitation

            - **1st level (4 slots):** detect magic, magic missile
        """)

        assert text == self.run_text_through_filter(clean_statblock_spells_to_list, text)

    def test_filtering_spell_levels(self):
        text = dedent("""\
            *Spellcasting.* The archmage is an 18th-level spellcaster. Its spellcasting ability is Intelligence (spell save DC 17, +9 to hit with spell attacks). The archmage can cast *disguise self* and *invisibility* at will and has the following wizard spells prepared:

            Cantrips (at will): *fire bolt*, *light*, *mage hand*, *prestidigitation*, *shocking grasp*

            1st level (4 slots): *detect magic*, *identify*, *mage armor*,\* *magic missile*
        """)
        expected = dedent("""\
            *Spellcasting.* The archmage is an 18th-level spellcaster. Its spellcasting ability is Intelligence (spell save DC 17, +9 to hit with spell attacks). The archmage can cast *disguise self* and *invisibility* at will and has the following wizard spells prepared:

                - Cantrips (at will): *fire bolt*, *light*, *mage hand*, *prestidigitation*, *shocking grasp*
                - 1st level (4 slots): *detect magic*, *identify*, *mage armor*,\* *magic missile*
        """)

        assert expected == self.run_text_through_filter(clean_statblock_spells_to_list, text)

    def test_filtering_at_will_spells(self):
        text = dedent("""\
            *Innate Spellcasting.* The deva's spellcasting ability is Charisma (spell save DC 17). The deva can innately cast the following spells, requiring only verbal components:

            At will: *detect evil and good*

            1/day each: *commune*, *raise dead*
        """)
        expected = dedent("""\
            *Innate Spellcasting.* The deva's spellcasting ability is Charisma (spell save DC 17). The deva can innately cast the following spells, requiring only verbal components:

                - At will: *detect evil and good*
                - 1/day each: *commune*, *raise dead*
        """)

        assert expected == self.run_text_through_filter(clean_statblock_spells_to_list, text)
