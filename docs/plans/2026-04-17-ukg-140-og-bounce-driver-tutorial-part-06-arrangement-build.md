# UKG 140 OG Bounce Driver: Tutorial Part 6 — Arrangement Build

## Purpose
Teach the learner how to turn the finished lanes for `ukg-140-og-bounce-driver` into a full `144`-bar club arrangement that:
- grows by different mechanisms in different sections
- keeps `Drop A` restrained enough for `Drop B` to matter
- makes the `Re-entry Build` a real re-entry, not a second break
- feels designed rather than blocky

This part should convert the frozen architecture into exact section assembly, phrase planning, and energy control.

Automation note:
- this chapter builds the clip-placement and section-logic version of the arrangement first
- use only coarse placeholder moves here when needed:
  - temporary filter states
  - obvious mutes / returns on or off
  - rough width states already baked into section clips
- detailed transition automation, sweeps, fills, FX throws, and section-boundary motion are authored in `Part 7: Transitions Toolkit`

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)

## Outcome
By the end of this part, the learner should have:
- all `9` sections laid out across the timeline:
  - `1–16 Intro A`
  - `17–32 Intro B`
  - `33–48 Drop A`
  - `49–64 Drop A Lift`
  - `65–80 Break`
  - `81–96 Re-entry Build`
  - `97–112 Drop B`
  - `113–128 Drop B Lift`
  - `129–144 Outro`
- all core lanes assigned by section:
  - drums
  - bass
  - chords
  - vocal main
  - vocal throw
  - air
- phrase-level changes inside each `16`-bar section
- one full-song rough arrangement bounce

## Time Estimate
- `60–90 minutes`

## Prerequisites
- learner has completed or can reference:
  - `Part 2` groove
  - `Part 3` bass floor
  - `Part 4` harmonic bed
  - `Part 5` identity
- this part does **not** assume the learner already knows Ableton arrangement mechanics
- clip creation, clip duplication, locator creation, mutes, and bar placement are explained before they are used

## What The Learner Should Understand Before Starting
Before arranging, run one carryover check from Parts `4` and `5`.

Do not arrange around broken lane sounds.

Chord lane must pass:
- `Chords` Serum patch has `Mono` off
- `Legato` is off
- `Poly` is at least `8`
- safe first-pass `Dm9` is `D3 F3 A3 C4 E4`
- the chord bed sounds like a soft garage organ/pad hybrid, not a single-note beep

Vocal lane must pass:
- if a vocal sample is already chosen, it works against the healthy chord bed without muting the chords
- if no vocal sample is chosen yet, `Vocal Main` and `Vocal Throw` stay empty or muted while the arrangement preserves the vocal space
- do not replace the missing vocal with a synth hook just because the sample is not chosen yet

Arrangement here is not:
- copy-pasting one 4-bar loop for 4 minutes
- muting and unmuting entire lanes with no phrase design
- making every section feel bigger by adding one more layer

Arrangement here is:
- section purpose
- phrase pressure
- selective removal
- earned returns

Important terminology:
- every section handoff in this song is a transition
- the `Re-entry Build` is only one dedicated section inside the arrangement
- `Intro A -> Intro B`, `Drop A -> Drop A Lift`, and `Drop B Lift -> Outro` are still transitions even though they do not get their own full `16`-bar blocks
- `Part 7` is where those boundary transitions get their detailed fill, subtraction, and automation moves

If every section uses the same growth move, the record will flatten out even if the sound design is good.

Timing reminder for this part:
- every position in this chapter is an Arrangement View position unless the step explicitly tells you to open a local clip
- that means `17.1.1` and `97.1.1` are full-song bars, not local clip bars

## Ableton Operations Used In This Part
Use this section whenever the steps below say `place`, `duplicate`, `mute`, or `create a clip`.

### Arrangement View
1. Press `Tab` until Ableton shows the horizontal timeline.
2. The numbers across the top are full-song bars.
3. Bar `1` is the start of the song.
4. Bar `33` is the start of `Drop A`.
5. Bar `97` is the start of `Drop B`.

If you are looking at vertical clip slots, you are in Session View.
Press `Tab` once to return to Arrangement View.

### Create An Empty MIDI Clip In Arrangement View
Use this when a lane is missing the clip you need.

1. Click and drag across the empty space on the target MIDI track.
2. Start exactly at the first bar named in the step.
3. Drag to the end bar named in the step.
4. Press `Cmd+Shift+M` on Mac or `Ctrl+Shift+M` on Windows.
5. Ableton creates an empty MIDI clip over the selected time.
6. Double-click the clip to open the piano roll.

Example:
- select `97.1.1` to `101.1.1` on `Vocal Guide MIDI`
- press `Cmd+Shift+M`
- now you have one empty `4`-bar guide clip for marking vocal placement

### Duplicate A Clip
Use this when the lesson says a clip repeats.

1. Click the clip once so it is selected.
2. Press `Cmd+D` on Mac or `Ctrl+D` on Windows.
3. Ableton places the duplicate immediately after the original.
4. Keep pressing `Cmd+D` until the clip reaches the required end bar.

Example:
- one `4`-bar clip from `33.1.1` to `37.1.1`
- press `Cmd+D`
- second copy appears from `37.1.1` to `41.1.1`
- press `Cmd+D` two more times
- the four copies now fill `33.1.1` to `49.1.1`

### Move A Clip To An Exact Bar
1. Turn on the grid if clips are not snapping cleanly.
2. Drag the clip left or right until its left edge lines up with the target bar.
3. Zoom in if needed.
4. The clip's left edge must sit exactly on the bar line.

