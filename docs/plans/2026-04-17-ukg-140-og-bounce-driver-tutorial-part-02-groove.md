# UKG 140 OG Bounce Driver: Tutorial Part 2 — Groove

## Purpose
Teach the learner how to build the drum groove for `ukg-140-og-bounce-driver` so it feels:
- body-forward
- bouncy
- late in the right places
- alive across a full `16`-bar section

This part should translate the drum philosophy into actual MIDI, timing, sample choice, and section architecture.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)

## Outcome
By the end of this part, the learner should have:
- a layered kick
- a clap lane
- closed hats
- ghost hats
- open hats
- a shaker lane
- one `16`-bar drop-drum section with internal micro-architecture
- one `2`-bar core drum variant
- one `2`-bar lift drum variant
- at least one phrase-end fill
- one bounce of `full drums`

## Time Estimate
- `45–75 minutes`

## Prerequisites
- learner can load one-shot drum samples in Ableton
- learner can edit MIDI timing and velocity
- learner understands bars, beats, `1/8`, and `1/16` note placement
- learner already has the session setup from `Part 0`

## What The Learner Should Understand Before Starting
The groove here should not come from:
- one global swing preset
- clipping the whole drum bus until it feels exciting
- adding more percussion until the loop sounds “busy”

It should come from:
- stable kick and clap anchors
- intentional late ghost hats
- hat and shaker velocity design
- phrase-end fills and lifts
- different internal jobs inside a `16`-bar section

If the drums feel stiff, the first suspect is usually MIDI timing.

Timing reminder for this part:
- positions like `1.2.3` are local positions inside the drum clip you are editing
- if you later paste that clip into Arrangement View at bar `33.1.1`, the clip still starts at local `1.1.1` inside itself
- do not type a full-song bar number into a `2`-bar clip

## Reference Axis
Primary A/B for this part:
- `Interplanetary Criminal - Slow Burner`
  - listen for ghost-hat drag and phrase-end groove movement
- `KETTAMA - It Gets Better`
  - listen for physical kick weight and density

Secondary check:
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - listen for how the tops sit around a rolling bassline without overfilling the center

## Files / Assets Needed
- current project with:
  - kick placeholder
  - clap placeholder
  - air layer if Part 1 is done
- separate tracks are recommended for this tutorial, not one combined drum rack, so bus/EQ/timing decisions stay easy to see
- use one track each for:
  - kick
  - clap
  - closed hats
  - ghost hats
  - open hats
  - shaker
  - optional top loop
- one `Drums` group

Plain-English drum terms used in this chapter:
- `anchor drums`: kick and clap; these stay on-grid so the track has a firm spine
- `top drums`: closed hats, ghost hats, open hats, shaker, and top loop; these create motion and air
- `ghost hat`: a quiet hat hit that is felt as groove more than heard as a main hat
- `support layer`: a quieter extra sample that reinforces another sound without becoming the main sound
- `drum bus`: the `Drums` group channel; all drum tracks feed into it so one compressor/saturator can affect the kit together
- `velocity`: the MIDI hit strength; higher values are louder/brighter, lower values are quieter/softer

## Sample Selection Rules
### Kick
- choose one short, tunable 909/garage-compatible body sample
- choose one short click/transient layer
- kick tail should stay inside `90–120 ms`
- the low body must still feel controllable once bass arrives

### Clap
- one main garage clap
- optional tight snare or rim support
- avoid a clap that already has too much long reverb baked in

### Hats
- choose crisp, short tops
- avoid brittle techno hats that dominate `8–10 kHz`

### Shaker
- choose one source that still reads after velocity changes and filtering

### Starting Source Recommendation
- use `Ableton Core Library` / stock 909-compatible samples as a first pass if exact external pack choices are not locked yet

## Step 1: Build The Kick
### Action
If you completed `Part 1`, reuse that kick. Do not rebuild it unless it failed the Part 1 checkpoint.

If you are building it here:
1. Load the kick body sample onto `Kick Body`.
2. Add Ableton `Tuner` after `Simpler`.
3. Use the Part 1 transpose map to make the kick body read `D` in `Tuner`.
4. Set kick body tail target to `100 ms`.
5. Load the click layer onto `Kick Click`.
6. Add `EQ Eight` to `Kick Click`.
7. Set `Kick Click` high-pass to `700 Hz`, slope `24 dB/oct`.
8. Add `Utility` to `Kick Click`.
9. Set `Kick Click` Utility Gain to `-8 dB`.
10. If the click is louder than the body, lower Utility Gain to `-10 dB` or `-12 dB`.

