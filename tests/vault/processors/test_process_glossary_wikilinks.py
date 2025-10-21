from textwrap import dedent

from update_vault import process_glossary_wikilinks
from . import TestFilter


class TestProcessGlossaryWikilinks(TestFilter):
    def test_unprocessed_text(self):
        text = dedent("""\
            - **AC** 17
            - **Initiative** +7 (17)
            - **HP** 150 (20d10 + 40)
            - **Speed** 10 ft., Swim 40 ft.

            _**Consume Memories.**_ _Intelligence Saving Throw:_ DC 16, one creature within 30 feet that is [[Charmed]] or [[Grappled]] by the aboleth. _Failure:_ 10 (3d6) Psychic damage. _Success:_ Half damage. _Failure or Success:_ The aboleth gains the target's memories if the target is a Humanoid and is reduced to 0 [[Hit Points]] by this action.

            _**Dominate Mind (2/Day).**_ _Wisdom Saving Throw:_ DC 16, one creature the aboleth can see within 30 feet. _Failure:_ The target has the [[Charmed]] condition until the aboleth dies or is on a different plane of existence from the target. While Charmed, the target acts as an ally to the aboleth and is under its control while within 60 feet of it. In addition, the aboleth and the target can communicate telepathically with each other over any distance.

            _**Bite.**_ _Melee Attack Roll:_ +5, reach 5 ft. _Hit:_ 10 (2d6 + 3) Piercing damage plus 7 (2d6) Poison damage.

            | Class                                        | Hit Points per Level   |
            |----------------------------------------------|------------------------|
            | Barbarian                                    | 7 + Con. modifier      |
            | Fighter, Paladin, or Ranger                  | 6 + Con. modifier      |
            | Bard, Cleric, Druid, Monk, Rogue, or Warlock | 5 + Con. modifier      |
            | Sorcerer or Wizard                           | 4 + Con. modifier      |

            | Primary Ability            | Intelligence                                                                                                       |
            |----------------------------|--------------------------------------------------------------------------------------------------------------------|
            | Hit Point Die              | D6 per Wizard level                                                                                                |
            | Saving Throw Proficiencies | Intelligence and Wisdom                                                                                            |
            | Skill Proficiencies        | Choose 2: Arcana, History, In sight, Investigation, Medicine, Nature, or Religion                                  |
            | Weapon Proficiencies       | Simple weapons                                                                                                     |
            | Armor Training             | None                                                                                                               |
            | Starting Equipment         | Choose A or B: (A) 2 Daggers, Arcane Focus (Quarterstaff), Robe, Spellbook, Scholar's Pack, and 5 GP; or (B) 55 GP |

            #### Criminal

            - **Ability Scores:** Dexterity, Constitution, Intelligence
            - **Feat:** Alert (see "Feats")
            - **Skill Proficiencies:** Sleight of Hand and Stealth
            - **Tool Proficiency:** Thieves' Tools
            - **Equipment:** _Choose A or B:_ (A) 2 Daggers, Thieves' Tools, Crowbar, 2 Pouches, Traveler's Clothes, 16 GP; or (B) 50 GP
        """)

        assert text == self.run_text_through_processor(
            process_glossary_wikilinks,
            text
        )

    def test_processed_text(self):
        text = dedent("""\
            - **Skills** History +12, Perception +10
            - **Senses** Darkvision 120 ft.; Passive Perception 20
            - **Languages** Deep Speech; Telepathy 120 ft.
            - **CR** 10 (XP 5,900, or 7,200 in lair; PB +4)

            _**Comet.**_ The next time you enter combat against one or more Hostile creatures, you can select one of them as your foe when you roll Initiative. If you reduce your foe to 0 Hit Points during that combat, you have Advantage on Death Saving Throws for 1 year. If someone else reduces your chosen foe to 0 Hit Points or you don't choose a foe, this card has no effect.

            A player character must make a Death Saving Throw (also called a Death Save) if they start their turn with 0 Hit Points. _See also_ "Playing the Game" ("Damage and Healing").
        """)
        expected = dedent("""\
            - **Skills** History +12, Perception +10
            - **Senses** [[Darkvision]] 120 ft.; [[Passive Perception]] 20
            - **Languages** Deep Speech; [[Telepathy]] 120 ft.
            - **CR** 10 (XP 5,900, or 7,200 in lair; PB +4)

            _**Comet.**_ The next time you enter combat against one or more [[Hostile]] creatures, you can select one of them as your foe when you roll [[Initiative]]. If you reduce your foe to 0 [[Hit Points]] during that combat, you have [[Advantage]] on [[Death Saving Throw]]s for 1 year. If someone else reduces your chosen foe to 0 Hit Points or you don't choose a foe, this card has no effect.

            A player character must make a [[Death Saving Throw]] (also called a Death Save) if they start their turn with 0 [[Hit Points]]. _See also_ "Playing the Game" ("[[Damage]] and [[Healing]]").
        """)

        assert expected == self.run_text_through_processor(
            process_glossary_wikilinks,
            text
        )
        assert expected == self.run_text_through_processor(
            process_glossary_wikilinks,
            expected
        )
