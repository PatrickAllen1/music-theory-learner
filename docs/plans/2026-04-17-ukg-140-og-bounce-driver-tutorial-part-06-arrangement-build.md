# UKG 140 OG Bounce Driver: Tutorial Part 6 - Arrangement Build

## Purpose
Teach the learner how to turn the finished lanes into a full `160`-bar arrangement.

This part is clip placement and section design.

Detailed risers, automation curves, fills, and boundary FX are handled in `Part 7`.

## Outcome
By the end of this part, the learner should have a complete rough arrangement with these exact sections:
- `1-16 Intro A`
- `17-32 Intro B`
- `33-48 Break A`
- `49-64 Drop A`
- `65-80 Drop A Lift`
- `81-96 Break B`
- `97-112 Re-entry Build`
- `113-128 Drop B`
- `129-144 Drop B Lift`
- `145-160 Outro`

The arrangement should include:
- air across the full song
- separate drum tracks placed section by section
- bass sub and bass mid placed section by section
- chord clips placed section by section
- vocal clips placed according to the new full-chorus-plus-chops plan
- a rough full-song bounce for review

## Time Estimate
- `90-150 minutes`

This is longer than a normal arrangement pass because the lesson does not assume Ableton fluency.

## Before You Start
You should already have these tracks:
- `Kick Body`
- `Kick Click`
- `Clap`
- `Closed Hat`
- `Ghost Hat`
- `Open Hat`
- `Shaker`
- `Drum Fill FX`
- `Bass Sub`
- `Bass Mid`
- `Chords`
- `Air`
- `Vocal Full Chorus`
- `Vocal Chops`
- `Vocal Throw`

If a track is missing, create it before continuing.

Do not combine the drum tracks into one rack in this tutorial.

Separate drum tracks make mixing easier later.

## Timing Language
Every position in this part is an Arrangement View position.

Examples:
- `49.1.1` means bar `49`, beat `1`, first subdivision
- `68.3.4` means bar `68`, beat `3`, fourth subdivision
- `145.1.1` means the start of the outro

When this lesson says `x.4.3`, `x` means the current bar.

Example:
- in bar `48`, `x.4.3` means `48.4.3`

## Step 1: Create The 10 Locators
### Action
Switch to Arrangement View.

Create these locators exactly:
1. `1.1.1` -> `1-16 Intro A`
2. `17.1.1` -> `17-32 Intro B`
3. `33.1.1` -> `33-48 Break A`
4. `49.1.1` -> `49-64 Drop A`
5. `65.1.1` -> `65-80 Drop A Lift`
6. `81.1.1` -> `81-96 Break B`
7. `97.1.1` -> `97-112 Re-entry Build`
8. `113.1.1` -> `113-128 Drop B`
9. `129.1.1` -> `129-144 Drop B Lift`
10. `145.1.1` -> `145-160 Outro`

How to create a locator in Ableton:
1. Click the timeline ruler at the target bar.
2. Right-click the ruler.
3. Choose `Add Locator`.
4. Click the locator name.
5. Press `Cmd+R` / `Ctrl+R`.
6. Type the exact name.
7. Press `Enter`.

If your Ableton version does not let you color locators, skip colors.

Names matter more than colors.

### Checkpoint
Read the locator names left to right.

There must be exactly `10`.

## Step 2: Place The Air Lane
### Action
The `Air` track should run quietly through the whole song.

1. Put the `Air` clip at `1.1.1`.
2. The first copy should run from `1.1.1` to `5.1.1`.
3. Select that clip.
4. Press `Cmd+D` / `Ctrl+D` until the last copy reaches `161.1.1`.

That means the air covers:
- `1.1.1-161.1.1`

If it is loud like rain:
- lower the `Air` fader
- keep it barely audible
- do not delete it

### Why
The air is the ceiling of the record.

It should be felt more than heard.

## Step 3: Place The Drums
### Action
Use the separate drum tracks from Part `2`.

If you already created `16`-bar drum clips in Part `2`, use those.

If you do not have them, create empty MIDI clips in the listed ranges and program the patterns described below.

### Drum Pattern Translation
`Four-on-the-floor` means:
- every bar has kick hits at `x.1.1`, `x.2.1`, `x.3.1`, `x.4.1`

