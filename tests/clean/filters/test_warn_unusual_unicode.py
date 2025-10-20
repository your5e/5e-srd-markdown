from textwrap import dedent
from clean_srd import warn_unusual_unicode
from . import TestFilter


class TestWarnUnusualUnicode(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            | Score   |   Modifier |
            |---------|------------|
            | 1       |         -5 |
            | 2-3     |         -4 |
            | 4-5     |         -3 |
            | 6-7     |         -2 |
            | 8-9     |         -1 |
            | 10-11   |         +0 |

            The steed resembles a Large, rideable animal of your choice, such as a horse, a camel, a dire wolf, or an elk. Whenever you cast the spell, choose the steed's creature type — Celestial, Fey, or Fiend which determines certain traits in the stat block.

            | Your Knowledge of the Target Is …   |   Save Modifier |
            |-------------------------------------|-----------------|
            | Secondhand (heard of the target)    |              +5 |
            | Firsthand (met the target)          |              +0 |
            | Extensive (know the target well)    |              -5 |

            † Characters' rate of travel while waterborne depends on the vehicle carrying them; see "Vehicles."
        """)

        assert not self.check_text_for_warning(warn_unusual_unicode, text)

    def test_warning(self):
        text = dedent("""\
            | Score | Modifier | Score | Modifier |
            |-------|----------|-------|----------|
            | 1     | −5       | 16–17 | +3       |
            | 2–3   | −4       | 18–19 | +4       |
            | 4–5   | −3       | 20–21 | +5       |
            | 6–7   | −2       | 22–23 | +6       |
            | 8–9   | −1       | 24–25 | +7       |
            | 10–11 | +0       | 26–27 | +8       |
            | 12–13 | +1       | 28–29 | +9       |
            | 14–15 | +2       | 30    | +10      |
        """)

        assert self.check_text_for_warning(warn_unusual_unicode, text)