### Why
The kick must:
- anchor the tonic
- hit physically
- stay short enough for the bass to breathe

### Starting Spec
- kick body tuned to `D`
- kick body tail target `100 ms`
- kick body acceptable tail window `90–120 ms`
- click layer high-passed at `700 Hz`
- click layer Utility Gain `-8 dB` first pass
- both kick layers panned center

### Screenshot Set
- `drums-01-kick-body`
- `drums-02-kick-click-layer`

## Step 2: Program The Kick Pattern
### Action
Program the kick on every quarter note for the drop groove:
- beats `1`, `2`, `3`, `4`

Use short MIDI notes:
- make every kick MIDI note exactly `1/16` long on the first pass
- let the sample tail do the real sustain work

Keep the kick on-grid.

Exact first-pass `2`-bar clip entry:
1. Create one `2`-bar MIDI clip on `Kick Body`.
2. Set the piano-roll grid to `1/16`.
3. Place kick notes at:
   - `1.1.1`
   - `1.2.1`
   - `1.3.1`
   - `1.4.1`
   - `2.1.1`
   - `2.2.1`
   - `2.3.1`
   - `2.4.1`
4. Make every MIDI note `1/16` long.
5. Copy that MIDI to `Kick Click` if the click is running on a separate MIDI track.

### Why
The whole groove will lean against this fixed center.

Do not try to “make it more garage” by changing the kick rhythm. The garage feel comes from everything around it.

### Screenshot
- `drums-03-kick-pattern`

### Visual MIDI Requirement
- show one full bar
- the MIDI note should be visibly short enough that the sample tail, not the MIDI length, is doing the sustain work

## Step 3: Build The Clap Layer
### Action
1. Put the clap on beats `2` and `4`.
2. Use one main garage clap first.
3. Add a tighter snare/rim only if the clap disappears when hats are added.
4. Put the support rim/snare on its own separate track, not inside the clap track.
5. Set the main clap velocity to `118`.
6. Set support rim/snare velocity to `92`.
7. Set support rim/snare track fader `-6 dB` below the main clap track on the first pass.

Exact first-pass `2`-bar clip entry:
1. Create one `2`-bar MIDI clip on `Clap`.
2. Set the grid to `1/16`.
3. Place clap notes at:
   - `1.2.1`
   - `1.4.1`
   - `2.2.1`
   - `2.4.1`
4. If a support rim/snare exists, place it at the exact same positions on its own lane.

### Why
The clap is the second fixed anchor after the kick.

### Starting Spec
- placement: beats `2` and `4`
- velocity:
  - main clap `118`
  - support rim/snare `92`
- support track level: `-6 dB` below main clap

### Screenshot
- `drums-04-clap-layer`

### Visual MIDI Requirement
- show one bar with the clap on beats `2` and `4`
- if a support hit exists, make the layering visible in the screenshot

## Step 4: Add The Closed Hat Scaffold
### Action
1. Add a short closed hat on the offbeats.
2. Start simple.
3. Keep it on-grid.

Exact first-pass `2`-bar scaffold:
1. Create one `2`-bar MIDI clip on `Closed Hat`.
2. Set the grid to `1/16`.
3. Place hats at these offbeat `1/8` positions:
   - `1.1.3`
   - `1.2.3`
   - `1.3.3`
   - `1.4.3`
   - `2.1.3`
   - `2.2.3`
   - `2.3.3`
   - `2.4.3`
4. Start with those placements only before adding ghost hats.
5. Set velocities in a repeating pattern:
   - `1.1.3`: `78`
   - `1.2.3`: `88`
   - `1.3.3`: `74`
   - `1.4.3`: `92`
   - repeat the same shape in bar `2`

### Why
This is not the swing layer. It is the stable top scaffold that lets the later ghost hats read clearly.

### Starting Placement
- use offbeat `1/8` placements as the backbone
- keep the first loop minimal

### Velocity
- first-pass values: `78`, `88`, `74`, `92`, then repeat
- do not leave every closed hat at `100`

### Screenshot
- `drums-05-closed-hat-scaffold`

### Visual MIDI Requirement
- show at least one full bar so the scaffold pattern is readable before ghost hats are added

