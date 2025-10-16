from textwrap import dedent
from clean_srd import clean_escape_square_brackets
from . import TestFilter


class TestCleanEscapeBrackets(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            # **Grappling**

            A creature can grapple another creature. Characters typically grapple by using an Unarmed Strike. Many monsters have special attacks that allow them to quickly grapple prey. However a grapple is initiated, it follows these rules. *See also* "Unarmed Strike" and "Grappled."
        """)

        assert text == self.run_text_through_filter(clean_escape_square_brackets, text)

    def test_filtering(self):
        text = dedent("""\
            - **Tags in Brackets.** Some entries have a tag in brackets after the entry's name, as in "Attack [Action]." A tag—Action, Area of Effect, Attitude, Condition, or Hazard—indicates that a rule is part of a family of rules. The tags also have glossary entries.
        """)
        expected = dedent("""\
            - **Tags in Brackets.** Some entries have a tag in brackets after the entry's name, as in "Attack \\[Action\\]." A tag—Action, Area of Effect, Attitude, Condition, or Hazard—indicates that a rule is part of a family of rules. The tags also have glossary entries.
        """)

        assert expected == self.run_text_through_filter(clean_escape_square_brackets, text)
