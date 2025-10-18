from textwrap import dedent
from clean_srd import clean_add_traits_header
from . import TestFilter


class TestCleanAddTraitsHeader(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            #### **Flying Sword**

            *Small construct, unaligned*

            **Armor Class** 17 (natural armor)

            **Hit Points** 17 (5d6)

            **Speed** 0 ft., fly 50 ft. (hover)
        """)

        assert text == self.run_text_through_filter(clean_add_traits_header, text)

    def test_filtering(self):
        text = dedent("""\
            **Languages** —

            **Challenge** 1/4 (50 XP)

            *Antimagic Susceptibility.* The sword is incapacitated while in the area of an *antimagic field.* If targeted by *dispel magic*, the sword must succeed on a Constitution saving throw against the caster's spell save DC or fall unconscious for 1 minute.
        """)
        expected = dedent("""\
            **Languages** —

            **Challenge** 1/4 (50 XP)

            #### Traits

            *Antimagic Susceptibility.* The sword is incapacitated while in the area of an *antimagic field.* If targeted by *dispel magic*, the sword must succeed on a Constitution saving throw against the caster's spell save DC or fall unconscious for 1 minute.
        """)

        assert expected == self.run_text_through_filter(clean_add_traits_header, text)
        assert expected == self.run_text_through_filter(clean_add_traits_header, expected)