## Step 5: Add Ghost Hats
### Action
1. Use a shorter, lighter hat sample than the main closed hat if needed.
2. Place ghost hats on `1/16` subdivisions around the beat:
   - starter loop: use the `e` and `a` of beats `2` and `4` in both bars of the first `2`-bar loop
   - later additions can include the `e` of beat `1` and the `a` of beat `3`
3. If Ableton exposes timing offsets, push them late by `+4 ms` or `+9 ticks` on the first pass.
4. If Ableton does not expose timing offsets, leave the ghost hats on-grid for now and continue.
5. Do not push them earlier than the grid.
6. Do not push them later than `+7 ms` / `+16 ticks` during the first build.
7. Keep them quieter than the main closed hats.

How to read the placement numbers:
- Ableton's piano-roll position format is `bar.beat.sixteenth`
- `1.2.2` means:
  - bar `1`
  - beat `2`
  - second sixteenth slot inside beat `2`
- Count one beat as four sixteenth slots:
  - `.1` = the beat itself
  - `.2` = the `e`
  - `.3` = the `&`
  - `.4` = the `a`
- So `1.2.2` is the `e` of beat `2`
- `1.2.4` is the `a` of beat `2`
- `1.4.2` is the `e` of beat `4`
- `1.4.4` is the `a` of beat `4`

What a ghost hat is:
- a ghost hat is a quiet extra hat hit
- it is felt more than heard
- it should sit behind the main closed hat scaffold
- if it sounds like a main hat, its velocity is too high

Exact starter placements in the same `2`-bar clip:
1. Create or open the `Ghost Hat` clip.
2. Set the grid to `1/16`.
3. Place the starter ghost hats at:
   - `1.2.2`
   - `1.2.4`
   - `1.4.2`
   - `1.4.4`
   - `2.2.2`
   - `2.2.4`
   - `2.4.2`
   - `2.4.4`
4. If the groove still feels too empty later, add the next two optional placements:
   - `1.1.2`
   - `1.3.4`
5. Then mirror those in bar `2`:
   - `2.1.2`
   - `2.3.4`
6. After placing them, try to open the Note or Clip properties and nudge only the ghost hats late, not the main closed hats.
7. Do not gauge milliseconds by eye. Use one of these first-pass methods:
   - if Ableton shows milliseconds, set every starter ghost-hat offset to `+4 ms`
   - if Ableton shows ticks, set every starter ghost-hat offset to `+9 ticks`
   - if Ableton only lets you drag notes, zoom in and move each ghost hat a tiny amount to the right, less than a `1/64` note
   - if none of that is clear, leave ghost hats on-grid and continue
8. If you added the optional ghost hats, give those the same late offset only if you successfully offset the starter ghost hats.
9. Set starter ghost-hat velocities:
   - `1.2.2`: `42`
   - `1.2.4`: `56`
   - `1.4.2`: `46`
   - `1.4.4`: `62`
   - repeat the same values in bar `2`
10. If you add the optional ghost hats later, set them to velocity `38` first.

### Why
This is the main source of bounce.

If the ghost hats are not intentionally late, the track will sound like house with extra hats rather than UKG.

### Starting Velocity
- starter values: `42`, `56`, `46`, `62`
- optional added ghosts: `38`
- maximum first-pass ghost velocity: `70`

### Rule
- do not use one global swing preset instead of these manual offsets

### Screenshot Set
- `drums-06-ghost-hat-placement`
- `drums-07-ghost-hat-velocity`

### Visual MIDI Requirement
- show the full `2`-bar loop
- annotate which ghost hats are the “starter” pattern and which ones are later additions

## Step 6: Add The Open Hat
### Action
1. Place the open hat on selected offbeats.
2. Start with restrained use:
   - not every possible offbeat
3. Let it act as a phrase-lift marker.

Exact first-pass placement:
1. Create one `2`-bar MIDI clip on `Open Hat`.
2. Set the grid to `1/16`.
3. Start with the highest-priority placement only:
   - `1.4.3`
   - `2.4.3`
   - velocity `104`
4. If the section still needs more openness, add:
   - `1.2.3`
   - `2.2.3`
   - velocity `96`
5. If an open hat lands on the same exact slot as a closed hat, mute or remove the closed hat at that slot so the two hats do not stack awkwardly.

### Why
The open hat should help signal lift and openness.

It should not flood the groove.

If only one placement survives:
- keep the `&` of `4`
- that placement usually gives the strongest garage push

