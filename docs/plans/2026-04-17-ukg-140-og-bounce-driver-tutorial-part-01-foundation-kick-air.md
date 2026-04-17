# UKG 140 OG Bounce Driver: Tutorial Part 1 — Foundation (Kick + Air Ceiling)

## Purpose
Teach the learner how to build the physical center and top ceiling of `ukg-140-og-bounce-driver` before writing the rest of the record.

This part should establish:
- a layered kick tuned to `D`
- a short enough kick tail that the bass can breathe later
- a quiet air bed that creates height from the very start of the track

It should not yet try to complete the full groove. `Part 2` takes this kick lane and turns it into the full top-drum pocket.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-part-02-groove.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-02-groove.md)

## Outcome
By the end of this part, the learner should have:
- one layered kick lane:
  - body sample
  - click layer
  - tuned to `D`
  - tail controlled around `90–120 ms`
- one quiet air layer that can live across the full track
- one simple `4`-bar checkpoint bounce of kick + air

## Time Estimate
- `20–30 minutes`

## Prerequisites
- learner can load one-shots into `Simpler`
- learner can use:
  - `Transpose`
  - `Detune`
  - `EQ Eight`
  - `Utility`
- the session from `Part 0` is already set to:
  - `140 BPM`
  - correct groups / returns
  - references loaded and gain-matched

## What The Learner Should Understand Before Starting
This chapter is about two things only:
- physical center
- vertical ceiling

The kick gives the record its floor.
The air layer gives the record its height.

If either is wrong:
- the bass chapter becomes harder than it should be
- the groove chapter gets built on the wrong foundation
- the arrangement later feels flat or sealed in

## Reference Axis
Primary A/B for this part:
- `KETTAMA - It Gets Better`
  - listen for kick weight and density

Secondary check:
- `Interplanetary Criminal - Slow Burner`
  - listen for how the record already has height and atmosphere even when the full mix is not firing yet

## Files / Assets Needed
- `Drums` group
- `Air` track or group
- `Return C: long filtered hall`
- one short tunable kick body sample
- one short click / transient layer
- `Ableton Core Library` 909-compatible samples are acceptable first-pass choices if exact external packs are not locked yet

## Step 1: Choose The Kick Body And Click
### Action
Choose:
- one short, tunable 909/garage-compatible kick body
- one short upper click / transient layer

Selection rules:
- body sample should carry the low-end weight
- click layer should help the kick read on smaller systems
- neither sample should have a long baked-in reverb tail

### Why
The kick needs two jobs:
- weight
- definition

Trying to get both from one badly chosen sample usually creates a kick that sounds huge in solo and vague in the track.

### Starting Source Recommendation
- use `Ableton Core Library` / stock 909-compatible material first if exact external sample packs are not locked yet

### Screenshot
- `foundation-01-kick-sample-choice`

## Step 2: Tune The Kick Body To `D`
### Action
1. Load the kick body sample into `Simpler`.
2. Use `Transpose` to get the kick body close to `D`.
3. Use `Detune` for the last fine adjustment.
4. Check the kick against a `D` reference note if needed.
5. Keep the click layer unpitched unless it obviously fights the body.

### Why
The kick does not need to sing a melody, but it should reinforce the key center rather than fight it.

### Rule
- tune by ear and verification
- not by guesswork

### Screenshot Set
- `foundation-02a-kick-simpler-pitch`
- `foundation-02b-kick-tuning-check`

## Step 3: Set The Kick Tail
### Action
Shape the kick so the body tail lands around `90–120 ms`.

Practical method:
- adjust sample start / fade if needed
- shorten the sustain / decay behavior only enough to keep the tail controlled
- keep enough body that the kick still feels physical

Do not over-shorten it into a papery click.

### Why
If the tail is too long:
- the bass chapter will need too much sidechain
- the groove will feel blurrier than intended

If the tail is too short:
- the kick loses floor weight

