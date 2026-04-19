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
  - tail controlled inside `90–120 ms`
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
- learner has access to a tuner:
  - Ableton `Tuner`
  - or a third-party tuner plugin
  - or a temporary `D1` / `D2` sine reference for ear-based tuning if no tuner device is available
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

Timing reminder for this part:
- positions like `1.1.1` are local clip or piano-roll positions
- later full-song bars such as `33.1.1` or `97.1.1` are Arrangement View positions

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

Plain-English kick terms used in this chapter:
- `kick body`: the low thump part of the kick, the part you feel in your chest
- `kick click`: the short upper tick that helps the kick read on smaller speakers
- if you only have one usable kick sample right now, load it on `Kick Body` first and leave `Kick Click` empty until Step `4`
- `Transpose`: coarse pitch movement in semitone steps, like moving a sample from `C` to `D`
- `Detune`: fine pitch movement in cents, used after `Transpose` gets the sample close
- `Tuner`: Ableton's device that tells you the note name it hears from the kick body

## Step 1: Choose The Kick Body And Click
### Action
1. On the `Kick Body` track, load one short, tunable 909/garage-compatible kick body sample.
2. On the `Kick Click` track, load one short upper click / transient sample.
3. Read the jobs in plain English before choosing:
   - `Kick Body` should sound like the low thump
   - `Kick Click` should sound like the little tick at the front
4. If the sample you loaded sounds like a full finished kick with both low thump and bright tick already built in, use it as `Kick Body` first and do not force a second layer yet.
5. Solo `Kick Body` and reject any sample that already has:
   - a long roomy tail
   - obvious stereo width
   - a click that is already too bright to layer
6. Solo `Kick Click` and reject any click sample that has:
   - obvious low end
   - a long noisy tail
7. Leave both tracks on their own channels. Do not combine them into one rack for this tutorial.

What a `fader` is:
- the fader is the track volume control
- in Ableton Session View, it is the vertical slider near the bottom of each track
- the number beside or under it is the level in `dB`
- when this tutorial says "set the `Kick Body` fader to `-10 dB`," click the volume number/slider on the `Kick Body` track and drag until it reads `-10.0 dB`
- if dragging is too sensitive, click the number and type `-10`, then press `Enter`

Concrete first-pass sample test:
1. Solo `Kick Body`.
2. Turn your monitor volume down before auditioning.
3. Pick a sample where the first impression is `low thump`, not `bright tick`.
4. If you can still hear the kick tail ringing after the next quarter note at `140 BPM`, reject it for this first pass.
5. Solo `Kick Click`.
6. Pick a sample where the first impression is `tick`, `snap`, or `front edge`.
7. If the click sample has a bass note or sub thump, reject it. The click layer must not create a second kick body.
8. Set `Kick Body` fader to `-10 dB` for the first pass.
9. Set `Kick Click` fader to `-18 dB` for the first pass.
10. Keep both panned center.

Low-frequency body check:
- after tuning, the kick body should have its main low thump below `80 Hz`
- `D1` is about `36.7 Hz`
- `D2` is about `73.4 Hz`
- if the tuner or analyzer mostly shows a high `D` like `D3` or `D4`, that sample is probably too high to be the kick body
- if the sample has no obvious low thump below `80 Hz`, move it to `Kick Click` or reject it and pick another body sample

### Why
The kick needs two jobs:
- weight
- definition

Trying to get both from one badly chosen sample usually creates a kick that sounds huge in solo and vague in the track.

Quick listening test:
- if the sample mainly says `thump`, it belongs on `Kick Body`
- if the sample mainly says `tick`, it belongs on `Kick Click`
- if it already says both, start with it on `Kick Body` and only add a click later if the kick disappears on small speakers

### Starting Source Recommendation
- use `Ableton Core Library` / stock 909-compatible material first if exact external sample packs are not locked yet

### Screenshot
- `foundation-01-kick-sample-choice`

