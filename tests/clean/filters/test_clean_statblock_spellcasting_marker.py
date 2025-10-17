from textwrap import dedent
from clean_srd import clean_statblock_spellcasting_marker
from . import TestFilter


class TestCleanStatblockSpellcastingMarker(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            - _**Spellcasting.**_ The archmage is an 18th-level spellcaster. Its spellcasting ability is Intelligence (spell save DC 17, +9 to hit with spell attacks). The archmage can cast *disguise self* and *invisibility* at will and has the following wizard spells prepared:

                - Cantrips (at will): mage hand, prestidigitation
                - 1st level (4 slots): detect magic, magic missile
        """)

        assert text == self.run_text_through_filter(clean_statblock_spellcasting_marker, text)

    def test_filtering_spellcasting(self):
        text = dedent("""\
            _**Spellcasting.**_ The archmage is an 18th-level spellcaster. Its spellcasting ability is Intelligence (spell save DC 17, +9 to hit with spell attacks). The archmage can cast *disguise self* and *invisibility* at will and has the following wizard spells prepared:

                - Cantrips (at will): *fire bolt*, *light*, *mage hand*, *prestidigitation*, *shocking grasp*
                - 1st level (4 slots): *detect magic*, *identify*, *mage armor*,\\* *magic missile*
        """)
        expected = dedent("""\
            - _**Spellcasting.**_ The archmage is an 18th-level spellcaster. Its spellcasting ability is Intelligence (spell save DC 17, +9 to hit with spell attacks). The archmage can cast *disguise self* and *invisibility* at will and has the following wizard spells prepared:

                - Cantrips (at will): *fire bolt*, *light*, *mage hand*, *prestidigitation*, *shocking grasp*
                - 1st level (4 slots): *detect magic*, *identify*, *mage armor*,\\* *magic missile*
        """)

        assert expected == self.run_text_through_filter(clean_statblock_spellcasting_marker, text)

    def test_filtering_innate_spellcasting(self):
        text = dedent("""\
            _**Innate Spellcasting.**_ The djinni's innate spellcasting ability is Charisma (spell save DC 17, +9 to hit with spell attacks). It can innately cast the following spells, requiring no material components:

                - At will: *detect evil and good*, *detect magic*, *thunderwave*
                - 3/day each: *create food and water* (can create wine instead of water), *tongues*, *wind walk*
        """)
        expected = dedent("""\
            - _**Innate Spellcasting.**_ The djinni's innate spellcasting ability is Charisma (spell save DC 17, +9 to hit with spell attacks). It can innately cast the following spells, requiring no material components:

                - At will: *detect evil and good*, *detect magic*, *thunderwave*
                - 3/day each: *create food and water* (can create wine instead of water), *tongues*, *wind walk*
        """)

        assert expected == self.run_text_through_filter(clean_statblock_spellcasting_marker, text)