### Starting Placement
- begin with the `&` of `2` and/or `&` of `4`
- test whether both are needed

### Velocity
- `& of 4`: `104`
- optional `& of 2`: `96`

### Screenshot
- `drums-08-open-hat-placement`

### Visual MIDI Requirement
- show one bar clearly enough that `& of 4` is labeled as the highest-priority placement

## Step 7: Add The Shaker Lane
### Action
1. Program a lightly moving shaker line around the main hats.
2. Use velocity variation to create phrase lift.
3. Keep it humanized, but not sloppy.

Starting pattern:
- begin with continuous `1/8` notes
- do not move the whole shaker lane to constant `1/16` notes in the core loop
- phrase lift comes from velocity and a few targeted pickups

Exact first-pass `1`-bar shaker pattern:
1. Create one `1`-bar MIDI clip on `Shaker`.
2. Set the grid to `1/16`.
3. Place shaker notes at:
   - `1.1.1`
   - `1.1.3`
   - `1.2.1`
   - `1.2.3`
   - `1.3.1`
   - `1.3.3`
   - `1.4.1`
   - `1.4.3`
4. Duplicate that bar into bar `2` if you are building a `2`-bar loop.
5. Start the later phrase-lift pickup by testing one extra note at `2.4.4`, not by filling the entire clip with `1/16` notes immediately.
6. Set first-pass shaker velocities:
   - `1.1.1`: `72`
   - `1.1.3`: `84`
   - `1.2.1`: `76`
   - `1.2.3`: `88`
   - `1.3.1`: `74`
   - `1.3.3`: `86`
   - `1.4.1`: `78`
   - `1.4.3`: `94`
7. If you add the pickup at `2.4.4`, set its velocity to `82`.
8. If you duplicate this `1`-bar shaker pattern into a `2`-bar clip, use the same base placements in bar `2`:
   - `2.1.1`
   - `2.1.3`
   - `2.2.1`
   - `2.2.3`
   - `2.3.1`
   - `2.3.3`
   - `2.4.1`
   - `2.4.3`
9. Copy the same velocity shape into bar `2`, then add only the pickup at `2.4.4`.

### Why
The shaker often carries the `5–8 kHz` lift that makes drops feel more alive without adding new low-mid clutter.

### Velocity
- first-pass range: `72–94`
- phrase-end pickup: `82`
- last-bar lift version: add `+6` velocity to existing shaker hits, capped at `100`

### Screenshot
- `drums-09-shaker-lane`

### Visual MIDI Requirement
- show one bar of the shaker pattern clearly enough that velocity shaping is visible
- if extra `1/16` pickups are added later, capture a second screenshot showing where they enter

## Step 8: Set The Timing Policy
### Action
Apply these timing rules:
- kick: on-grid
- clap: on-grid
- main closed hats: mostly on-grid
- ghost hats: intentionally late
- shakers: lightly humanized around the grid

Ableton click path for the late ghost-hat offsets:
1. Click one ghost-hat note in the piano roll.
2. Open the lower Note box or note-properties panel.
3. Find the timing offset / nudge field for that note.
4. If the field exists, start by pushing the note later by `+4 ms` or `+9 ticks`.
5. If the groove is still too stiff after listening in context, test `+6 ms` / `+13 ticks`, then `+7 ms` / `+16 ticks`.
6. Do not apply this offset to the kick, clap, or the main closed-hat scaffold.
7. For this tutorial's first pass, use `+4 ms` / `+9 ticks` on all starter ghost hats before testing other values.
8. If Ableton shows ticks instead of milliseconds, use this conversion at `140 BPM`:
   - `+4 ms` is about `+9 ticks`
   - `+6 ms` is about `+13 ticks`
   - `+7 ms` is about `+16 ticks`
9. If Ableton does not expose milliseconds or ticks, do not guess a number:
   - zoom in horizontally in the piano roll
   - turn the grid to `1/64`
   - drag each ghost hat just slightly to the right, less than one `1/64` grid step
   - if that feels imprecise, undo it and leave ghost hats on-grid until the rest of the groove is built

### Why
Asymmetric timing creates groove without destroying impact.

Random looseness is not the same thing as swing.

### Screenshot
- `drums-10-timing-policy`

## Step 9: Build The Drum Bus
### Action
On the `Drums` group, build this starting chain:
1. `EQ Eight`
2. `Glue Compressor`
3. `Saturator` or soft clip stage
4. `Utility`

