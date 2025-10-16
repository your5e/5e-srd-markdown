from textwrap import dedent
from clean_srd import clean_retabulate_ability_scores
from . import TestFilter


class TestCleanAbilityScoresLines521(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            | | Str. | Dex. | Con. | Int. | Wis. | Cha. |
            |--|--|--|--|--|--|--|
            | **Score** | 19 | 10 | 16 | 12 | 15 | 17 |
            | **Modifier** | +4 | +0 | +3 | +1 | +2 | +3 |
            | **Saving Throw** | +4 | +0 | +3 | +1 | +2 | +3 |

            |                  |  Str. |  Dex. |  Con. |  Int. |  Wis. |  Cha. |
            |------------------|-------|-------|-------|-------|-------|-------|
            | **Score**        |     3 |     8 |    11 |    10 |    10 |     6 |
            | **Modifier**     |    -4 |    -1 |    +0 |    +0 |    +0 |    -2 |
            | **Saving Throw** |    -4 |    -1 |    +0 |    +0 |    +0 |    -2 |

        """)

        assert text == self.run_text_through_filter(clean_retabulate_ability_scores, text)

    def test_filtering(self):
        text = dedent("""\
            **Str** 19 +4 +4
            **Dex** 10 +0 +0
            **Con** 16 +3 +3
            **Int** 12 +1 +1
            **Wis** 15 +2 +2
            **Cha** 17 +3 +3

            **Str** 3 -4 -4
            **Dex** 8 -1 -1
            **Con** 11 +0 +0
            **Int** 10 +0 +0
            **Wis** 10 +0 +0
            **Cha** 6 -2 -2

            ### Pirate Captain

            _Medium or Small Humanoid, Neutral_

            **AC** 17
            **Initiative** +7 (17)
            **HP** 84 (13d8 + 26)
            **Speed** 30 ft.
            **Str** 10 +0 +3
            **Dex** 18 +4 +7
            **Con** 14 +2 +2
            **Int** 10 +0 +0
            **Wis** 14 +2 +5
            **Cha** 17 +3 +6
            **Skills** Acrobatics +7, Perception +5
            **Gear** Pistol, Rapier
            **Senses** Passive Perception 15
            **Languages** Common plus one other language
            **CR** 6 (XP 2,300; PB +3)

        """)
        expected = dedent("""\

            | | Str. | Dex. | Con. | Int. | Wis. | Cha. |
            |--|--|--|--|--|--|--|
            | **Score** | 19 | 10 | 16 | 12 | 15 | 17 |
            | **Modifier** | +4 | +0 | +3 | +1 | +2 | +3 |
            | **Saving Throw** | +4 | +0 | +3 | +1 | +2 | +3 |

            | | Str. | Dex. | Con. | Int. | Wis. | Cha. |
            |--|--|--|--|--|--|--|
            | **Score** | 3 | 8 | 11 | 10 | 10 | 6 |
            | **Modifier** | -4 | -1 | +0 | +0 | +0 | -2 |
            | **Saving Throw** | -4 | -1 | +0 | +0 | +0 | -2 |

            ### Pirate Captain

            _Medium or Small Humanoid, Neutral_

            **AC** 17
            **Initiative** +7 (17)
            **HP** 84 (13d8 + 26)
            **Speed** 30 ft.

            | | Str. | Dex. | Con. | Int. | Wis. | Cha. |
            |--|--|--|--|--|--|--|
            | **Score** | 10 | 18 | 14 | 10 | 14 | 17 |
            | **Modifier** | +0 | +4 | +2 | +0 | +2 | +3 |
            | **Saving Throw** | +3 | +7 | +2 | +0 | +5 | +6 |

            **Skills** Acrobatics +7, Perception +5
            **Gear** Pistol, Rapier
            **Senses** Passive Perception 15
            **Languages** Common plus one other language
            **CR** 6 (XP 2,300; PB +3)

        """)

        assert expected == self.run_text_through_filter(clean_retabulate_ability_scores, text)
