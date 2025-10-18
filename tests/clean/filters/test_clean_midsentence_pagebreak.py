from textwrap import dedent
from clean_srd import clean_midsentence_pagebreak
from . import TestFilter


class TestCleanMidsentencePagebreak(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            Your rage lasts for 1 minute. It ends early if you are knocked unconscious or if your turn ends and you haven't attacked a hostile creature since your last turn or taken damage since then. You can also end your rage on your turn as a bonus action.

            Once you have raged the number of times shown for your barbarian level in the Rages column of the Barbarian table, you must finish a long rest before you can rage again.
        """)

        assert text == self.run_text_through_filter(clean_midsentence_pagebreak, text)

    def test_filtering(self):
        text = dedent("""\
            When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful

            one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.

            When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful



            one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.

            With each new level, characters acquire new capabilities that equip them to handle greater challenges. As characters advance in level, the tone of the game also changes, and the stakes of the campaign get higher. It's helpful to think of a character's (and a campaign's) arc in terms of four tiers of play,

            describing the journey from a level 1 character just beginning an adventuring career to the epic heights of level 20. These tiers don't have any rules associated with them; they point to the fact that the play experience evolves as characters gain levels.

        """)
        expected = dedent("""\
            When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.

            When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.

            With each new level, characters acquire new capabilities that equip them to handle greater challenges. As characters advance in level, the tone of the game also changes, and the stakes of the campaign get higher. It's helpful to think of a character's (and a campaign's) arc in terms of four tiers of play, describing the journey from a level 1 character just beginning an adventuring career to the epic heights of level 20. These tiers don't have any rules associated with them; they point to the fact that the play experience evolves as characters gain levels.

        """)

        assert expected == self.run_text_through_filter(clean_midsentence_pagebreak, text)
        assert expected == self.run_text_through_filter(clean_midsentence_pagebreak, expected)
