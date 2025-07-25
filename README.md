5e documents in Markdown
========================

The fifth edition reference documents that have been released under
[Creative Commons Attribution 4.0 International License \("CC-BY-4.0"\)][cc],
reformatted into Markdown.

[cc]: https://creativecommons.org/licenses/by/4.0/

Other than altering the form from PDF to Markdown, no changes have been made
to any text.


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

```
cp dnd/51/SRD_CC_v5.1.md dnd/51/breakdown.md \
  && ./breakdown.sh dnd/51/breakdown.md \
  && ./compare.sh dnd/51/breakdown.md dnd/51/SRD_CC_v5.1.md
```

### Clean the Markdown

Run the cleaning script:

```
python clean_srd.py dnd/51/SRD_CC_v5.1.md
```

When changing the source by hand and lines are added/removed, run:

```
./alter_breakdown.sh dnd/51/breakdown.txt /black_tentacles 2
```

to add/subtract to all line boundaries from the section matching
`/black_tentacles`.
