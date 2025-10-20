from textwrap import dedent
from clean_srd import warn_lowercase_start
from . import TestFilter


class TestWarnTableRunon(TestFilter):
    def test_no_warning(self):
        text = dedent("""\
            Your Proficiency Bonus can't be added to a die roll or another number more than once. For example, if a rule allows you to make a Charisma (Deception or Persuasion) check, you add your Proficiency Bonus if you're proficient in either skill, but you don't add it twice if you're proficient in both skills.

            Occasionally, a Proficiency Bonus might be multiplied or divided (doubled or halved, for example) before being added. For example, the Expertise feature (see "Rules Glossary") doubles the Proficiency Bonus for certain ability checks. Whenever the bonus is used, it can be multiplied only once and divided only once.
        """)

        assert not self.check_text_for_warning(warn_lowercase_start, text)

    def test_warning(self):
        text = dedent("""\
            If you lose your spellbook, you can use the same procedure to transcribe the Wizard spells that you have prepared into a new spellbook. Filling out the remainder of the new book requires you to find new spells to do so. For this reason, many wizards keep a backup spellbook.

            of your career, you gain each of your subclass's features that are of your Wizard level or lower.
        """)

        assert self.check_text_for_warning(warn_lowercase_start, text)
