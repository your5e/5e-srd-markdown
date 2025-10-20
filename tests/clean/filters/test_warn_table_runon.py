from textwrap import dedent
from clean_srd import warn_table_runon
from . import TestFilter


class TestWarnTableRunon(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            | Light Armor (1 Minute to Don or Doff)   | Armor Class (AC)   | Strength   | Stealth      | Weight   | Cost   |
            |-----------------------------------------|--------------------|------------|--------------|----------|--------|
            | Padded Armor                            | 11 + Dex modifier  | —          | Disadvantage | 8 lb.    | 5 GP   |
            | Leather Armor                           | 11 + Dex modifier  | —          | —            | 10 lb.   | 10 GP  |
            | Studded Leather Armor                   | 12 + Dex modifier  | —          | —            | 13 lb.   | 45 GP  |

            | Shield (Utilize Action to Don or Doff)   |   Armor Class (AC) | Weight   | Cost   |
            |------------------------------------------|--------------------|----------|--------|
            | Shield                                   |                 +2 | 6 lb.    | 10 GP  |
        """)

        assert not self.check_text_for_warning(warn_table_runon, text)

    def test_warning(self):
        text = dedent("""\
            | Light Armor (1 Minute to Don or Doff)   | Armor Class (AC)   | Strength   | Stealth      | Weight   | Cost   |
            |-----------------------------------------|--------------------|------------|--------------|----------|--------|
            | Padded Armor                            | 11 + Dex modifier  | —          | Disadvantage | 8 lb.    | 5 GP   |
            | Leather Armor                           | 11 + Dex modifier  | —          | —            | 10 lb.   | 10 GP  |
            | Studded Leather Armor                   | 12 + Dex modifier  | —          | —            | 13 lb.   | 45 GP  |

            | Medium Armor (5 Minutes to Don and 1 Minute to Doff)   | Armor Class (AC)          | Strength   | Stealth      | Weight   | Cost   |
            |--------------------------------------------------------|---------------------------|------------|--------------|----------|--------|
            | Hide Armor                                             | 12 + Dex modifier (max 2) | —          | —            | 12 lb.   | 10 GP  |
            | Chain Shirt                                            | 13 + Dex modifier (max 2) | —          | —            | 20 lb.   | 50 GP  |
            | Scale Mail                                             | 14 + Dex modifier (max 2) | —          | Disadvantage | 45 lb.   | 50 GP  |
            | Breastplate                                            | 14 + Dex modifier (max 2) | —          | —            | 20 lb.   | 400 GP |
            | Half Plate Armor                                       | 15 + Dex modifier (max 2) | —          | Disadvantage | 40 lb.   | 750 GP |
        """)

        assert self.check_text_for_warning(warn_table_runon, text)
