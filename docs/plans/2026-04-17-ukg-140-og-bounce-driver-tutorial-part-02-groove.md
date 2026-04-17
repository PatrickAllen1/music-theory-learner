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

## Reference Axis
Primary A/B for this part:
- `Interplanetary Criminal - Slow Burner`
  - listen for ghost-hat drag and phrase-end groove movement
- `KETTAMA - It Gets Better`
  - listen for physical kick weight and density

Secondary check:
- `Y U QT - NRG`
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

## Sample Selection Rules
### Kick
- choose one short, tunable 909/garage-compatible body sample
- choose one short click/transient layer
- kick tail should stay around `90–120 ms`
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
1. Load the kick body sample.
2. Tune it to `D` if needed.
3. Load the click layer on a separate chain or track.
4. High-pass the click so it does not add false low end.
5. Blend the click until the kick reads clearly on small speakers, then stop.

### Why
The kick must:
- anchor the tonic
- hit physically
- stay short enough for the bass to breathe

### Starting Spec
- kick body tuned to `D`
- kick body tail `~90–120 ms`
- click layer high-passed and quieter than the body

### Screenshot Set
- `drums-01-kick-body`
- `drums-02-kick-click-layer`

## Step 2: Program The Kick Pattern
### Action
Program the kick on every quarter note for the drop groove:
- beats `1`, `2`, `3`, `4`

Use short MIDI notes:
- start with roughly `1/16` note MIDI length
- let the sample tail do the real sustain work

Keep the kick on-grid.

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
2. If needed, add a tighter snare/rim under it.
3. Keep the support quieter than the main clap.

### Why
The clap is the second fixed anchor after the kick.

### Starting Spec
- placement: beats `2` and `4`
- velocity:
  - main clap `110–127`
  - support slightly lower

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

### Why
This is not the swing layer. It is the stable top scaffold that lets the later ghost hats read clearly.

### Starting Placement
- use offbeat `1/8` placements as the backbone
- keep the first loop minimal

### Velocity
- `60–110`
- do not keep every hat the same velocity

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
3. Push them slightly late:
   - roughly `5–15` ticks behind the grid
4. Keep them quiet enough that they are felt before they are consciously heard.

### Why
This is the main source of bounce.

If the ghost hats are not intentionally late, the track will sound like house with extra hats rather than UKG.

### Starting Velocity
- `30–70`

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
- `90–120`

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
- only move to `1/16` density if the section needs more lift later
- if the phrase still feels too empty, add single extra `1/16` pickups near the phrase boundary rather than converting the whole lane too early

### Why
The shaker often carries the `5–8 kHz` lift that makes drops feel more alive without adding new low-mid clutter.

### Velocity
- `70–100`
- let the last bar of a phrase rise slightly

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
- clean up obvious sub spill if needed
- leave room for kick and bass to own the bottom cleanly

#### Glue Compressor
- ratio `2:1` or `4:1`
- slower attack so the kick still punches
- release timed to the groove

#### Saturator / clip stage
- enough to add density
- not enough to flatten hat motion

Starting range:
- begin around `10–20%` of the intended drive amount and increase only if the loop still feels too thin

### Why
The drums need to feel glued, not flattened.

### Screenshot Set
- `drums-11-bus-overview`
- `drums-12-glue-compressor`

## Step 10: Build A 16-Bar Micro-Architecture
### Action
Inside one `16`-bar drop section, give each four-bar block a job:
- `Bars 1–4`: establish groove
- `Bars 5–8`: deepen pocket
- `Bars 9–12`: add slight top motion
- `Bars 13–16`: push into the next section

### Practical Moves
- `Bars 1–4`
  - keep the top loop and shaker support restrained
  - use only the starter ghost-hat pattern
  - keep the open hat to `& of 4` only if possible
- `Bars 5–8`
  - add the `e` of beat `1` and the `a` of beat `3` if they were not present yet
- `Bars 9–12`
  - raise shaker velocity by roughly `5–10` points
  - consider adding one extra open-hat emphasis on `& of 2` every second bar
- `Bars 13–16`
  - use a fill, riser, or brief cut
  - allow the densest ghost-hat version here only

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

### Why
Transitions feel exciting because the drums acknowledge the phrase boundary.

### Starting Fill Ideas
- snare roll in the last `2` beats
- extra hat density in the last bar
- one-beat drum drop before the return

### Screenshot
- `drums-14-phrase-end-fill`

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
- slightly tighten shaker lift toward phrase ends and raise the last-bar velocity by roughly `5–10` points
- consider one extra open-hat emphasis rather than changing the kick
- if a top loop exists, let it become a little more audible here before reaching for another percussion lane

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
- `Y U QT - NRG`
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
1. check ghost-hat timing
2. check velocity variation
3. only then change samples

### Problem: “The groove feels sloppy.”
Fix order:
1. pull ghost hats closer to the grid
2. reduce random humanization
3. keep kick and clap perfectly fixed

### Problem: “The drums feel exciting solo but too crowded with bass.”
Fix order:
1. reduce top-loop density
2. reduce low-mid drum spill
3. simplify the open hats

### Problem: “The drops don’t lift.”
Fix order:
1. add phrase-end fills
2. raise shaker/open-hat energy slightly
3. check whether the section has any micro-architecture at all

### Problem: “I followed the spec and it still sounds wrong.”
Fix order:
1. loudness-match the references
2. listen to the drums alone in mono
3. compare hat timing, not just sample tone
4. if needed, rebuild the ghost hats before replacing the whole drum kit

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