## Step 2: Tune The Kick Body To `D`
### Action
1. Load the kick body sample into `Simpler`.
2. Add Ableton `Tuner` after `Simpler` on the `Kick Body` track.
3. Understand what `Transpose` means before touching it:
   - `Transpose` moves the sample in semitone steps
   - `+1` means one semitone higher
   - `-1` means one semitone lower
   - `12` semitones = one octave
4. Trigger the kick repeatedly and watch the note name in `Tuner`.
5. Use `Transpose` first to move the kick body until the tuner note name reads `D`:
   - if the tuner reads `C`, move `Transpose` to `+2`
   - if the tuner reads `C#`, move `Transpose` to `+1`
   - if the tuner reads `D`, leave `Transpose` where it is
   - if the tuner reads `D#`, move `Transpose` to `-1`
   - if the tuner reads `E`, move `Transpose` to `-2`
   - if the tuner reads `F`, move `Transpose` to `-3`
   - if the tuner reads `F#`, move `Transpose` to `-4`
   - if the tuner reads `G`, move `Transpose` to `-5`
   - if the tuner reads `G#`, move `Transpose` to `+6` or `-6`; choose the one that keeps the kick sounding more natural
   - if the tuner reads `A`, move `Transpose` to `+5`
   - if the tuner reads `A#` / `Bb`, move `Transpose` to `+4`
   - if the tuner reads `B`, move `Transpose` to `+3`
6. Do not panic about octave number at this stage:
   - `D1`, `D2`, or `D3` are all still `D`
   - the important thing is the note name first
   - the next check decides whether that `D` is low enough to function as kick body
7. Once the tuner is showing `D`, use `Detune` for the last small adjustment if the reading still wobbles sharp or flat.
   - `Detune` is **not** inside `Tuner`
   - click the `Simpler` device on the `Kick Body` track
   - look for the pitch controls inside `Simpler`
   - `Transpose` is the coarse pitch control in semitones
   - `Detune` is the fine pitch control in cents
8. Keep the click layer unpitched unless it obviously fights the body.

If Ableton `Tuner` is not available:
1. Load any tuner plugin after `Simpler`, or create a temporary sine-wave reference that plays `D1` or `D2`.
2. Trigger the kick body against that reference.
3. Move `Transpose` in whole semitone steps until the kick body feels consonant with the `D` reference.
4. Use `Detune` for the final small adjustment.
5. Delete or mute the temporary reference before continuing.

Exact first-pass method:
1. Solo `Kick Body`.
2. Loop one kick hit so `Tuner` has time to settle.
3. Read the note name on `Tuner`.
4. Change `Transpose` in whole-number steps until the note name becomes `D`.
5. Then move `Detune` in small steps until the reading sits closest to the center of `D`.
6. Confirm the body is still low enough:
   - ideal: `D1` or `D2`
   - acceptable: another low `D` with visible sub weight below `80 Hz`
   - reject: a high `D` that sounds like click or tom, not kick body
7. Turn solo off and check the kick again in context before moving on.

What `Detune` means here:
- `Detune` lives on `Simpler`, not on `Tuner`
- `Tuner` only tells you what note it hears
- `Simpler` is where you change the sample pitch
- if `Tuner` shows `D` but the needle leans sharp, move `Detune` down in `-5` cent steps
- if `Tuner` shows `D` but the needle leans flat, move `Detune` up in `+5` cent steps
- stop once the body portion of the kick sits close to the center of `D`
- do not chase every tiny tuner flicker during the click/transient; watch the lower body after the first attack

If you cannot see `Detune` in `Simpler`:
1. Click the `Simpler` device title bar so its controls are visible in the bottom device panel.
2. Look for a pitch section with `Transpose` and `Detune`.
3. If the pitch section is collapsed, expand the device view or make the bottom device panel taller.
4. If you still cannot find it, skip fine detuning for now as long as `Tuner` already reads `D`.
5. Do not stop the tutorial over `Detune`; getting the note name to `D` with `Transpose` is the important first pass.

