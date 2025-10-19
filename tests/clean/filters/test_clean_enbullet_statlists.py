from textwrap import dedent
from clean_srd import clean_enbullet_statlists
from . import TestFilter


class TestCleanEnbulletStatblocks(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            # Sack

            **Cost:** 1 CP

            A Sack holds up to 30 pounds within 1 cubic foot.

            #### Assassin's Blood

            **Cost:** 150 GP

            _Ingested Poison_

            A creature subjected to Assassin's Blood makes a DC 10 Constitution saving throw. On a failed save, the creature takes 6 (1d12) Poison damage and has the Poisoned condition for 24 hours. On a successful save, the creature takes half as much damage only.
        """)

        assert text == self.run_text_through_filter(clean_enbullet_statlists, text)

    def test_filtering(self):
        text = dedent("""\
            ### Aboleth

            _Large Aberration, Lawful Evil_

            **AC** 17
            **Initiative** +7 (17)
            **HP** 150 (20d10 + 40)
            **Speed** 10 ft., Swim 40 ft.

            |                  |   Str. |   Dex. |   Con. |   Int. |   Wis. |   Cha. |
            |------------------|--------|--------|--------|--------|--------|--------|
            | **Score**        |     21 |      9 |     15 |     18 |     15 |     18 |
            | **Modifier**     |     +5 |     -1 |     +2 |     +4 |     +2 |     +4 |
            | **Saving Throw** |     +5 |     +3 |     +6 |     +8 |     +6 |     +4 |

            **Skills** History +12, Perception +10
            **Senses** Darkvision 120 ft.; Passive Perception 20
            **Languages** Deep Speech; telepathy 120 ft.
            **CR** 10 (XP 5,900, or 7,200 in lair; PB +4)

            ### Arcane Lock

            _Level 2 Abjuration (Wizard)_

            **Casting Time:** Action
            **Range:** Touch
            **Components:** V, S, M (gold dust worth 25+ GP, which the spell consumes)
            **Duration:** Until dispelled

            You touch a closed door, window, gate, container, or hatch and magically lock it for the duration. This lock can't be unlocked by any nonmagical means. You and any creatures you designate when you cast the spell can open and close the object despite the lock. You can also set a password that, when spoken within 5 feet of the object, unlocks it for 1 minute.

            # Alchemist's Supplies

            **Cost:** 50 GP
            **Ability:** Intelligence
            **Weight:** 8 lb.
            **Utilize:** Identify a substance (DC 15), or start a fire (DC 15)
            **Craft:** Acid, Alchemist's Fire, Component Pouch, Oil, Paper, Perfume

            #### Acolyte

            **Ability Scores:** Intelligence, Wisdom, Charisma
            **Feat:** Magic Initiate (Cleric) (see "Feats")
            **Skill Proficiencies:** Insight and Religion
            **Tool Proficiency:** Calligrapher's Supplies
            **Equipment:** _Choose A or B:_ (A) Calligrapher's Supplies, Book (prayers), Holy Symbol, Parchment (10 sheets), Robe, 8 GP; or (B) 50 GP

            #### Gnome

            **Creature Type:** Humanoid
            **Size:** Small (about 3-4 feet tall)
            **Speed:** 30 feet

        """)
        expected = dedent("""\
            ### Aboleth

            _Large Aberration, Lawful Evil_

            - **AC** 17
            - **Initiative** +7 (17)
            - **HP** 150 (20d10 + 40)
            - **Speed** 10 ft., Swim 40 ft.

            |                  |   Str. |   Dex. |   Con. |   Int. |   Wis. |   Cha. |
            |------------------|--------|--------|--------|--------|--------|--------|
            | **Score**        |     21 |      9 |     15 |     18 |     15 |     18 |
            | **Modifier**     |     +5 |     -1 |     +2 |     +4 |     +2 |     +4 |
            | **Saving Throw** |     +5 |     +3 |     +6 |     +8 |     +6 |     +4 |

            - **Skills** History +12, Perception +10
            - **Senses** Darkvision 120 ft.; Passive Perception 20
            - **Languages** Deep Speech; telepathy 120 ft.
            - **CR** 10 (XP 5,900, or 7,200 in lair; PB +4)

            ### Arcane Lock

            _Level 2 Abjuration (Wizard)_

            - **Casting Time:** Action
            - **Range:** Touch
            - **Components:** V, S, M (gold dust worth 25+ GP, which the spell consumes)
            - **Duration:** Until dispelled

            You touch a closed door, window, gate, container, or hatch and magically lock it for the duration. This lock can't be unlocked by any nonmagical means. You and any creatures you designate when you cast the spell can open and close the object despite the lock. You can also set a password that, when spoken within 5 feet of the object, unlocks it for 1 minute.

            # Alchemist's Supplies

            - **Cost:** 50 GP
            - **Ability:** Intelligence
            - **Weight:** 8 lb.
            - **Utilize:** Identify a substance (DC 15), or start a fire (DC 15)
            - **Craft:** Acid, Alchemist's Fire, Component Pouch, Oil, Paper, Perfume

            #### Acolyte

            - **Ability Scores:** Intelligence, Wisdom, Charisma
            - **Feat:** Magic Initiate (Cleric) (see "Feats")
            - **Skill Proficiencies:** Insight and Religion
            - **Tool Proficiency:** Calligrapher's Supplies
            - **Equipment:** _Choose A or B:_ (A) Calligrapher's Supplies, Book (prayers), Holy Symbol, Parchment (10 sheets), Robe, 8 GP; or (B) 50 GP

            #### Gnome

            - **Creature Type:** Humanoid
            - **Size:** Small (about 3-4 feet tall)
            - **Speed:** 30 feet

        """)

        assert expected == self.run_text_through_filter(clean_enbullet_statlists, text)
        assert expected == self.run_text_through_filter(clean_enbullet_statlists, expected)