Do not place clips slightly before or after the bar line on the first pass.
Micro-timing belongs inside MIDI clips, not in full-section arrangement placement.

### Mute A Clip Or Section
Use this when the lesson says a lane is silent for a range.

Option A:
1. Select the clip.
2. Press `0`.
3. The clip becomes disabled / greyed out.

Option B:
1. Delete the clip from that range.
2. Leave the track empty there.

For this tutorial, empty space is clearer than disabled clips.
If a lane should be silent, leaving that range empty is usually best.

### What `x` Means In Positions
When this lesson says `x.4.3`, the `x` means "whatever bar you are currently editing."

Examples:
- in bar `33`, `x.4.3` means `33.4.3`
- in bar `48`, `x.4.3` means `48.4.3`
- in bar `100`, `x.4.3` means `100.4.3`

## Reference Axis
Primary A/B for this part:
- `Interplanetary Criminal - Slow Burner`
  - listen for how the section changes feel rhythmic and pocket-based, not just FX-based
- `KETTAMA - It Gets Better`
  - listen for how pressure is maintained even when the arrangement strips down

Secondary check:
- `Sammy Virji - I Guess We're Not the Same`
  - listen for how harmonic and vocal information arrive in controlled stages

## Files / Assets Needed
- current project with:
  - working drums
  - bass
  - chords
  - vocal main
  - vocal throw
  - air
- one full arrangement timeline ready to place locators / markers
- access to the Full Song Plan sections:
  - arrangement assignments
  - energy curve
  - top-end map
  - growth rule by section

## Frozen Section Map
Use this as the source of truth:
- `1–16 Intro A`
- `17–32 Intro B`
- `33–48 Drop A`
- `49–64 Drop A Lift`
- `65–80 Break`
- `81–96 Re-entry Build`
- `97–112 Drop B`
- `113–128 Drop B Lift`
- `129–144 Outro`

Growth rule by section:
- `Drop A`: force and restraint
- `Drop A Lift`: top-end density and pocket only
- `Break`: upward harmonic bloom and air
- `Re-entry Build`: rhythmic re-engagement
- `Drop B`: harmonic bloom plus first real vocal sample identity
- `Drop B Lift`: strongest release through vocal placement, top-end opening, and chord bloom

## Step 0: Run The Sound-Health Gate
### Action
Do this before placing the full arrangement.
Do not skip it.

Create or loop one test range from `33.1.1` to `37.1.1`.
Use the core drop clips from Parts `2–5`.

Test `1`: kick and sub only.
1. Solo `Kick Body`, `Kick Click`, and `Bass Sub`.
2. Play the loop.
3. The low end should feel clean and stable.
4. If the sub disappears when the kick hits, reduce sidechain depth.
5. If the kick and sub rumble into each other, shorten kick tail or increase sub sidechain release discipline before arranging.

Test `2`: add `Bass Mid`.
1. Keep `Kick Body`, `Kick Click`, and `Bass Sub` playing.
2. Unmute `Bass Mid`.
3. The rhythm should become more audible.
4. The low end should not get larger, blurrier, or fartier.
5. If it gets muddy, fix `Bass Mid` before arranging:
   - `Sub` off
   - `Noise` off
   - Serum FX reverb/delay/chorus/hyper/compressor off
   - `Osc B` unison `1`
   - `Osc B Level` around `10–15%`
   - EQ after Serum high-pass around `220–300 Hz`
   - move only `Bass Mid` low notes up an octave if needed
6. Do not change `Bass Sub` if `Bass Sub` passed Test `1`.

Test `3`: add `Chords`.
1. Keep drums and both bass lanes playing.
2. Unmute `Chords`.
3. The chord bed should add harmony without swallowing the bass movement.
4. If mud appears only when `Chords` enters, fix `Chords` first:
   - confirm `Mono` off
   - confirm `Poly` at least `8`
   - high-pass chords around `180 Hz`
   - cut chords around `250 Hz` by `-2` to `-3 dB`
5. If the stack still muddies after chord cleanup, raise the `Bass Mid` high-pass toward `300–500 Hz`.
6. Do not arrange until `Kick + Bass Sub + Bass Mid + Chords` works as a `4`-bar loop.

Test `4`: check the vocal lane.
1. If you already chose a vocal sample in Part `5`, unmute `Vocal Main`.
2. Play the loop with drums, bass, and chords.
3. The vocal should feel human and phrase-led, not like a keyboard placeholder.
4. If the vocal fights the chords, mute it and keep the vocal lane empty until you find a better sample.
5. If you do not have a sample yet, continue with `Vocal Main` and `Vocal Throw` muted. The arrangement can still be built as long as the vocal space is preserved.

### Why
Arrangement will not fix a broken sound stack.

If the bass mid and chords are fighting in a `4`-bar loop, a `144`-bar arrangement only hides the problem until later.

### Pass Condition
Continue only when this stack works:
- `Kick Body`
- `Kick Click`
- `Bass Sub`
- `Bass Mid`
- `Chords`
- `Vocal Main` if a sample has already passed Part `5`

The stack does not need to be mixed perfectly.
It must be musically readable and not muddy.

## Step 1: Mark The Timeline
### Action
Create all `9` locators before placing clips.

How to create one locator in Ableton:
1. Go to Arrangement View.
2. Click in the top timeline ruler at the target bar.
3. If Ableton has a `Set` button near the locator area, click `Set`.
4. If you do not see `Set`, right-click in the top ruler and choose `Add Locator`.
5. Click the new locator name.
6. Press `Cmd+R` on Mac or `Ctrl+R` on Windows.
7. Type the exact locator name from the list below.
8. Press `Enter`.