`Clap on 2 and 4` means:
- every bar has clap hits at `x.2.1` and `x.4.1`

`Closed Hat offbeats` means:
- every bar has closed-hat hits at `x.1.3`, `x.2.3`, `x.3.3`, `x.4.3`

`Starter ghost hats` means:
- every bar has ghost hits at `x.2.2`, `x.2.4`, `x.4.2`, `x.4.4`
- after placing them, nudge them late as taught in Part `2`

`Shaker 1/8` means:
- every bar has shaker hits at `x.1.1`, `x.1.3`, `x.2.1`, `x.2.3`, `x.3.1`, `x.3.3`, `x.4.1`, `x.4.3`

### 3A: Intro A Drums, `1.1.1-17.1.1`
Place:
- `Kick Body`: four-on-the-floor from `1.1.1-17.1.1`
- `Kick Click`: same MIDI as `Kick Body`
- `Clap`: empty from `1.1.1-9.1.1`, then clap on 2 and 4 from `9.1.1-17.1.1`
- `Closed Hat`: offbeats from `1.1.1-17.1.1`
- `Ghost Hat`: empty from `1.1.1-9.1.1`, then starter ghost hats from `9.1.1-17.1.1`
- `Open Hat`: empty
- `Shaker`: empty from `1.1.1-9.1.1`, then shaker 1/8 from `9.1.1-17.1.1`
- `Drum Fill FX`: short fill at `16.4.3` and `16.4.4`

### 3B: Intro B Drums, `17.1.1-33.1.1`
Place:
- `Kick Body`: four-on-the-floor
- `Kick Click`: same MIDI as `Kick Body`
- `Clap`: clap on 2 and 4
- `Closed Hat`: offbeats
- `Ghost Hat`: starter ghost hats
- `Open Hat`: empty from `17.1.1-25.1.1`, then one open hat at `x.4.3` from bars `25-32`
- `Shaker`: shaker 1/8
- `Drum Fill FX`: short fill at `32.4.3` and `32.4.4`

### 3C: Break A Drums, `33.1.1-49.1.1`
This is the first vocal-introduction section.

Do not make it a full drop.

Place:
- `Kick Body`: empty from `33.1.1-41.1.1`, then one kick at `41.1.1`, `43.1.1`, `45.1.1`, `47.1.1`
- `Kick Click`: same as `Kick Body`, or empty if the break gets too sharp
- `Clap`: empty
- `Closed Hat`: sparse offbeat hits at `41.4.3`, `43.4.3`, `45.4.3`, `47.4.3`
- `Ghost Hat`: empty
- `Open Hat`: empty
- `Shaker`: very quiet 1/8 from `41.1.1-49.1.1`, or empty if the vocal needs more space
- `Drum Fill FX`: pre-drop fill at `48.4.3` and `48.4.4`

### 3D: Drop A Drums, `49.1.1-65.1.1`
This is the first full drop with the intact chorus.

Place:
- `Kick Body`: four-on-the-floor
- `Kick Click`: same MIDI as `Kick Body`
- `Clap`: clap on 2 and 4
- `Closed Hat`: offbeats
- `Ghost Hat`: starter ghost hats
- `Open Hat`: `x.4.3` as the priority open-hat placement
- `Shaker`: shaker 1/8, not too loud
- `Drum Fill FX`: short fill at `64.4.3` and `64.4.4`

Keep drums strong but not busier than the chorus.

### 3E: Drop A Lift Drums, `65.1.1-81.1.1`
Duplicate `Drop A` drums, then add lift density:
- `Ghost Hat`: add extra ghost hits on `x.1.2` and `x.3.4` from bars `73-80`
- `Open Hat`: add `x.2.3` from bars `73-80`
- `Shaker`: raise velocity slightly from bars `73-80`
- `Drum Fill FX`: fill at `80.4.3` and `80.4.4`

Do not change the kick pattern.

### 3F: Break B Drums, `81.1.1-97.1.1`
This is the darker second break.

