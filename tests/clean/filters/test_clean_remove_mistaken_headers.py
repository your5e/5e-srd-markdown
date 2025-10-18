from textwrap import dedent
from clean_srd import clean_remove_mistaken_headers
from . import TestFilter


class TestCleanRemoveMistakenHeaders(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            ## **Charm Person**

            *1st-level enchantment*

            **Casting Time:** 1 action **Range:** 30 feet **Components:** V, S **Duration:** 1 hour

            You attempt to charm a humanoid you can see within range. It must make a Wisdom saving throw, and does so with advantage if you or your companions are fighting it. If it fails the saving throw, it is charmed by you until the spell ends or until you or your companions do anything harmful to it. The charmed creature regards you as a friendly acquaintance. When the spell ends, the creature knows it was charmed by you.
        """)

        assert text == self.run_text_through_filter(clean_remove_mistaken_headers, text)

    def test_filtering(self):
        text = dedent("""\
            ## **Chill Touch**

            *Necromancy cantrip*

            **Casting Time:** 1 action **Range:** 120 feet

            #### **Components:** V, S **Duration:** 1 round

            You create a ghostly, skeletal hand in the space of a creature within range. Make a ranged spell attack against the creature to assail it with the chill of the grave. On a hit, the target takes 1d8 necrotic damage, and it can't regain hit points until the start of your next turn. Until then, the hand clings to the target.
        """)
        expected = dedent("""\
            ## **Chill Touch**

            *Necromancy cantrip*

            **Casting Time:** 1 action **Range:** 120 feet

            **Components:** V, S **Duration:** 1 round

            You create a ghostly, skeletal hand in the space of a creature within range. Make a ranged spell attack against the creature to assail it with the chill of the grave. On a hit, the target takes 1d8 necrotic damage, and it can't regain hit points until the start of your next turn. Until then, the hand clings to the target.
        """)

        assert expected == self.run_text_through_filter(clean_remove_mistaken_headers, text)
        assert expected == self.run_text_through_filter(clean_remove_mistaken_headers, expected)
