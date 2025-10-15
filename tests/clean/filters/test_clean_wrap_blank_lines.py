from textwrap import dedent
from clean_srd import clean_wrap_blank_lines
from . import TestFilter


class TestCleanWrapBlankLines(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            # **Initiative**

            Initiative determines the order of turns during combat. When combat starts, every participant rolls Initiative; they make a Dexterity check that determines their place in the Initiative order. The GM rolls for monsters.

            *Initiative Order.* A combatant's check total is called their Initiative count, or Initiative for short. The GM ranks the combatants, from highest to lowest Initiative.
        """)

        assert text == self.run_text_through_filter(clean_wrap_blank_lines, text)

    def test_filtering(self):
        text = dedent("""\
            # **Initiative**


            Initiative determines the order of turns during combat. When combat starts, every participant rolls Initiative; they make a Dexterity check that determines their place in the Initiative order. The GM rolls for monsters.


            *Initiative Order.* A combatant's check total is called their Initiative count, or Initiative for short. The GM ranks the combatants, from highest to lowest Initiative.


            *Ties.* If a tie occurs, the GM decides the order among tied monsters, and the players decide the order among tied characters.
        """)
        expected = dedent("""\
            # **Initiative**

            Initiative determines the order of turns during combat. When combat starts, every participant rolls Initiative; they make a Dexterity check that determines their place in the Initiative order. The GM rolls for monsters.

            *Initiative Order.* A combatant's check total is called their Initiative count, or Initiative for short. The GM ranks the combatants, from highest to lowest Initiative.

            *Ties.* If a tie occurs, the GM decides the order among tied monsters, and the players decide the order among tied characters.
        """)

        assert expected == self.run_text_through_filter(clean_wrap_blank_lines, text)