Place:
- `Kick Body`: empty from `81.1.1-89.1.1`, then one kick at `89.1.1`, `91.1.1`, `93.1.1`, `95.1.1`
- `Kick Click`: same as `Kick Body`, or empty
- `Clap`: empty
- `Closed Hat`: sparse hits at `89.4.3`, `91.4.3`, `93.4.3`, `95.4.3`
- `Ghost Hat`: empty
- `Open Hat`: empty
- `Shaker`: very quiet 1/8 from `89.1.1-97.1.1`
- `Drum Fill FX`: fill at `96.4.3` and `96.4.4`

### 3G: Re-entry Build Drums, `97.1.1-113.1.1`
Place:
- `Kick Body`: four-on-the-floor
- `Kick Click`: same MIDI as `Kick Body`
- `Clap`: empty from `97.1.1-105.1.1`, then clap on 2 and 4 from `105.1.1-113.1.1`
- `Closed Hat`: offbeats
- `Ghost Hat`: starter ghost hats from `101.1.1-113.1.1`
- `Open Hat`: empty from `97.1.1-109.1.1`, then `109.4.3`, `110.4.3`, `111.4.3`, `112.4.3`
- `Shaker`: empty from `97.1.1-105.1.1`, then shaker 1/8 from `105.1.1-113.1.1`
- `Drum Fill FX`: pre-drop fill at `112.4.3` and `112.4.4`

### 3H: Drop B Drums, `113.1.1-129.1.1`
Use the same core as `Drop A`, but allow a little more top support:
- `Kick Body`: four-on-the-floor
- `Kick Click`: same MIDI as `Kick Body`
- `Clap`: clap on 2 and 4
- `Closed Hat`: offbeats
- `Ghost Hat`: starter ghost hats
- `Open Hat`: `x.4.3`; add `x.2.3` only if the chorus still has space
- `Shaker`: shaker 1/8
- `Drum Fill FX`: fill at `128.4.3` and `128.4.4`

### 3I: Drop B Lift Drums, `129.1.1-145.1.1`
Use the densest drop drums:
- same as `Drop A Lift`
- fill at `144.4.3` and `144.4.4`

### 3J: Outro Drums, `145.1.1-161.1.1`
Place:
- `Kick Body`: four-on-the-floor from `145.1.1-161.1.1`
- `Kick Click`: same MIDI as `Kick Body`
- `Clap`: clap on 2 and 4 from `145.1.1-153.1.1`, then empty
- `Closed Hat`: offbeats from `145.1.1-161.1.1`
- `Ghost Hat`: starter ghosts from `145.1.1-153.1.1`, then empty
- `Open Hat`: empty
- `Shaker`: shaker 1/8 from `145.1.1-153.1.1`, then empty
- `Drum Fill FX`: empty

## Step 4: Place The Bass
### Action
Use `Bass Sub` and `Bass Mid`.

Most sections use the same MIDI timing on both tracks.

If `Bass Mid` gets muddy on low notes:
- keep the low note on `Bass Sub`
- use the octave-up version on `Bass Mid`
- example: `Bb1` on sub, `Bb2` on mid

### Bass Placement By Section
`Intro A`, `1.1.1-17.1.1`:
- leave bass empty

`Intro B`, `17.1.1-33.1.1`:
- use the teaser pattern from Part `3`
- copy it across the full range

`Break A`, `33.1.1-49.1.1`:
- mostly empty
- optional filtered root reminders only:
  - `D2` at `41.1.1-41.3.1`
  - `Bb1` at `43.1.1-43.3.1`
  - `F2` at `45.1.1-45.3.1`
  - `C2` at `47.1.1-47.3.1`

`Drop A`, `49.1.1-65.1.1`:
- place the full rolling bass clip from Part `3`
- copy the `4`-bar loop across `49.1.1-65.1.1`
- keep it supporting the full chorus

`Drop A Lift`, `65.1.1-81.1.1`:
- duplicate the `Drop A` bass
- do not add new pitches
- if you need lift, use tone/filter movement, not more notes

`Break B`, `81.1.1-97.1.1`:
- use sparse root reminders like `Break A`
- keep bass lower than the vocal and chords

`Re-entry Build`, `97.1.1-113.1.1`:
- use the filtered teaser bass
- make it more urgent than `Intro B`
- do not reveal a second bassline

