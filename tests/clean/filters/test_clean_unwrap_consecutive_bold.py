from textwrap import dedent
from clean_srd import clean_unwrap_consecutive_bold
from . import TestFilter


class TestCleanUnwrapConsecutiveBold(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ## **Hit Points**

            **Hit Dice:** 1d8 per bard level

            **Hit Points at 1st Level:** 8 + your Constitution modifier

            **Hit Points at Higher Levels:** 1d8 (or 5) + your Constitution modifier per bard level after 1st
        """)

        assert text == self.run_text_through_filter(clean_unwrap_consecutive_bold, text)

    def test_filtering(self):
        text = dedent("""\
            #### **Solar**

            *Large celestial, lawful good*

            **Armor Class** 21 (natural armor) **Hit Points** 243 (18d10 + 144) **Speed** 50 ft., fly 150 ft.

            | STR     | DEX     | CON     | INT     | WIS | CHA              |

            #### **Acid Arrow**

            *2nd-level evocation*

            **Casting Time:** 1 action **Range:** 90 feet **Components:** V, S, M (powdered rhubarb leaf and an adder's stomach) **Duration:** Instantaneous

            A shimmering green arrow streaks toward a target within range and bursts in a spray of acid. Make a ranged spell attack against the target. On a hit, the target takes 4d4 acid damage immediately and 2d4 acid damage at the end of its next turn. On a miss, the arrow splashes the target with acid for half as much of the initial damage and no damage at the end of its next turn.
        """)
        expected = dedent("""\
            #### **Solar**

            *Large celestial, lawful good*

            **Armor Class** 21 (natural armor)
            **Hit Points** 243 (18d10 + 144)
            **Speed** 50 ft., fly 150 ft.

            | STR     | DEX     | CON     | INT     | WIS | CHA              |

            #### **Acid Arrow**

            *2nd-level evocation*

            **Casting Time:** 1 action
            **Range:** 90 feet
            **Components:** V, S, M (powdered rhubarb leaf and an adder's stomach)
            **Duration:** Instantaneous

            A shimmering green arrow streaks toward a target within range and bursts in a spray of acid. Make a ranged spell attack against the target. On a hit, the target takes 4d4 acid damage immediately and 2d4 acid damage at the end of its next turn. On a miss, the arrow splashes the target with acid for half as much of the initial damage and no damage at the end of its next turn.
        """)

        assert expected == self.run_text_through_filter(clean_unwrap_consecutive_bold, text)
        assert expected == self.run_text_through_filter(clean_unwrap_consecutive_bold, expected)