### Starting Settings
#### EQ Eight
- leave flat on the first pass
- if there is low rumble that is not the kick body, turn on band `1`:
  - type: high-pass
  - frequency: `25 Hz`
  - slope: `24 dB/oct`

#### Glue Compressor
- ratio: `2:1`
- attack: `10 ms`
- release: `Auto`
- threshold: lower until the loudest section shows `1 dB` of gain reduction
- makeup: `off`

#### Saturator / clip stage
- drive: `+1 dB`
- output: `-1 dB`
- soft clip: `On`

#### Utility
- width: `100%`
- gain: `0 dB`

### Why
The drums need to feel glued, not flattened.

### Screenshot Set
- `drums-11-bus-overview`
- `drums-12-glue-compressor`

## Step 10: Build A 16-Bar Micro-Architecture
### Action
Build this as a `16`-bar drum section starting at local clip position `1.1.1`.

If this clip later lives at `Drop A` in Arrangement View, local bar `1` becomes full timeline bar `33`.
Do the programming in the clip first so the piano roll still reads `1.1.1`, `5.1.2`, `16.4.4`, etc.

What "micro-architecture" means here:
- the same basic groove repeats for `16` bars
- each `4`-bar block gets one small extra detail
- the section grows without sounding like four unrelated drum loops

Do not invent a new drum pattern for each block.
Copy the same `2`-bar loop first, then make the exact edits below.

Before you start, your lanes should be separate:
- `Kick Body`
- `Kick Click`
- `Clap`
- `Closed Hat`
- `Ghost Hat`
- `Open Hat`
- `Shaker`
- optional `Top Loop`
- optional `Drum Fill FX`

If you do not have a `Top Loop` lane yet, skip every `Top Loop` instruction in this step.
Do not create a top loop just because this step mentions it.

In this step, "restrained" means this exactly:
- no `Top Loop` clip in bars `1–12`
- no constant `1/16` shaker pattern
- no shaker pickup notes in bars `1–4`
- open hat only on `x.4.3` until bars `9–12`
- ghost hats start sparse and get denser later

### Build The 16-Bar Copy First
1. Make sure the `2`-bar drum loop from Steps 2–7 works.
2. Duplicate that `2`-bar loop until every drum lane covers bars `1–16`.
3. The copies should cover:
   - loop copy `1`: bars `1–2`
   - loop copy `2`: bars `3–4`
   - loop copy `3`: bars `5–6`
   - loop copy `4`: bars `7–8`
   - loop copy `5`: bars `9–10`
   - loop copy `6`: bars `11–12`
   - loop copy `7`: bars `13–14`
   - loop copy `8`: bars `15–16`
4. Leave the kick, kick click, clap, and closed-hat placements unchanged across all `16` bars on the first pass.
5. The changing lanes in this step are only:
   - `Ghost Hat`
   - `Open Hat`
   - `Shaker`
   - optional `Top Loop`
   - optional `Drum Fill FX`

### Bars 1-4: Plain Groove
Use bars `1–4` to state the groove without extra lift.

Do this:
1. Keep the starter ghost hats only.
2. For every bar `1–4`, the `Ghost Hat` lane should only have:
   - `x.2.2`
   - `x.2.4`
   - `x.4.2`
   - `x.4.4`
3. Written out, that means:
   - bar `1`: `1.2.2`, `1.2.4`, `1.4.2`, `1.4.4`
   - bar `2`: `2.2.2`, `2.2.4`, `2.4.2`, `2.4.4`
   - bar `3`: `3.2.2`, `3.2.4`, `3.4.2`, `3.4.4`
   - bar `4`: `4.2.2`, `4.2.4`, `4.4.2`, `4.4.4`
4. Keep the `Open Hat` only on the `&` of beat `4`:
   - `1.4.3`
   - `2.4.3`
   - `3.4.3`
   - `4.4.3`
5. Keep the `Shaker` on the `1/8` pattern only:
   - in every bar, use `x.1.1`, `x.1.3`, `x.2.1`, `x.2.3`, `x.3.1`, `x.3.3`, `x.4.1`, `x.4.3`
6. Delete shaker pickup notes such as `2.4.4` or `4.4.4` from bars `1–4` if they are already there.
7. Do not place any `Top Loop` clip in bars `1–4`.
8. Do not place any `Drum Fill FX` hit in bars `1–4`.

### Bars 5-8: Deepen The Pocket
Bars `5–8` should still be the same groove, but with a little more ghost-hat bounce.

