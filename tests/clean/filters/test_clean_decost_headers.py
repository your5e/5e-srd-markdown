from textwrap import dedent
from clean_srd import clean_decost_headers
from . import TestFilter


class TestCleanDecostHeaders(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ## Shield

            You gain the Armor Class benefit of a Shield only if you have training with it.
        """)

        assert text == self.run_text_through_filter(clean_decost_headers, text)

    def test_filtering(self):
        text = dedent("""\
            # Alchemist's Supplies (50 GP)

            **Ability:** Intelligence
            **Weight:** 8 lb.
            **Utilize:** Identify a substance (DC 15), or start a fire (DC 15)
            **Craft:** Acid, Alchemist's Fire, Component Pouch, Oil, Paper, Perfume

            # Alchemist's Fire (50 GP)

            When you take the Attack action, you can replace one of your attacks with throwing a flask of Alchemist's Fire. Target one creature or object you can see within 20 feet of yourself. The target must succeed on a Dexterity saving throw (DC 8 plus your Dexterity modifier and Proficiency Bonus) or take 1d4 Fire damage and start burning (see "Rules Glossary").

            ### Spell Scroll (Cantrip, 30 GP; Level 1, 50 GP)

            A _Spell Scroll_ (Cantrip) or _Spell Scroll_ (Level 1) is a magic item that bears the words of a cantrip or level 1 spell, respectively, determined by the scroll's creator. If the spell is on your class's spell list, you can read the scroll and cast the spell using its normal casting time and without providing any Material components.

            ### Wretched (Free)

            You survive via chance and charity. You're often exposed to natural dangers as a result of sleeping outside.
        """)
        expected = dedent("""\
            # Alchemist's Supplies

            **Cost:** 50 GP
            **Ability:** Intelligence
            **Weight:** 8 lb.
            **Utilize:** Identify a substance (DC 15), or start a fire (DC 15)
            **Craft:** Acid, Alchemist's Fire, Component Pouch, Oil, Paper, Perfume

            # Alchemist's Fire

            **Cost:** 50 GP

            When you take the Attack action, you can replace one of your attacks with throwing a flask of Alchemist's Fire. Target one creature or object you can see within 20 feet of yourself. The target must succeed on a Dexterity saving throw (DC 8 plus your Dexterity modifier and Proficiency Bonus) or take 1d4 Fire damage and start burning (see "Rules Glossary").

            ### Spell Scroll

            **Cost:** Cantrip, 30 GP; Level 1, 50 GP

            A _Spell Scroll_ (Cantrip) or _Spell Scroll_ (Level 1) is a magic item that bears the words of a cantrip or level 1 spell, respectively, determined by the scroll's creator. If the spell is on your class's spell list, you can read the scroll and cast the spell using its normal casting time and without providing any Material components.

            ### Wretched

            **Cost:** Free

            You survive via chance and charity. You're often exposed to natural dangers as a result of sleeping outside.
        """)

        assert expected == self.run_text_through_filter(clean_decost_headers, text)
        assert expected == self.run_text_through_filter(clean_decost_headers, expected)