Create these exact locators:
1. At `1.1.1`, name it `1-16 Intro A`
2. At `17.1.1`, name it `17-32 Intro B`
3. At `33.1.1`, name it `33-48 Drop A`
4. At `49.1.1`, name it `49-64 Drop A Lift`
5. At `65.1.1`, name it `65-80 Break`
6. At `81.1.1`, name it `81-96 Re-entry Build`
7. At `97.1.1`, name it `97-112 Drop B`
8. At `113.1.1`, name it `113-128 Drop B Lift`
9. At `129.1.1`, name it `129-144 Outro`

Do not worry about locator colors in Ableton Live `11`.
Some setups do not show a color option for locators.
The locator names matter more than colors.

Final check:
- read the locator names from left to right
- there should be exactly `9`
- the bar numbers should match the section map above

### Why
The arrangement needs a visible map before clips start flying around.

If the learner only arranges by ear with no timeline structure:
- the middle sections will drift
- the `Re-entry Build` will often disappear
- the outro will be too short or too empty

### Screenshot
- `arrangement-01-timeline-markers`

## Step 2: Lay In The Section Skeleton
### Action
This step gets the full song onto the Arrangement View timeline.
It gives exact first-pass placements instead of asking you to guess the arrangement by ear.
Follow the lane map below.

Work one lane family at a time:
1. `Air`
2. `Drums`
3. `Bass`
4. `Chords`
5. `Vocal Main`
6. `Vocal Throw`

After each lane family is placed, press play from `4` bars before the next section boundary.
Example: after placing `Intro A` and `Intro B`, play from `13.1.1` through `37.1.1`.

### 2A: Place The Air Lane
The `Air` lane should quietly run through the whole record.

1. Go to the `Air` track.
2. Place the `4`-bar air clip from Part `1` at `1.1.1`.
3. The first copy should run from `1.1.1` to `5.1.1`.
4. Press `Cmd+D` / `Ctrl+D` until the air reaches `145.1.1`.
5. Do not leave gaps between air clips.
6. If the air feels too loud, lower the `Air` fader.
7. Do not delete the air from the break or outro.

### 2B: Place The Drum Lanes
Keep drums on separate tracks.
Do not combine them into a rack here.

Use these tracks:
- `Kick Body`
- `Kick Click`
- `Clap`
- `Closed Hat`
- `Ghost Hat`
- `Open Hat`
- `Shaker`
- `Drum Fill FX`

Drum shorthand translation:
- `four-on-the-floor` means one MIDI note on every beat of every bar:
  - bar `x`: `x.1.1`, `x.2.1`, `x.3.1`, `x.4.1`
  - example bar `17`: `17.1.1`, `17.2.1`, `17.3.1`, `17.4.1`
- `beats 2 and 4` for `Clap` means:
  - bar `x`: `x.2.1` and `x.4.1`
  - example bar `17`: `17.2.1` and `17.4.1`
- `offbeat pattern` for `Closed Hat` means the `&` of every beat:
  - bar `x`: `x.1.3`, `x.2.3`, `x.3.3`, `x.4.3`
  - example bar `17`: `17.1.3`, `17.2.3`, `17.3.3`, `17.4.3`
- `starter ghost pattern` means the soft late ghost-hat hits from Part `2`:
  - bar `x`: `x.2.2`, `x.2.4`, `x.4.2`, `x.4.4`
  - after placing them, nudge those ghost-hat notes slightly late if Part `2` tells you to do so
- `quiet 1/8 pattern` for `Shaker` means:
  - bar `x`: `x.1.1`, `x.1.3`, `x.2.1`, `x.2.3`, `x.3.1`, `x.3.3`, `x.4.1`, `x.4.3`
  - keep shaker velocity lower than the closed hat so it supports the groove instead of becoming the main hat
- `Drum Fill FX` means the dedicated transition/fill track, not a rack:
  - use a short reverse cymbal, short noise burst, rim/snare pickup, or tom pickup
  - if you do not have a fill sample yet, place a muted empty placeholder clip at the listed time and return to it in Part `7`

First-pass drum placement:
- `1.1.1–17.1.1 Intro A`
  - `Kick Body`: four-on-the-floor pattern across the full range
  - `Kick Click`: same MIDI as `Kick Body`, lower fader than body
  - `Clap`: empty from `1.1.1–9.1.1`, then beats `2` and `4` from `9.1.1–17.1.1`
  - `Closed Hat`: offbeat pattern from `1.1.1–17.1.1`
  - `Ghost Hat`: empty from `1.1.1–9.1.1`, starter ghost pattern from `9.1.1–17.1.1`
  - `Open Hat`: empty
  - `Shaker`: empty from `1.1.1–9.1.1`, quiet `1/8` pattern from `9.1.1–17.1.1`
  - `Drum Fill FX`: one short fill only at `16.4.3` and `16.4.4`
- `17.1.1–33.1.1 Intro B`
  - `Kick Body`: four-on-the-floor across the full range
  - `Kick Click`: same MIDI as `Kick Body`
  - `Clap`: beats `2` and `4` across the full range
  - `Closed Hat`: offbeat pattern across the full range
  - `Ghost Hat`: starter ghost pattern across the full range
  - `Open Hat`: empty from `17.1.1–25.1.1`, then `x.4.3` from `25.1.1–33.1.1`
  - `Shaker`: `1/8` pattern across the full range
  - `Drum Fill FX`: one short fill at `32.4.3` and `32.4.4`
