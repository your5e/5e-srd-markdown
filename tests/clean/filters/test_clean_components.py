from textwrap import dedent
from clean_srd import clean_pluralise_component
from . import TestFilter


class TestCleanPluraliseComponent(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            *Level 2 Illusion (Wizard)*

            **Casting Time:** Action **Range:** Touch

            **Components:** V, S, M (a small square of silk) **Duration:** 24 hours

            With a touch, you place an illusion on a willing creature.
        """)

        assert text == self.run_text_through_filter(clean_pluralise_component, text)

    def test_filtering(self):
        text = dedent("""\
            *Level 2 Illusion (Wizard)*

            **Casting Time:** Action **Range:** Touch

            **Component:** V, S, M (a small square of silk) **Duration:** 24 hours

            With a touch, you place an illusion on a willing creature.
        """)
        expected = dedent("""\
            *Level 2 Illusion (Wizard)*

            **Casting Time:** Action **Range:** Touch

            **Components:** V, S, M (a small square of silk) **Duration:** 24 hours

            With a touch, you place an illusion on a willing creature.
        """)

        assert expected == self.run_text_through_filter(clean_pluralise_component, text)
