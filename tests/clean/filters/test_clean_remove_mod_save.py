from textwrap import dedent
from clean_srd import clean_remove_mod_save
from . import TestFilter


class TestCleanRemoveModSave(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            **AC** 19 (Natural Armor)

            **Speed** 40 ft., fly 80 ft.

            **HP** 195 (17d12 + 85)
        """)

        assert text == self.run_text_through_filter(clean_remove_mod_save, text)

    def test_filtering(self):
        text = dedent("""\
            **AC** 19 (Natural Armor) MOD SAVE MOD SAVE MOD SAVE

            **Speed** 40 ft., fly 80 ft. MOD SAVE MOD SAVE MOD SAVE

            **HP** 195 (17d12 + 85) MOD SAVE MOD SAVE MOD SAVE

            # **Awakened Shrub**

            *Small Plant, Neutral*

            **HP** 10 (3d6) **Speed** 20 ft.

            **AC** 9 **Initiative** −1 (9)

            MOD SAVE MOD SAVE MOD SAVE **Str** 3 −4 −4 **Dex** 8 −1 −1 **Con** 11 +0 +0 **Int** 10 +0 +0 **Wis** 10 +0 +0 **Cha** 6 −2 −2

            | MOD SAVE |  | MOD SAVE |  | MOD SAVE |  |
            |----------|--|----------|--|----------|--|
        """)
        expected = dedent("""\
            **AC** 19 (Natural Armor)

            **Speed** 40 ft., fly 80 ft.

            **HP** 195 (17d12 + 85)

            # **Awakened Shrub**

            *Small Plant, Neutral*

            **HP** 10 (3d6) **Speed** 20 ft.

            **AC** 9 **Initiative** −1 (9)

            **Str** 3 −4 −4 **Dex** 8 −1 −1 **Con** 11 +0 +0 **Int** 10 +0 +0 **Wis** 10 +0 +0 **Cha** 6 −2 −2

            | | | | | | |
            |----------|--|----------|--|----------|--|
        """)

        assert expected == self.run_text_through_filter(clean_remove_mod_save, text)