- `33.1.1–49.1.1 Drop A`
  - use the full `16`-bar micro-architecture from Part `2` Step `10`
  - place it exactly from `33.1.1` to `49.1.1`
- `49.1.1–65.1.1 Drop A Lift`
  - duplicate the `Drop A` drums from `33.1.1–49.1.1`
  - paste them from `49.1.1–65.1.1`
  - keep the same kick, clap, and closed-hat structure
  - use the denser ghost/shaker/fill behavior from Part `2` Step `10` as the lift mechanism
- `65.1.1–81.1.1 Break`
  - `Kick Body`: empty from `65.1.1–73.1.1`, then one kick at `73.1.1`, `75.1.1`, `77.1.1`, and `79.1.1`
  - `Kick Click`: same as `Kick Body`, or empty if the break feels too sharp
  - `Clap`: empty
  - `Closed Hat`: empty from `65.1.1–73.1.1`, then sparse offbeat hits at `73.4.3`, `75.4.3`, `77.4.3`, and `79.4.3`
  - `Ghost Hat`: empty
  - `Open Hat`: empty
  - `Shaker`: empty or very quiet `1/8` pattern from `73.1.1–81.1.1`
  - `Drum Fill FX`: one short pickup at `80.4.3` and `80.4.4`
- `81.1.1–97.1.1 Re-entry Build`
  - `Kick Body`: four-on-the-floor across the full range
  - `Kick Click`: same MIDI as `Kick Body`
  - `Clap`: empty from `81.1.1–89.1.1`, then beats `2` and `4` from `89.1.1–97.1.1`
  - `Closed Hat`: offbeat pattern across the full range
  - `Ghost Hat`: starter ghost pattern from `85.1.1–97.1.1`
  - `Open Hat`: empty from `81.1.1–93.1.1`, then `93.4.3`, `94.4.3`, `95.4.3`, `96.4.3`
  - `Shaker`: empty from `81.1.1–89.1.1`, then quiet `1/8` pattern from `89.1.1–97.1.1`
  - `Drum Fill FX`: pre-drop fill at `96.4.3` and `96.4.4`
- `97.1.1–113.1.1 Drop B`
  - duplicate the `Drop A` drums from `33.1.1–49.1.1`
  - paste them from `97.1.1–113.1.1`
- `113.1.1–129.1.1 Drop B Lift`
  - duplicate the `Drop A Lift` drums from `49.1.1–65.1.1`
  - paste them from `113.1.1–129.1.1`
- `129.1.1–145.1.1 Outro`
  - `Kick Body`: four-on-the-floor from `129.1.1–145.1.1`
  - `Kick Click`: same MIDI as `Kick Body`
  - `Clap`: beats `2` and `4` from `129.1.1–137.1.1`, then empty from `137.1.1–145.1.1`
  - `Closed Hat`: offbeat pattern from `129.1.1–145.1.1`
  - `Ghost Hat`: starter ghost pattern from `129.1.1–137.1.1`, then empty
  - `Open Hat`: empty
  - `Shaker`: quiet `1/8` pattern from `129.1.1–137.1.1`, then empty
  - `Drum Fill FX`: empty

### 2C: Place The Bass Lanes
Use both `Bass Sub` and `Bass Mid`.
The two lanes should use the same timing unless the step says otherwise.

`Intro A`:
- leave `Bass Sub` and `Bass Mid` empty from `1.1.1–17.1.1`

`Intro B`:
- create a `4`-bar teaser pattern from `17.1.1–21.1.1`
- bar `17`: place `D2` from `17.1.1–17.3.1`
- bar `18`: place `Bb1` from `18.1.1–18.3.1`, then `Bb2` at `18.4.3` with `1/16` length
- bar `19`: place `F2` from `19.1.1–19.3.1`
- bar `20`: place `C2` from `20.1.1–20.3.1`, then `C3` at `20.4.3` with `1/16` length
- copy `17.1.1–21.1.1` to `21.1.1–25.1.1`, `25.1.1–29.1.1`, and `29.1.1–33.1.1`
- on `Bass Mid`, if `Bb1` sounds bad, use `Bb2` for the mid layer only
- on `Bass Sub`, keep the low roots

`Drop A`:
- place the working `4`-bar rolling bass clip from Part `3` at `33.1.1–37.1.1`
- duplicate it to `37.1.1–41.1.1`
- duplicate it to `41.1.1–45.1.1`
- duplicate it to `45.1.1–49.1.1`

`Drop A Lift`:
- duplicate the `Drop A` bass from `33.1.1–49.1.1`
- paste it from `49.1.1–65.1.1`
- do not add new bass notes
- do not reveal new chord-color pitch events

`Break`:
- keep `Bass Sub` sparse:
  - `D2` from `65.1.1–65.3.1`
  - `Bb1` from `69.1.1–69.3.1`
  - `F2` from `73.1.1–73.3.1`
  - `C2` from `77.1.1–77.3.1`
- keep `Bass Mid` either empty or very quiet on the same notes
- do not use the full rolling bass clip in the break

`Re-entry Build`:
- use the same teaser logic as `Intro B`
- create one `4`-bar teaser from `81.1.1–85.1.1`
- duplicate it to `85.1.1–89.1.1`, `89.1.1–93.1.1`, and `93.1.1–97.1.1`
- keep this filtered / lighter than the drop bass

`Drop B`:
- duplicate the `Drop A` bass from `33.1.1–49.1.1`
- paste it from `97.1.1–113.1.1`
- allow phrase-end lift only if it already worked in Part `3`
- do not add a second bassline