Add these extra `Ghost Hat` notes:
- `5.1.2`, `5.3.4`
- `6.1.2`, `6.3.4`
- `7.1.2`, `7.3.4`
- `8.1.2`, `8.3.4`

Set these added ghost hats to velocity `38` first.
If you successfully delayed the earlier ghost hats by `+4 ms` or `+9 ticks`, delay these added ghost hats by the same amount.
If you did not delay the earlier ghost hats, leave these on-grid too.

Keep these lanes unchanged in bars `5–8`:
- `Kick Body`
- `Kick Click`
- `Clap`
- `Closed Hat`
- `Open Hat`

For `Shaker`:
- keep the same `1/8` pattern as bars `1–4`
- add one phrase pickup only at `8.4.4`
- set `8.4.4` to velocity `82`

For `Top Loop`:
- keep it empty or muted in bars `5–8`

For `Drum Fill FX`:
- keep it empty in bars `5–8`

### Bars 9-12: Add Slight Top Motion
Bars `9–12` should lift slightly without becoming the final push.

Keep all the ghost hats from bars `5–8`.
That means each bar keeps:
- starter ghosts at `x.2.2`, `x.2.4`, `x.4.2`, `x.4.4`
- added ghosts at `x.1.2` and `x.3.4`

On `Open Hat`, add `& of 2` only every second bar:
- add `10.2.3`
- add `12.2.3`

Do not add `9.2.3` or `11.2.3` on the first pass.

On `Shaker`:
- keep the same `1/8` note placements
- raise the existing shaker velocities in bars `9–12` by `+6`, capped at velocity `100`
- add one phrase pickup at `12.4.4`
- set `12.4.4` to velocity `88`

For `Top Loop`:
- first pass: still keep it empty or muted in bars `9–12`
- if the groove sounds too empty after everything else is working, add a quiet high-passed top loop from `9.1.1` to `13.1.1`
- if you add it, set its track fader around `-24 dB` and high-pass it around `300 Hz`

For `Drum Fill FX`:
- keep it empty in bars `9–12`

### Bars 13-16: Push Into The Next Section
Bars `13–16` are the only place this `16`-bar phrase should feel clearly like it is pushing forward.

Keep the denser ghost-hat version:
- starter ghosts at `x.2.2`, `x.2.4`, `x.4.2`, `x.4.4`
- added ghosts at `x.1.2` and `x.3.4`

Add one more pair of ghost hats only in bars `15–16`:
- `15.1.4`
- `15.3.2`
- `16.1.4`
- `16.3.2`

Set those four final-push ghost hats to velocity `34`.
They should be felt, not heard as new main hats.

On `Open Hat`:
- keep `x.4.3` in every bar
- keep `14.2.3`
- keep `16.2.3`
- do not add `13.2.3` or `15.2.3` on the first pass

On `Shaker`:
- keep the same `1/8` note placements
- use the same `+6` velocity lift as bars `9–12`
- add one final pickup at `16.4.4`
- set `16.4.4` to velocity `92`

For optional `Top Loop`:
- if you have no `Top Loop`, skip this
- if you have a `Top Loop`, place it only from `13.1.1` to `17.1.1`
- set its track fader around `-24 dB`
- high-pass it around `300 Hz`
- if it makes the section sound busy, mute it again

For `Drum Fill FX` or a spare clap/rim lane:
- place one short hit at `16.4.3`
- place one shorter follow-up hit at `16.4.4`
- set both fill hits to velocity `70` first
- if the fill clashes with the open hat at `16.4.3`, mute the `Open Hat` at `16.4.3` and let the fill own that slot

### Check The Shape
Play bars `1–16`, then loop only bars `13–16` into the next section.

The section should read like this:
- bars `1–4`: basic groove
- bars `5–8`: same groove with more pocket
- bars `9–12`: same groove with a little more top lift
- bars `13–16`: same groove pushing into the next section

If bars `1–4` already sound as busy as bars `13–16`, remove notes from bars `1–4`.
If bars `13–16` do not feel more energetic than bars `1–4`, add level or velocity to the existing shaker/fill before adding a new instrument.

### Why
If the drums repeat identically for all `16` bars, the section is not finished.

### Screenshot
- `drums-13-16bar-micro-architecture`

### Visual MIDI Requirement
- show the full `16` bars in one screenshot
- annotate what changes at bars `5`, `9`, and `13`

