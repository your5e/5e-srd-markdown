from textwrap import dedent
from clean_srd import clean_canonicalise_proper_nouns
from . import TestFilter


class TestCleanCanonicaliseProperNouns(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            Ages past, elves and humans waged a terrible war against evil dragons. When the world seemed doomed, powerful wizards came together and worked their greatest magic, forging five *Orbs of Dragonkind* (or *Dragon Orbs*) to help them defeat the dragons. One orb was taken to each of the five wizard towers, and there they were used to speed the war toward a victorious end. The wizards used the orbs to lure dragons to them, then destroyed the dragons with powerful magic.
        """)

        assert text == self.run_text_through_filter(clean_canonicalise_proper_nouns, text)

    def test_filtering(self):
        text = dedent("""\
            # Whispers of the Grave

            _Prerequisite: 9th level_

            You can cast *speak with dead* at will, without expending a spell slot.

            ## **Bag of Devouring**

            #### *Wondrous item, very rare*

            This bag superficially resembles a *bag of holding* but is a feeding orifice for a gigantic extradimensional creature. Turning the bag inside out closes the orifice.
        """)
        expected = dedent("""\
            # Whispers of the Grave

            _Prerequisite: 9th level_

            You can cast _Speak with Dead_ at will, without expending a spell slot.

            ## **Bag of Devouring**

            #### *Wondrous item, very rare*

            This bag superficially resembles a _Bag of Holding_ but is a feeding orifice for a gigantic extradimensional creature. Turning the bag inside out closes the orifice.
        """)

        assert expected == self.run_text_through_filter(clean_canonicalise_proper_nouns, text)
        assert expected == self.run_text_through_filter(clean_canonicalise_proper_nouns, expected)