`Drop B Lift`:
- duplicate the `Drop B` bass from `97.1.1–113.1.1`
- paste it from `113.1.1–129.1.1`
- keep the sub stable
- do not change bass notes; drums, chords, vocal placement, and top-end create the lift

`Outro`:
- use the sparse teaser/break bass from `129.1.1–145.1.1`
- keep only enough bass to make the outro mixable
- do not introduce new bass movement in the outro

### 2D: Place The Chords
Use one `Chords` track.
Do not make separate chord tracks for every section.

`Intro A`:
- leave `Chords` empty from `1.1.1–9.1.1`
- place a restrained chord hint from `9.1.1–17.1.1`
- use the restrained `4`-bar chord clip twice:
  - `9.1.1–13.1.1`
  - `13.1.1–17.1.1`

`Intro B`:
- place the restrained `4`-bar chord clip four times:
  - `17.1.1–21.1.1`
  - `21.1.1–25.1.1`
  - `25.1.1–29.1.1`
  - `29.1.1–33.1.1`

`Drop A`:
- place the restrained `4`-bar chord clip four times from `33.1.1–49.1.1`
- the `Bb` bar must stay restrained: `Bb2 F3 C4`
- do not use `A3` in the `Bb` bar here

`Drop A Lift`:
- duplicate the `Drop A` chord clips from `33.1.1–49.1.1`
- paste them from `49.1.1–65.1.1`
- do not change chord notes

`Break`:
- use the `8`-bar bloom chord clip twice:
  - `65.1.1–73.1.1`
  - `73.1.1–81.1.1`
- this is where the `Bbmaj7` bloom appears:
  - `Bb2 F3 A3 C4`

`Re-entry Build`:
- return to the restrained `4`-bar chord clip
- place it four times from `81.1.1–97.1.1`
- the `Bb` bar returns to `Bb2 F3 C4`

`Drop B`:
- use the `8`-bar bloom chord clip twice:
  - `97.1.1–105.1.1`
  - `105.1.1–113.1.1`

`Drop B Lift`:
- use the `8`-bar bloom chord clip twice:
  - `113.1.1–121.1.1`
  - `121.1.1–129.1.1`

`Outro`:
- use the restrained `4`-bar chord clip from `129.1.1–137.1.1`
- leave `Chords` empty from `137.1.1–145.1.1`

### 2E: Place Vocal Main And Vocal Throw
Use the vocal sample workflow from Part `5`.

Do not place the old synth hook/answer here.

If you have not found a sample yet:
- keep `Vocal Main` empty
- keep `Vocal Throw` empty
- optionally place muted placeholder clips at the listed positions so the vocal space is visible

If you have found a sample:
- `Vocal Main` is the main hook phrase, title chop, or phrase fragment
- `Vocal Throw` is the shorter tail, breath, syllable, or delayed response
- both should feel human and sample-led
- neither should sound like a beepy keyboard

If you are using a big trance / rave vocal stem:
- `VOC break lyric phrase` is the readable lyric moment for the break
- `VOC hook phrase` is the main `Drop B` identity
- `VOC hook title chop` is the shortest repeatable version of the hook
- `VOC isolation throw` is the ending word, tail, or breath used as punctuation
- `VOC reverse tail` is the transition pull into a section
- do not paste the full acapella across the track

If you are using the current source phrase:

```text
I just wanna give you something to believe in
```

Use this arrangement vocabulary:
- `VOC i just wanna tease`: filtered teaser before the main vocal reveal
- `VOC give you stab`: small rhythmic hint for restrained sections
- `VOC believe in main`: main `Drop B` vocal identity
- `VOC in throw`: short phrase-end punctuation
- `VOC to believe in long`: bigger `Drop B Lift` phrase
- `VOC believe reverse`: reverse pull into a section

Do not place the full `3.2`-bar source phrase across the whole arrangement on the first pass.

The arrangement is built from small clips with different jobs.

`Intro A`:
- keep `Vocal Main` empty
- keep `Vocal Throw` empty

`Intro B`:
- keep `Vocal Main` empty until the back half
- optional filtered vocal teaser only:
  - first teaser: `VOC i just wanna tease` attack starts at `29.3.4`
  - second teaser: duplicate `VOC i just wanna tease` at `30.3.4` only if the first one works
- keep these teasers quieter than the final `Drop B` vocal
- keep `Vocal Throw` empty

`Drop A`:
- keep the main vocal out on the first pass
- optional quiet teaser only:
  - `VOC give you stab` attack starts at `40.3.4`
  - duplicate only if it works at `48.3.4`
- keep `Vocal Throw` empty
- if the vocal teaser makes `Drop A` feel like the main drop, delete it
- do not use `VOC believe in main` here

`Drop A Lift`:
- keep the main vocal out on the first pass
- optional quiet teaser only:
  - `VOC i just wanna tease` or `VOC give you stab` attack starts at `56.3.4`
  - duplicate only if it works at `64.3.4`
- do not reveal the best vocal phrase here
- keep `Vocal Throw` empty

`Break`:
- keep the drop hook phrase out
- if using a phrase-led vocal, place `VOC break lyric phrase` at `72.1.1` or `76.1.1`
- if using the current source phrase, one quiet `VOC to believe in long` texture can sit at `76.4.4`
- optional reverse pull: place `VOC believe reverse` so the reversed tail ends exactly at `65.1.1`
- keep `Vocal Throw` empty unless the throw is a very quiet reverse or breath
- if the lyric becomes readable and dominant in the break, lower it or delete it
- if the break phrase feels like the full chorus has arrived, shorten it or move the clearest hook phrase back to `Drop B`