### Why
The kick does not need to sing a melody, but it should reinforce the key center rather than fight it.

### Rule
- tune by ear and verification
- not by guesswork

If the tuner keeps jumping around:
- ignore the first split-second of the transient
- watch the body portion of the hit, not the noisy attack
- if the sample is too noisy to read clearly, pick a simpler kick body sample instead of forcing the tuner

### Screenshot Set
- `foundation-02a-kick-simpler-pitch`
- `foundation-02b-kick-tuning-check`

## Step 3: Set The Kick Tail
### Action
Shape the kick so the body tail lands inside `90–120 ms`.

Practical method:
1. In `Simpler`, leave the sample start alone first unless there is obvious silence before the transient.
2. Set `Simpler` playback so one MIDI note triggers one kick hit cleanly.
3. Understand what the `volume envelope` means before changing it:
   - it is the shape of the sample's loudness after the MIDI note triggers it
   - it does **not** choose the sample
   - it does **not** tune the sample
   - it only controls how quickly the sound starts, fades, holds, and stops
4. In `Simpler`, look for the envelope section. It may be labeled `Volume`, `Amp`, or show the letters `A D S R`.
5. The letters mean:
   - `A / Attack`: how long the sound takes to start
   - `D / Decay`: how quickly it falls after the hit
   - `S / Sustain`: how loud it stays if the MIDI note keeps holding
   - `R / Release`: how long it takes to fade after the MIDI note ends
6. If using `Simpler Classic`, enable the volume envelope.
7. Set volume envelope first pass:
   - attack: `0 ms`
   - decay: `110 ms`
   - sustain: `0%`
   - release: `20 ms`
8. If the audio file itself has a long ringing tail, use the visible sample end / fade handle first, not the amp release:
   - open the sample display in `Simpler`
   - drag the sample end or fade so the visible waveform body ends near `100 ms`
   - use the envelope release only for the final click-free fade after the sample end is correct
   - do this before relying on release time
9. Use the volume envelope to control how the MIDI note triggers the sample.
10. Do not rely on `Release` to fix a long sample file:
   - release controls what happens after note-off
   - the sample end / fade controls how much long tail exists in the audio
11. Replay the kick on loop after each tail move.
12. Stop when the body ends before the next kick at `1/4` timing but still has a low thump.

If you cannot find the volume envelope:
1. Click the `Simpler` device title bar so its full device panel is visible.
2. Make the bottom device panel taller if the controls are hidden.
3. Look for `Classic`, `One-Shot`, or `Slice` mode tabs.
4. Use `Classic` mode for this first pass if you need ADSR control.
5. If you still cannot find ADSR, skip envelope editing for now and use the sample end / fade handle to shorten the kick tail.

Do not over-shorten it into a papery click.

### Why
If the tail is too long:
- the bass chapter will need too much sidechain
- the groove will feel blurrier than intended

If the tail is too short:
- the kick loses floor weight

### Starting Spec
- body tuned to `D`
- tail target: `100 ms`
- acceptable first-pass tail window: `90–120 ms`
- Simpler volume envelope: A `0 ms`, D `110 ms`, S `0%`, R `20 ms`
- strong enough in solo to feel physical
- short enough that the bass can later breathe beside it

### Screenshot
- `foundation-03-kick-tail-shape`

## Step 4: Layer The Click And Balance The Kick
### Action
1. Put the click on a separate track or chain.
2. Add `EQ Eight` to `Kick Click`.
3. Turn on band `1`.
4. Set band `1` to high-pass.
5. Set high-pass frequency to `700 Hz`.
6. Set slope to `24 dB/oct`.
7. Add `Utility` after `EQ Eight`.
8. Set `Utility Gain` to `-8 dB` on the first pass.
9. Play `Kick Body` and `Kick Click` together.
10. If the click is louder than the body, lower `Utility Gain` to `-10 dB` or `-12 dB`.
11. Stop before the click becomes the identity of the kick.