`Drop B`, `113.1.1-129.1.1`:
- use the full rolling bass again
- same root path as `Drop A`
- do not add a second melodic bass

`Drop B Lift`, `129.1.1-145.1.1`:
- duplicate `Drop B`
- allow stronger phrase-end releases if already written in Part `3`

`Outro`, `145.1.1-161.1.1`:
- reduce to root implication or sparse bass
- keep it DJ-safe

## Step 5: Place The Chords
### Action
Use the chord clips from Part `4`.

If you have both restrained and bloomed clips:
- use restrained clips in `Intro`, `Break A`, `Drop A`, `Drop A Lift`, and `Re-entry Build`
- use bloomed clips in `Break B`, `Drop B`, and `Drop B Lift`

### Chord Placement By Section
`Intro A`, `1.1.1-17.1.1`:
- `chord_intro_hint_4bar`
- low velocity
- filtered

`Intro B`, `17.1.1-33.1.1`:
- `chord_intro_full_4bar`
- still tucked

`Break A`, `33.1.1-49.1.1`:
- restrained chord bed
- no `Bbmaj7` bloom yet
- keep space for the first vocal

`Drop A`, `49.1.1-65.1.1`:
- restrained drop chord clip
- same harmonic restraint as the original plan
- no early `Bbmaj7` bloom

`Drop A Lift`, `65.1.1-81.1.1`:
- same harmony as `Drop A`
- slightly brighter pulse only

`Break B`, `81.1.1-97.1.1`:
- bloomed / stretched chord clip
- this is where the upward chord width opens

`Re-entry Build`, `97.1.1-113.1.1`:
- restrained pulse
- use restrained `Bb`, not bloomed `Bbmaj7`

`Drop B`, `113.1.1-129.1.1`:
- bloomed drop chord clip

`Drop B Lift`, `129.1.1-145.1.1`:
- bloomed drop chord clip
- slightly wider / brighter than `Drop B`

`Outro`, `145.1.1-161.1.1`:
- intro hint or restrained chord clip from `145.1.1-153.1.1`
- empty from `153.1.1-161.1.1`

## Step 6: Place The Vocals
### Action
Use the clips from Part `5`.

Do not paste the full vocal stem everywhere.

Use the clip functions.

### Vocal Placement By Section
`Intro A`, `1.1.1-17.1.1`:
- `Vocal Full Chorus`: empty
- `Vocal Chops`: empty
- `Vocal Throw`: empty

`Intro B`, `17.1.1-33.1.1`:
- all vocal tracks empty

`Break A`, `33.1.1-49.1.1`:
- `VOC mystery statement` at `40.1.1` on `Vocal Chops`
- optional `VOC mystery seed` at `44.1.1` on `Vocal Chops`
- `VOC question pre-drop` at `48.3.3` on `Vocal Chops`
- trim the question so it ends before `49.1.1`

`Drop A`, `49.1.1-65.1.1`:
- `VOC full chorus clean` at `49.1.1` on `Vocal Full Chorus`
- no constant chop loop
- only use `Vocal Throw` if there is a natural gap

`Drop A Lift`, `65.1.1-81.1.1`:
- `VOC chop A` at `68.3.4` on `Vocal Chops`
- `VOC chop B` at `72.3.4` on `Vocal Chops`
- `VOC exposed core` at `76.3.4` on `Vocal Chops`
- optional `VOC throw` at `80.4.4` on `Vocal Throw`

`Break B`, `81.1.1-97.1.1`:
- `VOC question pre-drop` or `VOC mystery seed` at `88.1.1`
- optional `VOC vulnerable phrase` at `92.1.1`

`Re-entry Build`, `97.1.1-113.1.1`:
- optional `VOC reverse tail` ending near `109.3.4`
- optional filtered pickup at `110.3.4`
- `VOC question pre-drop` at `112.3.3`
- trim it before `113.1.1`

`Drop B`, `113.1.1-129.1.1`:
- `VOC full chorus clean` at `113.1.1` on `Vocal Full Chorus`
- add only low-level chop texture in chorus gaps
- do not cover the full chorus with constant throws

