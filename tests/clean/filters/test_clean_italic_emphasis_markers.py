from textwrap import dedent
from clean_srd import clean_italic_emphasis_markers
from . import TestFilter


class TestCleanItalicEmphasisMarkers(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            # **Monsters**

            A monster's statistics, sometimes referred to as its **stat block**, provide the essential information that you need to run the monster.
        """)

        assert text == self.run_text_through_filter(clean_italic_emphasis_markers, text)

    def test_filtering(self):
        text = dedent("""\
            Ages past, elves and humans waged a terrible war against evil dragons. When the world seemed doomed, powerful wizards came together and worked their greatest magic, forging five *Orbs of Dragonkind* (or *Dragon Orbs*) to help them defeat the dragons. One orb was taken to each of the five wizard towers, and there they were used to speed the war toward a victorious end. The wizards used the orbs to lure dragons to them, then destroyed the dragons with powerful magic.
        """)
        expected = dedent("""\
            Ages past, elves and humans waged a terrible war against evil dragons. When the world seemed doomed, powerful wizards came together and worked their greatest magic, forging five _Orbs of Dragonkind_ (or _Dragon Orbs_) to help them defeat the dragons. One orb was taken to each of the five wizard towers, and there they were used to speed the war toward a victorious end. The wizards used the orbs to lure dragons to them, then destroyed the dragons with powerful magic.
        """)

        assert expected == self.run_text_through_filter(clean_italic_emphasis_markers, text)
        assert expected == self.run_text_through_filter(clean_italic_emphasis_markers, expected)