`Re-entry Build`:
- keep `81.1.1–93.1.1` vocal-empty
- optional filtered pickups only:
  - `VOC i just wanna tease` attack starts at `93.3.4`
  - optional second `VOC i just wanna tease` starts at `94.3.4`
  - optional `VOC believe reverse` ends at `97.1.1`
- keep `Vocal Throw` empty unless the final pickup needs a tiny delay tail

`Drop B`:
- this is the first real vocal identity section
- first-pass `Vocal Main` placements:
  - `VOC hook phrase`, `VOC hook title chop`, or `VOC believe in main` attack starts at `100.3.4`
  - repeat the same clip at `108.3.4`
- optional `Vocal Main` alternates if those feel wrong:
  - `104.4.1`
  - `112.4.1`
- first-pass `Vocal Throw` placements:
  - `VOC isolation throw` or `VOC in throw` attack starts at `104.4.4`
  - repeat the throw at `112.4.4`
- do not place the vocal on every listed point
- use `100.3.4` and `108.3.4` first, then add throws only if the phrase needs them
- if `VOC believe in main` feels too short, test `VOC to believe in long` only once at `108.3.4`, then compare

`Drop B Lift`:
- continue the `Drop B` vocal logic
- first-pass `Vocal Main` placements:
  - longer `VOC hook phrase`, `VOC to believe in long`, or `VOC something to believe in` at `116.3.4`
  - repeat at `124.3.4` only if the first one works
- first-pass `Vocal Throw` placements:
  - `VOC isolation throw` or `VOC in throw` at `120.4.4`
  - repeat the throw at `128.4.4`
- only add extra vocal chops if `Drop B` still feels too empty after drums, chords, and top-end lift are working

`Outro`:
- keep `Vocal Main` empty from `129.1.1–145.1.1`
- keep `Vocal Throw` empty from `129.1.1–145.1.1`

### Why
This gets the whole song on the page fast.

You want to hear the architecture first, before spending an hour polishing one transition.

### Screenshot
- `arrangement-02a-full-song-skeleton`
- `arrangement-02b-intro-through-break`
- `arrangement-02c-reentry-build-through-outro`

### Visual Requirement
- show the whole song on screen with all locators visible
- otherwise show:
  - `Intro A` through `Break`
  - `Re-entry Build` through `Outro`
- keep drums, bass, chords, vocal main, vocal throw, and air lanes visible in each capture

## Step 3: Verify Intro A And Intro B
### Action
Zoom into `1.1.1–33.1.1`.

Check `Intro A` from `1.1.1–17.1.1`:
1. `Air` is present the whole time.
2. `Bass Sub` is empty.
3. `Bass Mid` is empty.
4. `Vocal Main` is empty.
5. `Vocal Throw` is empty.
6. `Chords` only enter from `9.1.1`.
7. `Open Hat` is empty.
8. `Drum Fill FX` only appears at `16.4.3` and `16.4.4`.

Check `Intro B` from `17.1.1–33.1.1`:
1. `Air` is present.
2. `Chords` are present from `17.1.1–33.1.1`.
3. `Bass Sub` and `Bass Mid` use the teaser pattern.
4. `Open Hat` appears only from `25.1.1–33.1.1`.
5. `Vocal Main` is empty or has only filtered teasers at `29.3.4` and `30.3.4`.
6. `Vocal Throw` is empty.
7. `Drum Fill FX` appears at `32.4.3` and `32.4.4`.

Playback check:
1. Set the loop brace from `13.1.1` to `37.1.1`.
2. Press play.
3. Listen for the move from intro into drop.
4. If `Intro B` already feels like a drop, remove `Open Hat` until `29.1.1` and lower `Shaker` by `-2 dB`.

### Why
The intro should prove the world of the track without giving away the full drop.

### Screenshot Set
- `arrangement-03-intro-a`
- `arrangement-04-intro-b`
- `arrangement-04b-intro-transition-detail`

## Step 4: Verify Drop A
### Action
Zoom into `33.1.1–49.1.1`.

Check every required lane:
1. `Kick Body` is active across the full range.
2. `Kick Click` is active across the full range.
3. `Clap`, `Closed Hat`, `Ghost Hat`, `Open Hat`, and `Shaker` follow the Part `2` `16`-bar micro-architecture.
4. `Bass Sub` uses the working rolling bass clip across all `16` bars.
5. `Bass Mid` uses the same rhythm as `Bass Sub`, with the cleaned-up mid patch.
6. `Chords` use the restrained `4`-bar chord clip four times.
7. The `Bb` chord in `Drop A` is restrained: `Bb2 F3 C4`.
8. `Vocal Main` is empty, or has only quiet filtered teasers at `40.3.4` and `48.3.4`.
9. `Vocal Throw` is empty on the first pass.
10. `Air` is present.

Vocal check:
- if using a teaser, the first vocal attack starts at `40.3.4`
- if repeating the teaser, the second vocal attack starts at `48.3.4`
- the best vocal phrase is not revealed in `Drop A`

Playback check:
1. Set the loop brace from `33.1.1` to `49.1.1`.
2. Listen once with all lanes.
3. Mute `Chords`.
4. If the bass suddenly feels much cleaner, return to Step `0` and fix the chord/bass stack.
5. Unmute `Chords`.
6. Mute `Bass Mid`.
7. If the track loses movement but the low end cleans up, the `Bass Mid` still needs EQ or octave cleanup.

