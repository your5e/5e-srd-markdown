from textwrap import dedent
from clean_srd import clean_spell_list_emphasis
from . import TestFilter


class TestCleanSpellListEmphasis(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ### **Flame Tongue**

            #### *Weapon (Any Melee Weapon), Rare (Requires Attunement)*

            While holding this magic weapon, you can take a Bonus Action and use a command word to cause flames to engulf the damage-dealing part of the weapon. These flames shed Bright Light in a 40 foot radius and Dim Light for an additional 40 feet. While the weapon is ablaze, it deals an extra 2d6 Fire damage on a hit. The flames last until you take a Bonus Action to issue the command again or until you drop, stow, or sheathe the weapon.
        """)

        assert text == self.run_text_through_filter(clean_spell_list_emphasis, text)

    def test_filtering(self):
        text = dedent("""\
            | Spell            | School        | Special   |
            |------------------|---------------|-----------|
            | Chill Touch      | Necromancy    | —         |
            | Eldritch Blast   | Evocation     | —         |
            | Mage Hand        | Conjuration   | —         |
            | Minor Illusion   | Illusion      | —         |
            | Poison Spray     | Necromancy    | —         |
            | Prestidigitation | Transmutation | —         |
            | True Strike      | Divination    | —         |

            |   Druid Level | Circle Spells                  |
            |---------------|--------------------------------|
            |             3 | Blur, Burning Hands, Fire Bolt |
            |             5 | Fireball                       |
            |             7 | Blight                         |
            |             9 | Wall of Stone                  |

            |   Cleric Level | Prepared Spells                             |
            |----------------|---------------------------------------------|
            |              3 | Aid, Bless, Cure Wounds, Lesser Restoration |
            |              5 | Mass Healing Word, Revivify                 |
            |              7 | Aura of Life, Death Ward                    |
            |              9 | Greater Restoration, Mass Cure Wounds       |

            | Spell                         | Charge Cost |
            |-------------------------------|-------------|
            | Cure Wounds (level 9 version) | 4           |
            | Daylight                      | 1           |
            | Death Ward                    | 2           |
            | Detect Magic                  | 0           |
            | Scrying (save DC 18)          | 3           |

            | 1d20  | Bead                 | Spell                         |
            |-------|----------------------|-------------------------------|
            | 1–6   | Bead of Blessing     | Bless                         |
            | 7–12  | Bead of Curing       | Cure Wounds (level 2 version) |
            | 13–16 | Bead of Favor        | Greater Restoration           |
            | 17–18 | Bead of Smiting      | Shining Smite                 |
            | 19    | Bead of Summons      | Guardian of Faith             |
            | 20    | Bead of Wind Walking | Wind Walk                     |

            | Original Spell | Becomes Spell  |
            |----------------|----------------|
            | Cure Wounds    | Inflict Wounds |
        """)
        expected = dedent("""\
            | Spell            | School        | Special   |
            |------------------|---------------|-----------|
            |*Chill Touch*| Necromancy    | —         |
            |*Eldritch Blast*| Evocation     | —         |
            |*Mage Hand*| Conjuration   | —         |
            |*Minor Illusion*| Illusion      | —         |
            |*Poison Spray*| Necromancy    | —         |
            |*Prestidigitation*| Transmutation | —         |
            |*True Strike*| Divination    | —         |

            |   Druid Level | Circle Spells                  |
            |---------------|--------------------------------|
            |             3 |*Blur*, *Burning Hands*, *Fire Bolt*|
            |             5 |*Fireball*|
            |             7 |*Blight*|
            |             9 |*Wall of Stone*|

            |   Cleric Level | Prepared Spells                             |
            |----------------|---------------------------------------------|
            |              3 |*Aid*, *Bless*, *Cure Wounds*, *Lesser Restoration*|
            |              5 |*Mass Healing Word*, *Revivify*|
            |              7 |*Aura of Life*, *Death Ward*|
            |              9 |*Greater Restoration*, *Mass Cure Wounds*|

            | Spell                         | Charge Cost |
            |-------------------------------|-------------|
            |*Cure Wounds* (level 9 version)| 4           |
            |*Daylight*| 1           |
            |*Death Ward*| 2           |
            |*Detect Magic*| 0           |
            |*Scrying* (save DC 18)| 3           |

            | 1d20  | Bead                 | Spell                         |
            |-------|----------------------|-------------------------------|
            | 1–6   | Bead of Blessing     |*Bless*|
            | 7–12  | Bead of Curing       |*Cure Wounds* (level 2 version)|
            | 13–16 | Bead of Favor        |*Greater Restoration*|
            | 17–18 | Bead of Smiting      |*Shining Smite*|
            | 19    | Bead of Summons      |*Guardian of Faith*|
            | 20    | Bead of Wind Walking |*Wind Walk*|

            | Original Spell | Becomes Spell  |
            |----------------|----------------|
            |*Cure Wounds*|*Inflict Wounds*|
        """)

        assert expected == self.run_text_through_filter(clean_spell_list_emphasis, text)