`Drop B Lift`, `129.1.1-145.1.1`:
- `VOC chop A` at `132.3.4`
- `VOC chop B` at `136.3.4`
- `VOC exposed core` or `VOC throw` at `140.3.4`
- optional `VOC throw` at `144.3.4`

`Outro`, `145.1.1-161.1.1`:
- no new lyric
- tails only if needed

## Step 7: Do The First Playback Pass
### Action
Play from `1.1.1` to `161.1.1`.

Do not edit during the first playback.

Write down the first section that feels wrong.

Use this section checklist:
1. `1-16 Intro A`: no vocal, useful DJ intro
2. `17-32 Intro B`: bass teaser, still no vocal
3. `33-48 Break A`: first vocal introduction, no chorus yet
4. `49-64 Drop A`: full chorus lands cleanly
5. `65-80 Drop A Lift`: chops deconstruct the chorus
6. `81-96 Break B`: darker vocal return, less drums
7. `97-112 Re-entry Build`: groove wakes back up
8. `113-128 Drop B`: full chorus returns with more production
9. `129-144 Drop B Lift`: strongest chop / throw energy
10. `145-160 Outro`: DJ-safe stripdown

### Why
Fix the arrangement by section purpose, not by random editing.

## Step 8: Check The Energy Curve
### Action
Listen once and rate each section from `1` to `10`.

Target curve:
- `Intro A`: `2/10`
- `Intro B`: `3/10`
- `Break A`: `5/10`
- `Drop A`: `7/10`
- `Drop A Lift`: `8/10`
- `Break B`: `4/10`
- `Re-entry Build`: `6/10`
- `Drop B`: `8/10`
- `Drop B Lift`: `9/10`
- `Outro`: `5/10`

If a section is more than `1` point away from target, check the growth mechanism:
- too quiet: missing core lane or vocal placement
- too loud: too many layers too early
- too flat: no phrase-end change
- too busy: too many vocals or hats

## Step 9: Bounce The Rough Arrangement
### Action
In Ableton:
1. Set the loop brace from `1.1.1` to `161.1.1`.
2. Choose `File -> Export Audio/Video`.
3. Export a `24-bit WAV`.
4. Name it `ukg-140-og-bounce-driver_part06_rough-arrangement.wav`.

This is not the final mix.

It is a rough arrangement checkpoint.

## Screenshot Requirements
Capture:
- `part06-01-10-locators`
- `part06-02-air-full-length`
- `part06-03-drums-break-a-to-drop-a`
- `part06-04-bass-drop-a-placement`
- `part06-05-chords-break-b-bloom`
- `part06-06-vocals-break-a`
- `part06-07-vocals-drop-a-full-chorus`
- `part06-08-vocals-drop-a-lift-chops`
- `part06-09-vocals-drop-b-full-chorus`
- `part06-10-full-arrangement-view`

## Troubleshooting
### Drop A feels like karaoke
The full chorus is probably too exposed relative to the club groove.

Fix in this order:
1. Check drum strength.
2. Check bass body.
3. Add a very low chop or throw only in a natural gap.
4. Do not chop the whole first chorus to solve this.

### Drop A feels too crowded
Remove extras.

First-pass `Drop A` should be:
- drums
- bass
- restrained chords
- full chorus

It should not have:
- constant chop loop
- loud throws
- full chord bloom

### Break A feels boring
Do not add the chorus.

Instead:
- move `VOC mystery statement` later to `40.1.1`
- keep drums thinner
- make the question at `48.3.3` more obvious

### Drop B does not feel bigger than Drop A
Check:
- chords are bloomed in `Drop B`
- top end is more open
- drums have slightly stronger top support
- `Drop B` returns the intact chorus after the listener heard chops in `Drop A Lift`

### Drop B Lift is messy
Mute `Vocal Throw` first.

Then mute one chop.

The peak should feel edited, not chaotic.

## Completion Check
Before moving to Part `7`, confirm:
- there are `10` locators
- `Break A` exists before `Drop A`
- `Drop A` starts at `49.1.1`
- `VOC full chorus clean` appears at `49.1.1` and `113.1.1`
- `Drop A Lift` contains chops, not another full chorus
- `Break B` returns to mystery before `Re-entry Build`
- `Outro` starts at `145.1.1`
- no vocal clip crosses a section boundary by accident
