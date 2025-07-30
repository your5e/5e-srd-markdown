# List style changes

Inconsistent list style types, normally indicates indentation is missing.

- _**Roar (3/Day).**_ The sphinx emits a magical roar. Each time it roars before finishing a long rest, the roar is louder and the effect is different, as detailed below. Each creature within 500 feet of the sphinx and able to hear the roar must make a saving throw.
- **First Roar.** Each creature that fails a DC 18 Wisdom saving throw is frightened for 1 minute. A frightened creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.
- **Second Roar.** Each creature that fails a DC 18 Wisdom saving throw is deafened and frightened for 1 minute. A frightened creature is paralyzed and can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.


# Table run-on

A table that could be a run-on, but because it has headers it isn't corrected.

| Level | Proficiency | Features |
|-------|-------------|----------|
| 1st   | +2          | Rage     |

|       | Proficiency | Features      |
|-------|-------------|---------------|
| 2nd   | +2          | Reckless      |


# Mid-paragraph italic

A mid-paragraph italic that ends with a . or a : could be a mistakenly
joined line not handled by normal processing (excludes the common "Hit:"
from attacks.)

detected:
- _**Quiver.**_ A quiver can hold up to 20 arrows. - _Ram, Portable._ You can use a portable ram to break down doors. When doing so, you gain a +4 bonus on the Strength check. One other character can help you use the ram, giving you advantage on this check.

detected:
- _**Bite.** Melee Weapon Attack:_ +11 to hit, reach 10 ft., one target. _Hit:_ 17 (2d10 + 6) piercing damage. _Claw. Melee Weapon Attack:_ +11 to hit, reach 5 ft., one target. _Hit:_ 13 (2d6 + 6) slashing damage.

not detected:
- _**Bite.** Melee Weapon Attack:_ +2 to hit, reach 5 ft., one target. _Hit:_ 3 (1d6) piercing damage.

# Unusual unicode

Some unicode (weird whitespace, using minus `−` instead of hyphen `-`)
is automatically replaced. Anything else that is out of the ordinary,
(such as `⁵`) is flagged.