### Why
`Drop A` is supposed to hit physically while saving the harmonic bloom for later.

### Screenshot
- `arrangement-05-drop-a`
- `arrangement-05b-drop-a-close`

## Step 5: Verify Drop A Lift
### Action
Zoom into `49.1.1–65.1.1`.

This section must be bigger than `Drop A` without adding new harmony.

Check:
1. `Bass Sub` notes match `Drop A`.
2. `Bass Mid` notes match `Drop A`.
3. `Chords` notes match `Drop A`.
4. The `Bb` chord is still restrained: `Bb2 F3 C4`.
5. `Vocal Main` is empty, or has only quiet filtered teasers at `56.3.4` and `64.3.4`.
6. `Vocal Throw` is empty on the first pass.
7. The full vocal sample is still saved for later.
8. Drums use the denser/lift version from Part `2`.
9. `Drum Fill FX` pushes into the break at `64.4.3` and `64.4.4`.

Do not do these in `Drop A Lift`:
- do not reveal the main vocal phrase
- do not add `A3` to the restrained `Bb` chord
- do not add a new bass melody
- do not add the vocal throw conversation yet

Playback check:
1. Loop `45.1.1–69.1.1`.
2. Listen through `Drop A -> Drop A Lift -> Break`.
3. If `Drop A Lift` sounds emotionally wider than `Drop A`, check the chord voicing first.
4. If it only sounds more energetic, that is correct.

### Screenshot
- `arrangement-06-drop-a-lift`
- `arrangement-06b-drop-a-vs-lift-comparison`

## Step 6: Verify The Break
### Action
Zoom into `65.1.1–81.1.1`.

Check:
1. Full rolling bass is gone.
2. `Bass Sub` only gives sparse root reminders at `65.1.1`, `69.1.1`, `73.1.1`, and `77.1.1`.
3. `Bass Mid` is empty or very quiet.
4. `Chords` use the `8`-bar bloom clip twice:
   - `65.1.1–73.1.1`
   - `73.1.1–81.1.1`
5. The `Bbmaj7` bloom appears in the chord clip as `Bb2 F3 A3 C4`.
6. `Kick Body` is empty from `65.1.1–73.1.1`.
7. `Kick Body` returns only at `73.1.1`, `75.1.1`, `77.1.1`, and `79.1.1`.
8. `Vocal Main` is empty except optional texture at `76.4.4`.
9. `Vocal Throw` is empty or a very quiet reverse/breath only.
10. `Air` is present.

Playback check:
1. Loop `61.1.1–85.1.1`.
2. Listen through `Drop A Lift -> Break -> Re-entry Build`.
3. If the break feels empty, raise chord level or air level slightly.
4. If the break feels like a different song, reduce chord brightness before changing notes.

### Screenshot
- `arrangement-07-break`
- `arrangement-07b-break-close`

## Step 7: Verify The Re-entry Build
### Action
Zoom into `81.1.1–97.1.1`.

Check:
1. `Kick Body` is back across the full section.
2. `Clap` stays out until `89.1.1`.
3. `Ghost Hat` stays out until `85.1.1`.
4. `Open Hat` stays out until `93.1.1`.
5. `Bass Sub` and `Bass Mid` use the teaser pattern, not the full drop bass.
6. `Chords` return to the restrained `4`-bar clip.
7. The `Bb` chord is back to `Bb2 F3 C4`.
8. `Vocal Main` is empty until the late pickup window:
   - optional pickup at `93.3.4`
   - optional pickup at `94.3.4`
   - optional pickup at `96.4.4`
9. `Vocal Throw` is empty unless the final pickup needs a small delay tail.
10. `Drum Fill FX` pushes into `97.1.1` at `96.4.3` and `96.4.4`.

Playback check:
1. Loop `77.1.1–101.1.1`.
2. Listen through `Break -> Re-entry Build -> Drop B`.
3. If `Re-entry Build` feels like another break, restore more drums earlier.
4. If it feels like `Drop B` has already arrived, remove vocal pickups before `93.3.4` and keep chords restrained.

### Screenshot
- `arrangement-08-reentry-build`
- `arrangement-08b-reentry-build-close`

## Step 8: Verify Drop B
### Action
Zoom into `97.1.1–113.1.1`.

Check:
1. `Kick Body`, `Kick Click`, and full drums are active.
2. `Bass Sub` and `Bass Mid` use the full rolling bass.
3. `Chords` use the `8`-bar bloom clip twice:
   - `97.1.1–105.1.1`
   - `105.1.1–113.1.1`
4. `Vocal Main` carries the first real vocal identity.
5. `Vocal Throw` punctuates phrase endings only if it helps.
6. `Vocal Main` and `Vocal Throw` do not crowd the same phrase ending.

Vocal Main placements:
- first main vocal attack starts at `100.3.4`
- second main vocal attack starts at `108.3.4`
- optional alternate main placements are `104.4.1` and `112.4.1`

Vocal Throw placements:
- first throw attack starts at `104.4.4`
- second throw attack starts at `112.4.4`
- if the throw sounds cheesy, delete it and keep only `Vocal Main`

Playback check:
1. Loop `97.1.1–113.1.1`.
2. Listen once with `Vocal Main` muted.
3. Listen once with `Vocal Throw` muted.
4. Listen once with both active.
5. If both together feel crowded, delete extra vocal placements before lowering both faders.

### Screenshot
- `arrangement-09-drop-b`
- `arrangement-09b-drop-b-vocal-map`

## Step 9: Verify Drop B Lift And Outro
### Action
Zoom into `113.1.1–145.1.1`.