## Step 11: Add Phrase-End Fills
### Action
1. Create one `1`-bar phrase-end fill.
2. Use it selectively at `8`- or `16`-bar boundaries.
3. Keep it short and functional.

What `Drum Fill FX` means:
- it is a separate drum lane used only for little transition hits
- it is **not** a full drum rack
- it is **not** the main kick / clap / hat groove
- it can hold either:
  - one short fill sample, or
  - a few copied hits from existing drum sounds

Use one of these two beginner-safe options:
1. Existing-drum option:
   - use the same clap/rim sound you already have
   - place the fill hits on a spare clap/rim lane
   - this is the safest first pass if you do not have a fill sample
2. FX-sample option:
   - use one short snare fill, rim fill, noise tick, or reverse-tail sample
   - put it on the `Drum Fill FX` lane
   - reject any fill sample with a long tail that spills into the next section

Recommended first pass:
- use the existing-drum option
- copy your clap/rim sound to a spare fill lane
- make the fill from short hits, not a premade loop

Exact first-pass fill you can type in immediately:
1. Create a new `1`-bar MIDI clip on a spare clap/rim lane or `Drum Fill FX` lane.
2. Load or reuse one short sound:
   - safest: existing clap/rim
   - alternate: one short fill FX sample
3. Set the grid to `1/16`.
4. Place hits at:
   - `1.3.3`
   - `1.4.1`
   - `1.4.3`
   - `1.4.4`
5. Keep the MIDI notes `1/16` long or shorter.
6. Set fill velocity lower than the main clap first:
   - start at velocity `70`
   - raise only if the fill disappears in context
7. When you paste this fill to the end of a real section, place the fill clip so its `1.1.1` starts at the first bar of the final phrase-end bar:
   - start it at `16.1.1` for the `16 -> 17` boundary
   - start it at `32.1.1` for the `32 -> 33` boundary
   - follow the same rule for `48`, `64`, `80`, `96`, `112`, `128`, and `144`

Arrangement placement rule:
- the fill clip itself still uses local positions such as `1.3.3` and `1.4.4`
- the arrangement position tells you where that `1`-bar fill starts in the song
- example:
  - if you paste the fill clip at `32.1.1`, the fill hits will land at:
    - `32.3.3`
    - `32.4.1`
    - `32.4.3`
    - `32.4.4`

Boundary strength map:
1. Small reveal boundaries:
   - `16 -> 17`
   - `64 -> 65`
   - `128 -> 129`
   - `144 -> 145`
   Use only the shorter two-hit ending:
   - `1.4.1`
   - `1.4.3`
2. Medium boundaries:
   - `32 -> 33`
   - `80 -> 81`
   - `96 -> 97`
   Use the full four-hit pattern, but keep the hits quieter than the main redrops.
3. Main landing boundaries:
   - `48 -> 49`
   - `112 -> 113`
   Use the full four-hit pattern and clear a little more top-end space right after it:
   - mute the `Open Hat` at `x.4.3`
   - let the fill own `x.4.3` and `x.4.4`
   - bring the `Open Hat` back on the next bar

### Why
Transitions feel exciting because the drums acknowledge the phrase boundary.

### Starting Fill Ideas
- snare roll in the last `2` beats
- extra hat density in the last bar
- one-beat drum drop before the return

### Screenshot
- `drums-14-phrase-end-fill`

### Visual MIDI Requirement
- show the local `1`-bar fill clip on its own
- show one arrangement example where that same fill clip is placed at a real song bar such as `32.1.1`

## Step 12: Build The Drop Core And Drop Lift Variants
### Action
Create:
- one `2`-bar drop core variant
- one `2`-bar drop lift variant

The lift variant should get bigger through:
- more top-end density
- tighter phrase pressure
- not a new kick pattern

### Why
The kick remains the anchor. Growth comes from the tops and the phrase edge.

Concrete lift changes:
- make the `e` of beat `1` and the `a` of beat `3` part of the regular loop instead of occasional additions
- raise last-bar shaker velocity by `+6`, capped at `100`
- add open hat `& of 2` at velocity `96`
- if a top loop exists, raise it by `+1.5 dB` in the lift before adding another percussion lane

Exact lift-variant MIDI changes in a `2`-bar clip:
1. On `Ghost Hat`, add:
   - `1.1.2`
   - `1.3.4`
   - `2.1.2`
   - `2.3.4`
