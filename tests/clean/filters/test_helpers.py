from textwrap import dedent

from clean_srd import get_table_headers


def test_get_table_headers():
    text = dedent("""\

        | Dragon   | Damage Type   | Breath Weapon                |
        |----------|---------------|------------------------------|
        | Black    | Acid          | 5 by 30 ft. line (Dex. save) |
        | Blue     | Lightning     | 5 by 30 ft. line (Dex. save) |
        | Brass    | Fire          | 5 by 30 ft. line (Dex. save) |
        | Bronze   | Lightning     | 5 by 30 ft. line (Dex. save) |
        | Copper   | Acid          | 5 by 30 ft. line (Dex. save) |
        | Gold     | Fire          | 15 ft. cone (Dex. save)      |
        | Green    | Poison        | 15 ft. cone (Con. save)      |
        | Red      | Fire          | 15 ft. cone (Dex. save)      |
        | Silver   | Cold          | 15 ft. cone (Con. save)      |
        | White    | Cold          | 15 ft. cone (Con. save)      |

        | Spell                         | Charge<br>Cost |  |
        |-------------------------------|----------------|--|
        | Cure Wounds (level 9 version) | 4              |  |
        | Daylight                      | 1              |  |
        | Death Ward                    | 2              |  |
        | Detect Magic                  | 0              |  |
        | Scrying (save DC 18)          | 3              |  |

        | Spell            | School        | Special   |
        |------------------|---------------|-----------|
        | Chill Touch      | Necromancy    | —         |
        | Eldritch Blast   | Evocation     | —         |
        | Mage Hand        | Conjuration   | —         |
        | Minor Illusion   | Illusion      | —         |
        | Poison Spray     | Necromancy    | —         |
        | Prestidigitation | Transmutation | —         |
        | True Strike      | Divination    | —         |

    """)
    lines = text.splitlines()

    assert get_table_headers(lines, 0) is None
    assert get_table_headers(lines, 1) is None
    assert get_table_headers(lines, 2) is None

    assert get_table_headers(lines, 3) == ['Dragon', 'Damage Type', 'Breath Weapon']
    assert get_table_headers(lines, 8) == ['Dragon', 'Damage Type', 'Breath Weapon']
    assert get_table_headers(lines, 12) == ['Dragon', 'Damage Type', 'Breath Weapon']

    assert get_table_headers(lines, 13) is None
    assert get_table_headers(lines, 14) is None
    assert get_table_headers(lines, 15) is None

    assert get_table_headers(lines, 16) == ['Spell', 'Charge<br>Cost', '']
    assert get_table_headers(lines, 20) == ['Spell', 'Charge<br>Cost', '']

    assert get_table_headers(lines, 21) is None
    assert get_table_headers(lines, 22) is None
    assert get_table_headers(lines, 23) is None

    assert get_table_headers(lines, 24) == ['Spell', 'School', 'Special']
    assert get_table_headers(lines, 30) == ['Spell', 'School', 'Special']

    assert get_table_headers(lines, 31) is None
