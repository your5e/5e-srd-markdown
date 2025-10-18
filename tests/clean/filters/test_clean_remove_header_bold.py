from textwrap import dedent
from clean_srd import clean_remove_header_bold
from . import TestFilter


class TestCleanRemoveHeaderBold(TestFilter):
    def test_unmatching_text_passed_through(self):
        text = dedent("""\
            # Legal Information

            The System Reference Document 5.1 is provided to you free of charge under the terms of the Creative Commons [Attribution 4.0 International License ("CC-BY-4.0"). You are free](https://creativecommons.org/licenses/by/4.0/legalcode) to use this content in any manner permitted by that license as long as you include the following attribution statement in your own work:
        """)

        assert text == self.run_text_through_filter(clean_remove_header_bold, text)

    def test_filtering(self):
        text = dedent("""\
            ### **Languages**

            By virtue of your race, your character can speak, read, and write certain languages.

            #### **Subraces**

            Some races have subraces. Members of a subrace have the traits of the parent race in addition to the traits specified for their subrace. Relationships among subraces vary significantly from race to race and world to world.
        """)
        expected = dedent("""\
            ### Languages

            By virtue of your race, your character can speak, read, and write certain languages.

            #### Subraces

            Some races have subraces. Members of a subrace have the traits of the parent race in addition to the traits specified for their subrace. Relationships among subraces vary significantly from race to race and world to world.
        """)

        assert expected == self.run_text_through_filter(clean_remove_header_bold, text)
        assert expected == self.run_text_through_filter(clean_remove_header_bold, expected)