2. Set those added ghost hats to velocity `38`.
3. Nudge those added ghost hats late by the same amount as the starter ghosts:
   - `+4 ms`
   - or `+9 ticks`
4. On `Open Hat`, add:
   - `1.2.3` at velocity `96`
   - `2.2.3` at velocity `96`
5. On `Shaker`, raise only the final bar's existing hits by `+6` velocity points:
   - `2.1.1`
   - `2.1.3`
   - `2.2.1`
   - `2.2.3`
   - `2.3.1`
   - `2.3.3`
   - `2.4.1`
   - `2.4.3`
6. Do not change `Kick Body`, `Kick Click`, or `Clap` MIDI in the lift variant.

### Screenshot
- `drums-15-drop-core-vs-lift`

## Step 13: A/B Against References
### Action
Bounce or loop `full drums`.

Compare against:
- `Interplanetary Criminal - Slow Burner`
  - ghost-hat drag
  - phrase-end movement
- `KETTAMA - It Gets Better`
  - weight and density
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - how the tops leave room for a rolling bassline

### What To Listen For
- does the groove bounce before the bass even enters?
- do the hats feel intentionally late or just messy?
- does the kick feel physical without sounding harsh?
- is there enough space left for the bass floor?

Expected answer:
- the starter loop should feel sparse but already bouncy before any lift additions
- the lift version should have noticeably more top motion without changing the kick pattern
- the ghost-hat density should still feel countable, not like a constant `1/16` wash

## Troubleshooting
### Problem: “The drums feel stiff.”
Fix order:
1. open the `Ghost Hat` MIDI clip and check the ghost hats are nudged `+4 ms`
2. if still stiff, move ghost hats to `+6 ms`
3. check closed-hat velocities are not all identical
4. only then change samples

### Problem: “The groove feels sloppy.”
Fix order:
1. pull ghost hats from `+6 ms` back to `+4 ms`
2. if still sloppy, pull them to `+2 ms`
3. remove random humanization from kick and clap
4. keep kick and clap exactly on-grid

### Problem: “The drums feel exciting solo but too crowded with bass.”
Fix order:
1. mute optional open hats at `1.2.3` and `2.2.3`
2. lower shaker by `-2 dB`
3. high-pass any top loop at `300 Hz`
4. check the drum bus is not clipping or adding more than `1 dB` gain reduction

### Problem: “The drops don’t lift.”
Fix order:
1. check bars `13–16` contain the phrase-end fill at `16.4.3` and `16.4.4`
2. raise last-bar shaker velocities by `+6`, capped at `100`
3. add optional open hat at `& of 2` with velocity `96`
4. check the section has the bar `5`, bar `9`, and bar `13` micro-architecture changes

### Problem: “I followed the spec and it still sounds wrong.”
Fix order:
1. loudness-match the references
2. listen to the drums alone in mono
3. compare hat timing before sample tone
4. check ghost hats are not louder than velocity `70`
5. check the kick and clap are still on-grid
6. rebuild the ghost hats before replacing the whole drum kit

## Checkpoint Deliverables
At the end of Part 2, save:
- `Drums` MIDI
- `Drums` group chain
- one `2`-bar drop core variant
- one `2`-bar drop lift variant
- one `full drums` bounce

## Capture Checklist
Capture these artifacts while building:
- screenshots:
  - `drums-01-kick-body`
  - `drums-02-kick-click-layer`
  - `drums-03-kick-pattern`
  - `drums-04-clap-layer`
  - `drums-05-closed-hat-scaffold`
  - `drums-06-ghost-hat-placement`
  - `drums-07-ghost-hat-velocity`
  - `drums-08-open-hat-placement`
  - `drums-09-shaker-lane`
  - `drums-10-timing-policy`
  - `drums-11-bus-overview`
  - `drums-12-glue-compressor`
  - `drums-13-16bar-micro-architecture`
  - `drums-14-phrase-end-fill`
  - `drums-15-drop-core-vs-lift`
- audio:
  - `checkpoint-full-drums.wav`
- notes:
  - which reference forced the biggest timing change
  - whether the groove changed more from MIDI or sample changes
  - what the phrase-end fill solved

## Lesson Conversion Notes
When this becomes the guided lesson:
- split it into:
  - kick foundation
  - hat timing
  - clap and shaker support
  - drum bus
  - micro-architecture
  - A/B checkpoint
- keep the ghost-hat timing doctrine visible:
  - `intentionally late, not randomly loose`
