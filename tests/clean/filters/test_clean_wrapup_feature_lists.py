from textwrap import dedent
from clean_srd import clean_wrapup_feature_lists
from . import TestFilter


class TestCleanWrapupFeatureLists(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            #### **Pseudodragon**

            *Tiny dragon, neutral good*

            **Armor Class** 13 (natural armor)

            **Hit Points** 7 (2d4 + 2)
        """)

        assert text == self.run_text_through_filter(clean_wrapup_feature_lists, text)

    def test_filtering_consecutive_features(self):
        text = dedent("""\
            **Challenge** 1/4 (50 XP)

            _**Keen Senses.**_ The pseudodragon has advantage on Wisdom (Perception) checks that rely on sight, hearing, or smell.

            _**Magic Resistance.**_ The pseudodragon has advantage on saving throws against spells and other magical effects.

            _**Limited Telepathy.**_ The pseudodragon can magically communicate simple ideas, emotions, and images telepathically with any creature within 100 feet of it that can understand a language.
        """)
        expected = dedent("""\
            **Challenge** 1/4 (50 XP)

            - _**Keen Senses.**_ The pseudodragon has advantage on Wisdom (Perception) checks that rely on sight, hearing, or smell.
            - _**Magic Resistance.**_ The pseudodragon has advantage on saving throws against spells and other magical effects.
            - _**Limited Telepathy.**_ The pseudodragon can magically communicate simple ideas, emotions, and images telepathically with any creature within 100 feet of it that can understand a language.
        """)

        assert expected == self.run_text_through_filter(clean_wrapup_feature_lists, text)