### Why
The click is support.
The body is still the instrument.

### Rule
- if the kick sounds bright but not heavy, the click is too loud
- first correction is always lowering `Kick Click`, not boosting `Kick Body`

### Screenshot Set
- `foundation-04a-kick-click-eq`
- `foundation-04b-kick-layer-balance`

## Step 5: Program The Foundation Kick Pattern
### Action
Program the kick on every quarter note for a simple `4`-bar foundation loop:
- beats `1`, `2`, `3`, `4`

Use short MIDI notes:
- make every kick MIDI note exactly `1/16` long on the first pass
- let the sample tail do the real sustain

Keep the kick perfectly on-grid.

Exact first-pass clip entry in the piano roll:
1. Create one `4`-bar MIDI clip on `Kick Body`.
2. Set the piano-roll grid to `1/16`.
3. Place the kick notes at:
   - `1.1.1`
   - `1.2.1`
   - `1.3.1`
   - `1.4.1`
   - `2.1.1`
   - `2.2.1`
   - `2.3.1`
   - `2.4.1`
   - `3.1.1`
   - `3.2.1`
   - `3.3.1`
   - `3.4.1`
   - `4.1.1`
   - `4.2.1`
   - `4.3.1`
   - `4.4.1`
4. Make every MIDI note `1/16` long.
5. Duplicate that same MIDI clip or copy the same MIDI note positions onto `Kick Click`.

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
- leave modulation off on the first pass

What this sound is supposed to be:
- a quiet layer of filtered hiss / air
- not a melody
- not a chord
- not a pad
- not something you clearly hear as "a synth part"

In plain English:
- the `Noise` oscillator creates the hiss
- the MIDI note only opens the synth so the hiss can play
- the note `C3` does **not** mean the air layer should sound like the pitch `C`
- the high-pass filter removes low and mid junk so only the top-air layer remains

Route most of the sense of space from:
- `Return C: long filtered hall`

not from drowning the patch itself in wet reverb.

Exact first-pass setup:
1. On the `Air` track, insert `Serum 2`.
2. Initialize the patch.
3. Turn `Osc A` off.
4. Turn `Osc B` off.
5. If Serum 2 shows `Osc C`, turn `Osc C` off too.
6. In Serum 2's main oscillator panel, find the `Noise` section beside or below the oscillator sections.
7. Click the `Noise` section power button so the noise oscillator is on.
8. Choose a broad white-noise or bright-noise source:
   - if you see `White Noise`, use it
   - if not, use the brightest neutral noise source available
   - avoid tonal or percussive noise sources for this first pass
9. Set `Noise Level` to `35%`.
10. Route the noise through `Filter 1` if Serum does not do it automatically:
   - make sure the filter routing includes `N` / `Noise`
   - if there is a small `N` routing button near the filter, turn it on
11. Set `Filter 1` to a high-pass filter:
   - click the filter type dropdown that may currently say something like `MG Low 18`
   - do **not** leave it on `Low`, `Low Pass`, or `MG Low`
   - choose a high-pass type such as `High 12`, `High 24`, `HP 12`, or `HP 24`
12. Set filter first pass:
   - type: high-pass
   - cutoff: `7 kHz`
   - resonance: `0–5%`
   - drive: `0%`
13. If the Serum filter menu is confusing, use this fallback:
   - leave Serum noise on
   - put Ableton `EQ Eight` after Serum on the `Air` track
   - turn on band `1`
   - set band `1` to high-pass
   - set frequency to `7 kHz`
   - set slope to `24 dB/oct`
