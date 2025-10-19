from textwrap import dedent
from clean_srd import warn_linebreaks
from . import TestFilter


class TestWarnLinebreaks(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            A churning storm cloud forms for the duration, centered on a point within range and spreading to a radius of 300 feet. Each creature under the cloud when it appears must succeed on a Constitution saving throw or take 2d6 Thunder damage and have the Deafened condition for the duration.

            At the start of each of your later turns, the storm produces different effects, as detailed below.

            - **Object Creation.** You create one object of up to 25,000 GP in value that isn't a magic item. The object can be no more than 300 feet in any dimension, and it appears in an unoccupied space that you can see on the ground.
            - **Instant Health.** You allow yourself and up to twenty creatures that you can see to regain all Hit Points, and you end all effects on them listed in the _Greater Restoration_ spell.
            - **Resistance.** You grant up to ten creatures that you can see Resistance to one damage type that you choose. This Resistance is permanent.

            | Abbreviation   | Stands For          |
            |----------------|---------------------|
            | AC             | Armor Class         |
            | C              | Concentration       |
            | CE             | Chaotic Evil        |
            | CG             | Chaotic Good        |

            1. **Roll 1d20.** You always want to roll high. If the roll has Advantage or Disadvantage (described later in "Playing the Game"), you roll two d20s, but you use the number from only one of them the higher one if you have Advantage or the lower one if you have Disadvantage.
            2. **Add Modifiers.** Add these modifiers to the number rolled on the d20:
                - **The Relevant Ability Modifier.** "Playing the Game" and "Rules Glossary" explain which ability modifiers to use for various D20 Tests.
                - **Your Proficiency Bonus If Relevant.** Each creature has a Proficiency Bonus, a number added when making a D20 Test that uses something, such as a skill, in which the creature has proficiency. See "Proficiency" later in "Playing the Game."
                - **Circumstantial Bonuses and Penalties.** A class feature, a spell, or another rule might give a bonus or penalty to the die roll.
            3. **Compare the Total to a Target Number.** If the total of the d20 and its modifiers equals or exceeds the target number, the D20 Test succeeds. Otherwise, it fails. The Game Master determines target numbers and tells players whether their rolls are successful. The target number for an ability check or a saving throw is called a Difficulty Class (DC). The target number for an attack roll is called an Armor Class (AC), which appears on a character sheet or in a stat block (see "Rules Glossary").

        """)

        assert not self.check_text_for_warning(warn_linebreaks, text)

    def test_warning(self):
        text = dedent("""\
            A churning storm cloud forms for the duration, centered on a point within range and spreading to a radius of 300 feet. Each creature under the cloud when it appears must succeed on a Constitution saving throw or take 2d6 Thunder damage and have the Deafened condition for the duration.
            At the start of each of your later turns, the storm produces different effects, as detailed below.
        """)
        assert self.check_text_for_warning(warn_linebreaks, text)

        text = dedent("""\
            **AC** 13
            **Initiative** +1 (11)
            **HP** 67 (9d8 + 27)
            **Speed** 30 ft.
        """)
        assert self.check_text_for_warning(warn_linebreaks, text)

        text = dedent("""\
            The three main pillars of D&D play are social interaction, exploration, and combat. Whichever one you're experiencing, the game unfolds according to this basic pattern:
            1. **The Game Master Describes a Scene.** The GM tells the players where their adventurers are and what's around them (how many doors lead out of a room, what's on a table, and so on).
            2. **The Players Describe What Their Characters Do.** Typically, the characters stick together as they travel through a dungeon or another environment. Sometimes different adventurers do different things: one adventurer might search a treasure chest while a second examines a mysterious symbol engraved on a wall and a third keeps watch for monsters. Outside combat, the GM ensures that every character has a chance to act and decides how to resolve their activity. In combat, the characters take turns.
            3. **The GM Narrates the Results of the Adventurers' Actions.** Sometimes resolving a task is easy. If an adventurer walks across a room and tries to open a door, the GM might say the door opens and describe what lies beyond. But the door might be locked, the floor might hide a trap, or some other circumstance might make it challenging for an adventurer to complete a task. In those cases, the GM might ask the player to roll a die to help determine what happens. Describing the results often leads to another decision point, which brings the game back to step 1.
        """)
        assert self.check_text_for_warning(warn_linebreaks, text)

        text = dedent("""\
            - **Skills** Athletics +10, Performance +5
            **Gear** Shield, Spears (3), Studded Leather Armor
            - **Senses** Passive Perception 11
            - **Languages** Common
            - **CR** 5 (XP 1,800; PB +3)
        """)
        assert self.check_text_for_warning(warn_linebreaks, text)