### Starting Spec
- body tuned to `D`
- tail around `90–120 ms`
- strong enough in solo to feel physical
- short enough that the bass can later breathe beside it

### Screenshot
- `foundation-03-kick-tail-shape`

## Step 4: Layer The Click And Balance The Kick
### Action
1. Put the click on a separate track or chain.
2. High-pass the click so it adds no false low end.
3. Blend the click until the kick speaks clearly.
4. Stop before the click becomes the identity of the kick.

### Why
The click is support.
The body is still the instrument.

### Rule
- if the kick sounds bright but not heavy, the click is too loud

### Screenshot Set
- `foundation-04a-kick-click-eq`
- `foundation-04b-kick-layer-balance`

## Step 5: Program The Foundation Kick Pattern
### Action
Program the kick on every quarter note for a simple `4`-bar foundation loop:
- beats `1`, `2`, `3`, `4`

Use short MIDI notes:
- start around `1/16` MIDI length
- let the sample tail do the real sustain

Keep the kick perfectly on-grid.

### Why
This chapter is not where the garage feel gets created.
This chapter is where the fixed center gets established.

`Part 2` will build the clap, hats, ghost hats, shaker, and micro-architecture around this exact fixed kick lane.

### Screenshot
- `foundation-05-kick-pattern`

### Visual MIDI Requirement
- show one full bar
- make the MIDI visibly short enough that the tail is sample-driven, not MIDI-length-driven

## Step 6: Build The Quiet Air Ceiling
### Action
Create an air layer in `Serum 2`:
- noise oscillator only
- no tonal oscillators by default
- high-pass aggressively so it behaves like ceiling, not a pad
- keep any movement tiny and slow if needed

Route most of the sense of space from:
- `Return C: long filtered hall`

not from drowning the patch itself in wet reverb.

### Why
The air layer should create:
- height
- breath
- ceiling

It should not create:
- melody
- obvious hiss
- a fake pad on top of the song

### Starting Spec
- noise-only source
- aggressively high-passed
- quiet in level
- most audible later in the break
- already present softly from the start

### Screenshot Set
- `foundation-06a-air-patch-source`
- `foundation-06b-air-return-routing`

## Step 7: Set The Initial Air Level
### Action
Bring the air layer in quietly against the kick.

Target feeling:
- you miss it when muted
- but you do not notice it as its own musical statement when active

Check it in context:
- with kick only
- then with the reference playing quietly afterward

### Why
Air is a support layer.
If it announces itself too early, later sections lose their sense of opening upward.

### Rule
- ceiling, not spotlight

### Screenshot
- `foundation-07-air-level-in-context`

## Step 8: Bounce And A/B The Foundation
### Action
Bounce `4` bars of:
- kick
- air

Compare against the references.

What to check:
- does the kick feel physically centered without sounding harsh?
- does the record already feel tall enough to hold later layers?
- does the air feel like height rather than hiss?

### Expected Answer
- the kick should feel heavy and short, not flabby
- the air should feel quiet but necessary
- the combination should already suggest a club record, even before bass or hook

## Troubleshooting
### Problem: “The kick feels huge solo but weak in context.”
Fix order:
1. lower the click slightly
2. shorten the kick tail a bit
3. re-check the tuning against `D`

### Problem: “The kick feels clicky, not weighty.”
Fix order:
1. lower the click layer
2. confirm the body sample still owns the low end
3. choose a better body sample before over-processing

### Problem: “The air sounds like hiss.”
Fix order:
1. lower the air level
2. high-pass it more aggressively
3. reduce broadband noise and let `Return C` create the space instead

### Problem: “The air sounds like a pad.”
Fix order:
1. remove tonal oscillators
2. reduce obvious movement
3. make it less melodic and more textural

## What Must Be Captured For Later Lesson Conversion
- kick body sample screenshot
- kick tuning screenshot
- kick tail / layering screenshot
- air patch screenshot
- kick + air checkpoint bounce
