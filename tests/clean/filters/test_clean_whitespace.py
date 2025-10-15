from textwrap import dedent
from clean_srd import clean_whitespace
from . import TestFilter


class TestCleanWhitespace(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            "Very familiar" is a place you have been very often, a place you have carefully studied, or a place you can see when you cast the spell. "Seen casually" is someplace you have seen more than once but with which you aren't very familiar. "Viewed once" is a place you have seen once, possibly using magic. "Description" is a place whose location and appearance you know through someone else's description, perhaps from a map.

            "False destination" is a place that doesn't exist. Perhaps you tried to scry an enemy's sanctum but instead viewed an illusion, or you are attempting to teleport to a familiar location that no longer exists.
        """)

        assert text == self.run_text_through_filter(clean_whitespace, text)

    def test_filtering(self):
        text = dedent("""\
            The destination you choose must be known to you, and it must be on the same plane of existence as you. Your familiarity with the destination determines whether you arrive there successfully. The GM rolls d100 and consults the table.

            |                      |        | Similar | Off    | On     |
            |----------------------|--------|---------|--------|--------|
            | Familiarity          | Mishap | Area    | Target | Target |
            | Permanent<br>circle  | —      | —       | —      | 01–100 |
            | Associated<br>object | —      | —       | —      | 01–100 |
            | Very	familiar        | 01–05  | 06–13   | 14–24  | 25–100 |
            | Seen	casually        | 01–33  | 34–43   | 44–53  | 54–100 |
            | Viewed	once          | 01–43  | 44–53   | 54–73  | 74–100 |
            | Description          | 01–43  | 44–53   | 54–73  | 74–100 |
            | False<br>destination | 01–50  | 51–100  | —      | —      |
        """)
        expected = dedent("""\
            The destination you choose must be known to you, and it must be on the same plane of existence as you. Your familiarity with the destination determines whether you arrive there successfully. The GM rolls d100 and consults the table.

            |                      |        | Similar | Off    | On     |
            |----------------------|--------|---------|--------|--------|
            | Familiarity          | Mishap | Area    | Target | Target |
            | Permanent circle  | —      | —       | —      | 01–100 |
            | Associated object | —      | —       | —      | 01–100 |
            | Very familiar        | 01–05  | 06–13   | 14–24  | 25–100 |
            | Seen casually        | 01–33  | 34–43   | 44–53  | 54–100 |
            | Viewed once          | 01–43  | 44–53   | 54–73  | 74–100 |
            | Description          | 01–43  | 44–53   | 54–73  | 74–100 |
            | False destination | 01–50  | 51–100  | —      | —      |
        """)

        assert expected == self.run_text_through_filter(clean_whitespace, text)
