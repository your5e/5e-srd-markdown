from textwrap import dedent
from clean_srd import clean_detabulate_mixed_stats
from . import TestFilter


class TestCleanDetabulateMixedStats(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            _Medium Dragon (Chromatic), Chaotic Evil_

            **AC** 17

            **Initiative** +4 (14)

            **HP** 33 (6d8 + 6)

            **Speed** 30 ft., Fly 60 ft., Swim 30 ft.

            **Str** 15 +2 +2
            **Dex** 14 +2 +4
            **Con** 13 +1 +1

            | Abbreviation | Stands For |
            |------|-------------------|
            | AC   | Armor Class       |
            | C    | Concentration     |
            | CE   | Chaotic Evil      |
            | CG   | Chaotic Good      |
            | Cha. | Charisma          |
            | CN   | Chaotic Neutral   |
            | Con. | Constitution      |
            | CP   | Copper Piece(s)   |
            | CR   | Challenge Rating  |
            | DC   | Difficulty Class  |
            | Dex. | Dexterity         |
            | EP   | Electrum Piece(s) |
            | GM   | Game Master       |
            | GP   | Gold Piece(s)     |
            | HP   | Hit Point(s)      |
            | Int. | Intelligence      |
            | LE   | Lawful Evil       |
            | LG   | Lawful Good       |
            | LN   | Lawful Neutral    |
            | M    | Material component         |
            | N    | Neutral           |
            | NE   | Neutral Evil      |
            | NG   | Neutral Good      |
            | NPC  | Nonplayer character        |
            | PB   | Proficiency Bonus |
            | PP   | Platinum Piece(s) |
            | R    | Ritual            |
            | S    | Somatic component          |
            | SP   | Silver Piece(s)   |
            | Str. | Strength          |
            | V    | Verbal component          |
            | Wis. | Wisdom            |
            | XP   | Experience Point(s)      |

            | | | MOD | SAVE |
            | -- | -- | -- | -- |
            | **STR** | 19 | +4  | +4   |
            | **DEX** | 10 | +0  | +0   |
            | **CON** | 16 | +3  | +3   |
            | **INT** | 12 | +1  | +1   |
            | **WIS** | 15 | +2  | +2   |
            | **CHA** | 17 | +3  | +3   |

            | Druid Level | Known Forms | Max CR | Fly Speed |
            |-------------|-------------|--------|-----------|
            | 2           | 4           | 1/4    | No        |
            | 4           | 6           | 1/2    | No        |
            | 8           | 8           | 1      | Yes       |

            | 1d100 | Size          | Capacity | Fly Speed |
            |-------|---------------|----------|-----------|
            | 01–20 | 3 ft. × 5 ft. | 200 lb.  | 80 feet   |
            | 21–55 | 4 ft. × 6 ft. | 400 lb.  | 60 feet   |
            | 56–80 | 5 ft. × 7 ft. | 600 lb.  | 40 feet   |
            | 81–00 | 6 ft. × 9 ft. | 800 lb.  | 30 feet   |
        """)

        assert text == self.run_text_through_filter(clean_detabulate_mixed_stats, text)

    def test_filtering(self):
        text = dedent("""\
            | | | MOD SAVE | | | MOD SAVE | | | MOD SAVE |
            |---|---|---------|---|---|---------|---|---|---------|
            | Str19 | +4 +4 || Dex 10 | +0 | +0 | Con 16 | +3 | +3 |
            | Int 12 | +1 | +1 | Wis 15 | +2 | +2 | Cha 17 | +3 | +3 |

            ### **Storm Giant**

            *Huge Giant, Chaotic Good*

            | AC 16                                                       | Initiative +7 (17)   |    |                       |                                              |    |     |        |    |          |  |  |
            |-------------------------------------------------------------|----------------------|----|-----------------------|----------------------------------------------|----|-----|--------|----|----------|--|--|
            | HP 230 (20d12 + 100)                                        |                      |    |                       |                                              |    |     |        |    |          |  |  |
            | Speed 50 ft., Fly 25 ft. (hover), Swim 50 ft.               |                      |    |                       |                                              |    |     |        |    |          |  |  |
            |                                                             | MOD SAVE MOD SAVE |    |                       |                                              |    |     |        |    | MOD SAVE |  |  |
            | Str 29                                                      |                      | +9 | +14                   | Dex 14                                       | +2 | +2  | Con 20 | +5 | +10      |  |  |
            | Int                                                         | 16                   | +3 | +3                    | Wis 20                                    | +5 | +10 | Cha 18 | +4 | +9       |  |  |
            | Skills Arcana +8, Athletics +14, History +8, Perception +10 |                      |    |                       |                                              |    |     |        |    |          |  |  |
            | Resistances Cold                                            |                      |    |                       |                                              |    |     |        |    |          |  |  |
            | Immunities Lightning, Thunder                               |                      |    |                       |                                              |    |     |        |    |          |  |  |
            |                                                             |                      |    |                       | Senses Darkvision 120 ft., Truesight 30 ft.; |    |     |        |    |          |  |  |
            |                                                             |                      |    | Passive Perception 20 |                                              |    |     |        |    |          |  |  |

            **Languages** Common, Giant **CR** 13 (XP 10,000; PB +5)

            # **Gold Dragon Wyrmling**

            *Medium Dragon (Metallic), Lawful Good*

            | AC 17 | Initiative +4 (14)                    |
            |-------|---------------------------------------|
            |       | HP 60 (8d8 + 24)                      |
            |       | Speed 30 ft., Fly 60 ft., Swim 30 ft. |

            |        |    |    | MOD SAVE |           |    | MOD SAVE |        | MOD SAVE |    |
            |--------|----|----|----------|-----------|----|----------|--------|----------|----|
            | Str 19 |    | +4 | +4       | Dex 14    | +2 | +4       | Con 17 | +3       | +3 |
            | Int    | 14 | +2 | +2       | Wis 11 | +0 | +2       | Cha 16 | +3       | +3 |

            - **Speed** 0 ft., fly 50 ft. (hover)

            | STR     | DEX     | CON     | INT    | WIS    | CHA    |
            |---------|---------|---------|--------|--------|--------|
            | 12 (+1) | 15 (+2) | 11 (+0) | 1 (-5) | 5 (-3) | 1 (-5) |

            - **Saving Throws** Dex +4
            - **Damage Immunities** poison, psychic
        """)
        expected = dedent("""\
            **Str** 19 +4 +4
            **Dex** 10 +0 +0
            **Con** 16 +3 +3
            **Int** 12 +1 +1
            **Wis** 15 +2 +2
            **Cha** 17 +3 +3

            ### **Storm Giant**

            *Huge Giant, Chaotic Good*

            **AC** 16
            **Initiative** +7 (17)
            **HP** 230 (20d12 + 100)
            **Speed** 50 ft., Fly 25 ft. (hover), Swim 50 ft.
            **Str** 29 +9 +14
            **Dex** 14 +2 +2
            **Con** 20 +5 +10
            **Int** 16 +3 +3
            **Wis** 20 +5 +10
            **Cha** 18 +4 +9
            **Skills** Arcana +8, Athletics +14, History +8, Perception +10
            **Resistances** Cold
            **Immunities** Lightning, Thunder
            **Senses** Darkvision 120 ft., Truesight 30 ft.; Passive Perception 20

            **Languages** Common, Giant **CR** 13 (XP 10,000; PB +5)

            # **Gold Dragon Wyrmling**

            *Medium Dragon (Metallic), Lawful Good*

            **AC** 17
            **Initiative** +4 (14)
            **HP** 60 (8d8 + 24)
            **Speed** 30 ft., Fly 60 ft., Swim 30 ft.

            **Str** 19 +4 +4
            **Dex** 14 +2 +4
            **Con** 17 +3 +3
            **Int** 14 +2 +2
            **Wis** 11 +0 +2
            **Cha** 16 +3 +3

            - **Speed** 0 ft., fly 50 ft. (hover)

            **Str** 12 +1 +1
            **Dex** 15 +2 +2
            **Con** 11 +0 +0
            **Int** 1 -5 -5
            **Wis** 5 -3 -3
            **Cha** 1 -5 -5

            - **Saving Throws** Dex +4
            - **Damage Immunities** poison, psychic
        """)

        assert expected == self.run_text_through_filter(clean_detabulate_mixed_stats, text)
        assert expected == self.run_text_through_filter(clean_detabulate_mixed_stats, expected)
