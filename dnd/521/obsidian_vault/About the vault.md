# About the vault

A conversion of the 5.1 SRD PDF to Markdown, then converted to an Obsidian vault.

The [original PDF used](https://github.com/your5e/5e-srd-markdown/blob/main/dnd/521/SRD_CC_v5.2.1.pdf) and the resulting [unbroken large Markdown file](https://github.com/your5e/5e-srd-markdown/blob/main/dnd/521/SRD_CC_v5.2.1.md) are available on [GitHub](https://github.com/your5e/5e-srd-markdown).

Conversion notes:

- removed the table of contents from the Markdown (where it makes no sense)
- created a version of the table of contents along with lists of spells, magic items, monsters, and animals in the Obsidian vault
- fixed numbering of steps in D20 tests (its 4, 5, 6 in the PDF, which seems to be an accidental continuation from Rhythm of Play)
- Tables and sidebars have been repositioned in the source to where they make sense, rather than preserving the original document order, and table headers (and references to them) have been removed as a result
- Corrected occurrences of "on \[the\] table" to "in \[the\] table"
- Tables are reformatted for Markdown:
    - Markdown doesn't support multiple header rows as used in many tables (eg. in class features, the spanning "spell slots per spell level"), so the text has been adjusted to be only one row
    - restructured side-by-side tables used to reduce height in the PDF, including rotating statblock tables to have the abilities in the first column
    - split tables using mid-table headers into multiple tables
    - monster ability tables have been reformatted to be in the format score/modifier/saving throw