Check `Drop B Lift` from `113.1.1–129.1.1`:
1. Drums use the lift version.
2. Bass stays stable and does not add a new line.
3. Chords keep the `8`-bar bloom clip twice:
   - `113.1.1–121.1.1`
   - `121.1.1–129.1.1`
4. `Vocal Main` can return at bars `116` and `124`.
5. `Vocal Throw` can return at bars `120` and `128`.
6. This is the biggest section, but it should not be the messiest section.

Check `Outro` from `129.1.1–145.1.1`:
1. `Vocal Main` is empty.
2. `Vocal Throw` is empty.
3. `Chords` play from `129.1.1–137.1.1`, then stop.
4. `Air` continues.
5. `Kick Body`, `Kick Click`, and `Closed Hat` continue to `145.1.1`.
6. `Clap`, `Ghost Hat`, and `Shaker` stop at `137.1.1`.
7. `Open Hat` is empty.

Playback check:
1. Loop `113.1.1–145.1.1`.
2. The lift should release energy.
3. The outro should become easier to mix out of.
4. If the outro dies too suddenly, keep shaker until `141.1.1`.
5. If the outro is too busy, remove clap at `133.1.1` instead of `137.1.1`.

### Screenshot Set
- `arrangement-10-drop-b-lift`
- `arrangement-11-outro`

## Step 10: Whole-Song Pass
### Action
Play the full arrangement from `1.1.1`.

Do not edit while listening on the first pass.
Write down the first bar number where something feels wrong.

Use this checklist:
1. `1–16`: intro is useful for mixing, not empty.
2. `17–32`: teaser appears, but full drop has not arrived.
3. `33–48`: `Drop A` hits, but no bloom yet.
4. `49–64`: `Drop A Lift` gets more energetic without new harmonic material.
5. `65–80`: break opens upward and does not feel like a mistake.
6. `81–96`: `Re-entry Build` wakes the rhythm back up.
7. `97–112`: `Drop B` blooms and introduces the main vocal sample identity.
8. `113–128`: `Drop B Lift` is the peak.
9. `129–144`: outro strips back without killing the mixable groove.

If something is wrong, fix only the first wrong section first.
Do not jump around the whole arrangement making random edits.

### Screenshot
- `arrangement-12-full-song-pass`
- `arrangement-12b-section-checklist`

## Step 11: Check The Energy Curve
### Action
Bounce the full rough arrangement and compare it to the planned energy staircase:
- `Intro A`: `2/10`
- `Intro B`: `3/10`
- `Drop A`: `7/10`
- `Drop A Lift`: `8/10`
- `Break`: `4/10`
- `Re-entry Build`: `6/10`
- `Drop B`: `8/10`
- `Drop B Lift`: `9/10`
- `Outro`: `5/10`

Measurement method:
1. loudness-match the rough bounce to the references before judging
2. listen section by section at a stable monitor level
3. write down a perceived-energy score from `1–10` for each section
4. compare those notes to the target curve
5. if any section is off by more than `1` point, treat that as evidence that a growth mechanism leaked or failed

### Why
This is the easiest way to catch leaks:
- if `Break` is too high, bloom leaked early
- if the `Re-entry Build` is too low, it feels like a second break
- if `Drop B` is not clearly above `Drop A`, the substitution failed

### Rule
- these are perceived-energy targets, not exact meter readings
- the deltas between sections matter more than the raw numbers

## Step 12: A/B The Full Arrangement
### Action
Bounce the full rough song.

Compare against:
- `Interplanetary Criminal - Slow Burner`
  - listen for re-entry pocket and transition logic
  - identify the phrase position where the drums feel fully back after the reset, then compare that relative position to your `Re-entry Build -> Drop B` handoff
- `KETTAMA - It Gets Better`
  - listen for sustained pressure across stripped and full sections
  - check whether your stripped sections still feel physically connected to the club record, not like demos
- `Sammy Virji - I Guess We're Not the Same`
  - listen for how vocal and harmonic information arrive in stages
  - check whether your vocal / harmony reveals are landing in distinct phases rather than all at once

### What To Listen For
- does `Drop A` hit hard enough without spending bloom?
- does the `Re-entry Build` feel like a re-entry and not a second break?
- does `Drop B` feel bigger because of substitution and bloom, not pile-up?
- does the outro still feel mixable?

### Expected Answer
- the second half should feel earned, not just louder
- every section should have a different reason for being bigger or smaller
- the arrangement should sound designed even before the final mix pass
- the rough bounce should already make structural sense before detailed automation is written in `Part 7`

## Troubleshooting
### Problem: “The arrangement feels blocky.”
Fix order:
1. add phrase-level change inside the section
2. improve removal/addition timing
3. only then add a new transition effect

### Problem: “The Re-entry Build feels like another break.”
Fix order:
1. restore more rhythmic motion
2. reduce harmonic openness
3. push the vocal pickup later

### Problem: “Drop B doesn’t feel bigger than Drop A.”
Fix order:
1. check whether bloom leaked in `Drop A Lift`
2. save the main vocal phrase for `Drop B`
3. make the vocal throw phrase-end only
4. reopen width / air around the chords

### Problem: “The outro feels dead.”
Fix order:
1. keep the air whisper
2. leave a stable drum/bass groove longer
3. remove emotional lanes before removing physical ones

## What Must Be Captured For Later Lesson Conversion
- full-song timeline screenshot
- one screenshot per major section
- one screenshot showing phrase-level changes inside a `16`-bar drop
- one rough full-song bounce
- one note on what changed between the first section skeleton and the final arrangement pass
