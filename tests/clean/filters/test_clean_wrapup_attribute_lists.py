from textwrap import dedent
from clean_srd import clean_wrapup_attribute_lists
from . import TestFilter


class TestCleanWrapupAttributeLists(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            #### **Actions**

            *Multiattack.* The worm makes two attacks: one with its bite and one with its stinger.

            *Tail Stinger. Melee Weapon Attack:* +9 to hit, reach 10 ft., one creature. *Hit:* 19 (3d6 + 9) piercing damage, and the target must make a DC 19 Constitution saving throw, taking 42 (12d6) poison damage on a failed save, or half as much damage on a successful one.
        """)

        assert text == self.run_text_through_filter(clean_wrapup_attribute_lists, text)

    def test_filtering(self):
        text = dedent("""\
            #### **Purple Worm**

            *Gargantuan monstrosity, unaligned*

            **Armor Class** 18 (natural armor)

            **Hit Points** 247 (15d20 + 90)

            **Speed** 50 ft., burrow 30 ft.
        """)
        expected = dedent("""\
            #### **Purple Worm**

            *Gargantuan monstrosity, unaligned*

            - **Armor Class** 18 (natural armor)
            - **Hit Points** 247 (15d20 + 90)
            - **Speed** 50 ft., burrow 30 ft.
        """)

        assert expected == self.run_text_through_filter(clean_wrapup_attribute_lists, text)
        assert expected == self.run_text_through_filter(clean_wrapup_attribute_lists, expected)