14. Create one `4`-bar MIDI clip on the `Air` track.
15. In that clip, place one long note starting at `1.1.1`.
16. Use a middle-register trigger note such as `C3`.
17. Drag that note all the way to `4.4.4` so the noise source stays open across the whole clip.
18. In Clip View, turn `Loop` on.
19. Set loop start to `1.1.1`.
20. Set loop end to `5.1.1`.
21. Set the `Air` track fader to `-28 dB`.
22. Set `Air` `Send C` to `-18 dB`.
23. On the very first pass, do not add LFO movement yet. Get the ceiling working as a static layer before adding motion.

What `Send C` means:
- sends are the small knobs in the `Sends` area of each track
- each send knob sends a copy of that track to one return effect
- `Send C` means the knob labeled `C`
- in this tutorial, `C` should feed `Return C long hall`
- turning up `Send C` on `Air` sends some of the air layer into the long hall return

Ableton Live 11 exact send move:
1. In Session View, find the `Air` track.
2. Find the `Sends` section on that track.
3. Look for the knob labeled `C`.
4. If you cannot see send knobs, press `Cmd+Option+S` on Mac or `Ctrl+Alt+S` on Windows.
5. Click the `C` send knob and drag up until the value reads `-18 dB`.
6. If dragging is too sensitive, click the send value box if Ableton exposes it, type `-18`, and press `Enter`.
7. Leave sends `A`, `B`, and `D` at `-inf` on the `Air` track for this first pass.

Screenshot self-check:
- `Osc A`: off
- `Osc B`: off
- `Osc C`: off if present
- `Noise`: on
- `Filter 1`: high-pass, not low-pass
- filter cutoff: `7 kHz`
- `Air` fader: `-28 dB`

Arrangement note:
- this `4`-bar air loop is enough for the checkpoint
- in `Part 6`, extend or duplicate it so the `Air` track plays continuously from bar `1.1.1` through bar `145.1.1`

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
- noise level: `35%`
- high-pass cutoff: `7 kHz`
- track fader: `-28 dB`
- `Send C`: `-18 dB`
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

Starting level move:
1. Start with the `Air` track fader at `-28 dB`.
2. Play the kick and air together.
3. Mute and unmute `Air`.
4. If muting `Air` changes nothing, raise the fader to `-26 dB`.
5. If unmuting `Air` sounds like hiss arriving, lower the fader to `-30 dB`.
6. Keep `Send C` at `-18 dB` for the first pass.
7. Do not raise the air above `-24 dB` in this chapter.

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

Exact export range:
1. In Arrangement View, place the kick clip at bar `1.1.1`.
2. Place the air clip at bar `1.1.1`.
3. Set the loop brace / export range start to `1.1.1`.
4. Set the loop brace / export range end to `5.1.1`.
5. Export a `24-bit WAV`.
6. Name it `checkpoint-01-kick-air.wav`.
7. Put it in `Exports / Checkpoints`.

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
1. lower `Kick Click` by `-2 dB`
2. shorten the body decay from `110 ms` to `95 ms`
3. re-check `Tuner` and make sure the body reads `D`

### Problem: “The kick feels clicky, not weighty.”
Fix order:
1. lower `Kick Click` Utility from `-8 dB` to `-12 dB`
2. solo `Kick Body` and check that it still has a low thump with the click muted
3. choose a better body sample before over-processing

### Problem: “The air sounds like hiss.”
Fix order:
1. lower `Air` fader from `-28 dB` to `-30 dB`
2. raise the air high-pass cutoff from `7 kHz` to `8 kHz`
3. lower `Noise Level` from `35%` to `25%`
4. keep `Send C` at `-18 dB`

### Problem: “The air sounds like a pad.”
Fix order:
1. remove tonal oscillators
2. turn off any LFO or pitch movement
3. raise high-pass cutoff to `8 kHz`
4. lower `Send C` from `-18 dB` to `-22 dB`

## What Must Be Captured For Later Lesson Conversion
- kick body sample screenshot
- kick tuning screenshot
- kick tail / layering screenshot
- air patch screenshot
- kick + air checkpoint bounce
