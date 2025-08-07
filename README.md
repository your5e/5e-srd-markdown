5e refererences in Markdown
===========================

The fifth edition reference documents that have been released under
[Creative Commons Attribution 4.0 International License \("CC-BY-4.0"\)][cc],
reformatted into Markdown.

[cc]: https://creativecommons.org/licenses/by/4.0/

Other than as needed during the conversion from PDF to Markdown, no changes
have been made to the text, tables, or details. Any changes are noted with
the SRD in question.


- D&D 5th edition 5.1 SRD (2014)

    - [PDF](dnd/51/SRD_CC_v5.1.pdf)
    - [Markdown (untouched)](dnd/51/SRD_CC_v5.1.untouched.md)
    - [Markdown (whole)](dnd/51/SRD_CC_v5.1.md)
    - [Markdown (broken into sections)](dnd/51/markdown)

    > This work includes material taken from the System Reference Document 5.1
    > ("SRD 5.1") by Wizards of the Coast LLC and available at
    > <https://dnd.wizards.com/resources/systems-reference-document>.
    > The SRD 5.1 is licensed under the Creative Commons Attribution 4.0
    > International License available at
    > <https://creativecommons.org/licenses/by/4.0/legalcode>.

    Conversion notes:

    - Markdown doesn't support multiple header rows as used in class tables, so
      they have been compressed to one row.
    - added "Traits" header in statblocks to create a clarity separator
      between the list of skills/senses/CR etc and the list of traits
    - fixed "Components" typo in Contagion
    - changed "Petrifying Gaze" to be bold italics for consistency
    - Some tables have been broken into section to make them clearer, as
      Markdown doesn't support mid-table headers:
        - Armor types ([Armor](dnd/51/markdown/equpiment/armor.md))
        - Saddles ([Mounts and Vehicles](dnd/51/markdown/equipment/mounts_and_vehicles.md))
        - Scrying ([Scrying](dnd/51/markdown/spells/level_5/scrying.md))
        - Tack, Harness, and Drawn Vehicles ([Tools](dnd/51/markdown/equipment/tools.md))
        - Weapon types ([Weapons](dnd/51/markdown/equipment/weapons.md))
    - Re-arranged the order of the Fantasy-Historical Pantheons so that the
      table of deities appears in the description of that pantheon
    - Subclass introduction headers added to Barbarian, Bard, Cleric & Druid


## Workflow for breaking the whole SRD into sections

### Create Markdown files

Create the Markdown using [marker](https://github.com/datalab-to/marker):

    marker_single -output_dir . --output_format markdown SRD_CC_v5.1.pdf

Place the resulting Markdown to the right place (`srd/51/SRD_CC_v5.1.md`),
keep a pristine copy (`srd/51/SRD_CC_v5.1.untouched.md`), and copy it to
`breakdown.md` for processing into smaller files.

A draft breakdown is made with

```bash
initial_breakdown.sh dnd/51/SRD_CC_v5.1.md > dnd/51/breakdown.txt
```

and then refined by hand (as either `marker` detects far too many lines as
headers, or the PDF was styled poorly). While refining the breakdown, this is
run repeatedly to spot mistakes:

```bash
cp dnd/51/SRD_CC_v5.1.md dnd/51/breakdown.md \
    && ./breakdown.sh dnd/51/breakdown.md \
    && diff -u dnd/51/SRD_CC_v5.1.md <(./rebuild.sh dnd/51/breakdown.md)
```

### Clean the Markdown

Run the cleaning script:

```bash
python clean_srd.py dnd/51/SRD_CC_v5.1.md
```

If it detects any errors it cannot fix automatically, it will issue errors and
not process the file further. After reformatting the document, it will also
scan for problems that might need human intervention. Any automatic changes
will have updated the breakdown file as necessary.

When changing the source by hand and lines are added/removed, use
`alter_lines.sh` to add/subtract line boundaries from a matching
section onwards:

```bash
./alter_lines.sh -d dnd/51/ /black_tentacles -2
```

### Fix header progression

The broken down fragments of the SRD should start with a first level header.
Some fragments can be fixed automatically (most statblocks, anything with
a clear header progression), but some will have to be edited by hand.

```bash
./fix_statblock_headers.sh dnd/51/markdown/statblocks \
./fix_headers.sh dnd/51/markdown
```

The warnings from the `fix*` scripts can be piped to `edit_warnings.sh`
to open the file at the right line (in Sublime Text).

```bash
./fix_statblock_headers.sh dnd/51/markdown/statblocks \
    | ./edit_warnings.sh
```

To check, use

```bash
diff -u dnd/51/SRD_CC_v5.1.md <(./rebuild.sh dnd/51/breakdown.md)
```

### Create an Obsidian vault

Once the SRD is edited, create a copy to use as an Obsidian vault.

```bash
python update_vault.py \
    --progress \
        dnd/51/markdown \
        dnd/51/obsidian_vault
```

Some words that are also conditions (eg invisible) may be incorrectly linked.
The lines that they are on can be added to `ignore_vault.txt` so that they
won't be re-created when re-running the script:

```bash
python update_vault.py \
    --progress \
    --ignore dnd/51/ignore_vault.txt \
        dnd/51/markdown \
        dnd/51/obsidian_vault
```

And where files need to be altered after the script has run in a way that
would be overwritten (eg creating more wikilinks that would be removed again),
after editing the files, create patches:

```bash
./vault_patches.sh create dnd/51
```

that can then be restored later:

```bash
./vault_patches.sh apply dnd/51
```
