# UKG 140 OG Bounce Driver: Tutorial Part 3 — Bass Floor

## Purpose
Teach the learner how to build the bass floor for `ukg-140-og-bounce-driver` in a way that is:
- modern rolling UKG
- rhythmic-primary
- dark but controlled
- supportive of the hook and harmony instead of replacing them

This part is the first full-depth template for the handheld tutorial format.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)

## Outcome
By the end of this part, the learner should have:
- one `Serum 2` sub patch
- one `Serum 2` mid-bass patch
- one `Bass` group in Ableton
- working sidechain from kick to sub and mid-bass
- one `4`-bar bass phrase that follows:
  - `D2 -> Bb1 -> F2 -> C2`
- phrase-end release-note vocabulary that does not imply new chords
- one audio bounce of `drums + bass`

## Time Estimate
- `60–90 minutes`

## Prerequisites
- learner can create a MIDI track in Ableton
- learner can insert and initialize `Serum 2`
- learner can route sidechain in Ableton compressor
- learner understands note length, velocity, and bar/beat positions in MIDI

## What The Learner Should Understand Before Starting
The bass in this track is the `floor`, not the lead.

That means:
- the sub should feel stable and confident
- the character should come from the harmonic layer
- the groove should come from rhythm and gate shape first
- the tone motion should support the groove, not become a melody

If the bass starts feeling like the hook, the learner has gone too far.

Timing reminder for this part:
- positions like `1.4.3` and `3.2.4` are local positions inside the `4`-bar bass clip
- if this chapter mentions a full-song section such as `33–48`, that is Arrangement View timing, not clip timing

## Reference Axis
Primary A/B for this part:
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - listen for rhythmic roll, not just tone
- `Interplanetary Criminal - Slow Burner`
  - listen for how the bass and kick breathe together

Secondary check:
- `KETTAMA - It Gets Better`
  - listen for weight and size, not note content

## Files / Assets Needed
- current project with `Kick`, `Clap`, and basic top groove already present
- one empty MIDI track named `Bass Sub`
- one empty MIDI track named `Bass Mid`
- one group track named `Bass`

## Step 1: Create The Bass Group
### Action
1. Create two MIDI tracks.
2. Rename them:
   - click the first track header and press `Cmd+R` / `Ctrl+R`, then type `Bass Sub`
   - click the second track header and press `Cmd+R` / `Ctrl+R`, then type `Bass Mid`
3. Group them into a folder named `Bass`.
4. Route both tracks to the `Bass` group.
5. Color the `Bass` group differently from drums so bass edits are visually obvious.

### Why
The sub and the character layer must be separable.

If they live on one track:
- sidechain is harder to tune
- EQ crossover is harder to control
- troubleshooting becomes slower

### Screenshot
- `bass-group-routing-overview`

## Step 2: Build The Sub Patch In Serum 2
### Action
1. Load a fresh instance of `Serum 2` on `Bass Sub`.
2. Initialize the patch.
3. Turn `Osc A` off.
4. Turn `Osc B` off.
5. Turn the `Sub` oscillator on.
6. Set the sub waveform to `Sine`.
7. Set `Sub Level` to `100%` while designing.
8. In the `Sub` oscillator section, set `Direct Out` to `On` so the sub bypasses unnecessary in-patch coloration.
9. Set `Voices` / unison to `1`.
10. Set `Mono` to `On`.
11. Set portamento / glide to `8 ms` on the first pass.
12. Set amp envelope:
    - attack: `0 ms`
    - decay: `0`
    - sustain: `100%`
    - release: `45 ms`
13. Open the modulation matrix and confirm there is no `Velocity -> Level` routing on the sub.
14. If there is one, right-click the routing amount and delete that modulation before continuing.

### Why
This keeps the sub:
- stable
- centered
- consistent from note to note

The sub should not provide excitement. It should provide authority.

### Final Sub Patch Spec
- engine: `Serum 2`
- oscillator: `Sub only`
- waveform: `Sine`
- main oscillators: `Off`
- unison: `1`
- mono: `On`
- glide: `8 ms` starting point
- amp env:
  - A `0`
  - D `0`
  - S `100%`
  - R `45 ms`

### Screenshot Set
- `sub-01-init`
- `sub-02-sub-osc-only`
- `sub-03-env-and-mono`

## Step 3: Build The Mid-Bass Patch In Serum 2
### Action
1. Load a fresh instance of `Serum 2` on `Bass Mid`.
2. Initialize the patch.
3. Set `Osc A` to `Basic Shapes`.
4. Choose a square wave for `Osc A`:
   - open the `Basic Shapes` wavetable view
   - move the wavetable position until the displayed shape looks like a blocky square wave
   - a square wave looks mostly flat on top, drops straight down, stays flat on the bottom, then jumps back up
   - if Serum shows named shapes, choose `Square`
   - if you cannot find a perfect square, choose the most blocky shape available
5. Set `Osc A Level` to `75%`.
6. Set `Osc B` to `Basic Shapes`.
7. Choose a saw wave for `Osc B`:
   - move the wavetable position until the displayed shape looks like a ramp or diagonal slope
   - a saw wave usually rises or falls in a straight diagonal line, then jumps back to the start
   - if Serum shows named shapes, choose `Saw`
   - if you cannot find a perfect saw, choose the closest ramp-shaped option
8. Set `Osc B Level` to `30%`.
9. Leave both at the same octave to start.
10. Set unison conservatively:
    - `Osc A`: `1 voice`
    - `Osc B`: `2 voices`
11. Set `Osc B Detune` to a tiny fixed amount:
    - set it to `0.05` on Serum's `0.00–1.00` detune scale on the first pass
12. Route both through a low-pass filter:
    - type: `MG Low 12`
13. Set initial filter settings:
    - cutoff: `160 Hz`
    - resonance: `12%`
    - drive: `15%`
14. Set amp envelope:
    - attack: `0–3 ms`
    - decay: `~250 ms`
    - sustain: `70–80%`
    - release: `50–70 ms`

### Why
This layer needs:
- body
- upper harmonic information
- mild stereo-safe richness
- room to move

It does **not** need:
- supersaw width
- big detune
- enough harmonic complexity to become the hook

### Final Mid-Bass Starting Spec
- engine: `Serum 2`
- Osc A: `Basic Shapes`, square wave or closest blocky square shape
- Osc B: `Basic Shapes`, saw wave or closest ramp-shaped saw shape
- A/B balance: `Osc A 75%` / `Osc B 30%`
- detune: `0.05` on Serum's `0.00–1.00` scale, on Osc B only
- filter: `MG Low 12`
- cutoff: `160 Hz` initial
- resonance: `12%`
- drive: `15%`
- amp env:
  - A `0–3 ms`
  - D `250 ms`
  - S `75%`
  - R `60 ms`

### Screenshot Set
- `mid-01-oscillators`
- `mid-02-filter`
- `mid-03-amp-envelope`

## Step 4: Add Rhythmic-Primary Motion
### Action
1. Create `LFO 1` as a slow, smooth breathing shape.
2. Set the rate so it breathes over phrase motion, not per note:
   - set it to `1 bar` synced on the first pass
3. Drag `LFO 1` onto the filter cutoff.
4. Set the modulation amount by dragging the modulation ring to `15%`.
5. If the bass still sounds completely static in context, raise the depth to `18%`.
6. If it starts sounding like wobble bass, lower the depth to `10%`.
7. Do not add a second modulation target until the `15%` cutoff movement works against the drums.

### Why
The mid layer is `tonal-secondary`.

That means:
- modulation supports the phrase
- modulation does not define the phrase

If the learner hears “wobble,” the movement is too deep.

### Starting Motion Spec
- `LFO 1`
  - shape: gentle rise/fall
  - sync: on
  - rate: `1 bar`
  - destination: filter cutoff
  - depth: `15%`

### Screenshot Set
- `mid-04-lfo-shape`
- `mid-05-lfo-routing`

## Step 5: Add In-Patch Character FX
### Action
1. Add light distortion in Serum 2 FX:
   - set drive to `8%` on the first pass
2. Add EQ after distortion:
   - set one bell cut at `220 Hz`, `-1.5 dB`, `Q 1.0`
   - leave true sub to the sub track
3. Avoid reverb, delay, chorus, or wide imaging on the mid-bass patch itself at this stage.

### Why
The bass needs attitude, but the width and space belong elsewhere in the mix.

### Starting FX Spec
- distortion:
  - drive `8%` first pass
  - do not raise above `15%` before checking against drums
- EQ:
  - `220 Hz`
  - `-1.5 dB`
  - `Q 1.0`
  - do not master the tone inside the patch

### Screenshot Set
- `mid-06-distortion`
- `mid-07-eq`

## Step 6: Program The Root Path
### Action
Create a `4`-bar MIDI clip on both bass tracks with these roots:
- Bar 1: `D2` under `Dm9`
- Bar 2: `Bb1` under `Bb`
- Bar 3: `F2` under `Fadd9`
- Bar 4: `C2` under `Cadd9`

Starting placement:
- put each root on beat `1`
- use the exact note lengths in the first-pass MIDI entry below
- this should feel like the `50–70%` gate target once the loop is playing at speed

Exact first-pass MIDI entry in the `4`-bar clip:
1. Open the bass clip on both `Bass Sub` and `Bass Mid`.
2. Set the piano-roll grid to `1/16`.
3. Place `D2` at `1.1.1` and drag it to `1.3.3`.
4. Place `Bb1` at `2.1.1` and drag it to `2.3.2`.
5. Place `F2` at `3.1.1` and drag it to `3.3.3`.
6. Place `C2` at `4.1.1` and drag it to `4.3.2`.
7. Copy the same note positions onto both bass tracks first. Do not change sound design until both lanes play the same MIDI correctly.

### Gate Strategy
Start with these body-note lengths:
- `D2`: `1.1.1` to `1.3.3`
- `Bb1`: `2.1.1` to `2.3.2`
- `F2`: `3.1.1` to `3.3.3`
- `C2`: `4.1.1` to `4.3.2`

Do **not** make every note the same length.

### Why
This is the first source of rolling motion:
- not extra notes
- not extra modulation
- note-length life

### Screenshot
- `bass-midi-01-root-path`

### Visual MIDI Requirement
- show all `4` bars in one screenshot
- label the chord above each bar in the tutorial annotation

## Step 7: Add Phrase-End Release Notes
### Action
Add short release gestures only at phrase ends or controlled turn points.

Allowed vocabulary:
- over `Dm9`: `D2`, `D3`, `A2`, `C3`
- over `Bb`: `Bb1`, `Bb2`, `F2`, `D2`
- over `Fadd9`: `F2`, `F3`, `C3`, `G3`
- over `Cadd9`: `C2`, `C3`, `G2`, `D3`

Release-note gate feel:
- use `1/16` length on the first pass
- that gives a short pickup gesture without becoming a new sustained bass event

Starting placement:
- first try the release note in the last `1/8` or `1/16` of the bar
- treat it like a pickup into the next bar, not a new sustained event
- do not add one to every bar automatically
- this step is meant to fill the end-of-bar gap left by Step `6`

Exact first-pass release-note example:
1. In bar `1`, place `A2` at `1.4.3` with `1/16` length.
2. In bar `2`, place `F2` at `2.4.3` with `1/16` length.
3. In bar `3`, place `G3` at `3.4.4` with `1/16` length.
4. In bar `4`, place `D3` at `4.4.3` with `1/16` length.
5. Play the loop and remove any release note that suddenly makes the next bar feel like a different chord family.

### Rule
If a release note makes the chord feel like it changed, delete it.

### Why
The release notes are punctuation, not reharmonization.

### Screenshot
- `bass-midi-02-release-vocabulary`

## Step 8: Program Internal Pulse Without Extra Melody
### Action
1. Inside the 4-bar phrase, add small note-length differences.
2. Split only the exact notes listed in the first-pass example below before inventing any other internal pulse.
3. Do **not** add a bunch of new pitches to create movement.

Starting rhythm rule:
- first try pulse by changing note lengths before adding extra note-ons
- if you do add a second note-on inside a bar, keep it the same pitch before trying a new pitch
- let phrase-end release notes be the first place a different pitch appears
- keep this internal pulse earlier in the bar than the Step `7` release note so they do not collide at the bar end

Exact first-pass internal-pulse example:
1. Leave bars `2` and `4` as single sustaining roots on the first pass.
2. In bar `1`, split the `D2` note into:
   - `D2` from `1.1.1` to `1.2.4`
   - `D2` again from `1.3.1` to `1.3.3`
3. In bar `3`, split the `F2` note into:
   - `F2` from `3.1.1` to `3.2.4`
   - `F2` again from `3.3.1` to `3.3.3`
4. Leave the release notes at the end of the bar where they are.
5. If the phrase already rolls correctly at this point, do not add more pulse notes just because the lane looks sparse.

### Why
This is the main style-defining choice:
- `rhythmic-primary`
- `tonal-secondary`

### Diagnostic
Ask:
- if I muted filter movement, would the bass still roll?

If the answer is no, the rhythm is not doing enough work.

### Screenshot
- `bass-midi-03-gate-variation`

### Visual MIDI Requirement
- show the full `4`-bar phrase after internal pulse is added
- the tutorial should show the progression:
  - roots only
  - roots + release notes
  - roots + release notes + internal pulse

## Step 9: Create The Bass Bus Chain
### Action
On the `Bass` group, build this starting chain:
1. `EQ Eight`
2. `Saturator`
3. `Compressor` or sidechain stage for glue
4. `Utility`

### Starting Settings
#### EQ Eight
- low cut only if a layer is spilling into the wrong range
- use this mainly to separate sub and mid layers, not as a tone crutch

#### Saturator
- set drive to `8%` on the first pass
- if the bass still feels too clean after balancing, raise drive to `12%`
- do not go above `15%` during this part
- stop before saturation blurs the phrase

#### Utility
- keep the bass group centered
- mono-safe low end

### Why
The bass bus should:
- glue the two layers
- add attitude
- preserve center stability

### Screenshot Set
- `bass-bus-01-overview`
- `bass-bus-02-saturator`

## Step 10: Add Sidechain
### Action
Put a sidechain compressor on:
- `Bass Sub`
- `Bass Mid`

Use the kick as the sidechain source.

### Starting Sidechain Settings
#### Sub
- ratio: `4:1` to `6:1`
- attack: fast
- release: `90–120 ms`
- aim: clear duck, but not a disappearing sub

#### Mid
- ratio: `2:1` to `4:1`
- attack: fast
- release: start at `95 ms`, slightly shorter than the `Sub` first-pass release
- aim: breathing motion, not heavy pumping

### Why
The kick and bass should breathe together.

The ducking should feel like part of the groove, not punishment.

### Screenshot Set
- `sidechain-01-sub`
- `sidechain-02-mid`

## Step 11: Balance The Layers
### Action
1. Bring up the `Bass Sub` until the floor feels stable.
2. Bring up the `Bass Mid` until the phrase becomes readable.
3. Stop before the mid layer sounds like the hook.

### Practical Listening Rule
- if the sub is muted and the phrase still works, the mid layer has enough definition
- if the mid layer is muted and the groove collapses, the sub was never enough on its own

You need both.

## Step 12: A/B Against References
### Action
Bounce or loop `drums + bass`.

Compare against:
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - listen for roll character
- `Interplanetary Criminal - Slow Burner`
  - listen for kick-bass breathing
- `KETTAMA - It Gets Better`
  - listen for physical weight

### What To Listen For
- how often the bass pitch actually changes across the phrase
- does the bass roll because of rhythm, not just filter motion?
- does the kick still land with authority?
- is the low end big without becoming slow?
- does the phrase feel club-functional, not decorative?

Expected answer:
- the main root pitch changes `4` times across the `4`-bar loop
- across a `16`-bar drop span, expect `16` main root events if the loop repeats four times
- extra pitch movement should come mainly from phrase-end release notes, not constant interior rewrites
- a healthy first pass should add `4–8` extra release-note pitch events across those `16` bars, not dozens of interior rewrites

## Troubleshooting
### Problem: “The bass feels static.”
Fix order:
1. vary gate lengths
2. add or refine internal pulse
3. only then deepen small filter movement

### Problem: “The bass feels too melodic.”
Fix order:
1. delete extra notes
2. keep only phrase-end punctuation
3. reduce modulation depth

### Problem: “The kick disappears when the bass comes in.”
Fix order:
1. shorten the kick tail
2. reduce low content in the mid-bass layer
3. increase sidechain slightly

### Problem: “The bass sounds wide and weak.”
Fix order:
1. center the bass group harder
2. reduce stereo behavior in the mid layer
3. make sure the sub is truly mono

### Problem: “The bass feels like the hook.”
Fix order:
1. reduce phrase-end note count
2. reduce upper harmonic brightness
3. simplify the gate pattern

### Problem: “I followed the spec and it still sounds wrong.”
Fix order:
1. check kick and bass together in mono
2. loudness-match the reference before judging tone
3. solo the mid-bass without the sub and make sure Steps `6–8` are actually producing rhythmic life
4. reduce LFO-to-filter depth from `15%` to `10%` before changing the MIDI again

## Checkpoint Deliverables
At the end of Part 3, save:
- `Bass Sub` Serum 2 preset
- `Bass Mid` Serum 2 preset
- `Bass` MIDI clip
- `drums + bass` bounce

## Capture Checklist
Capture these artifacts while building:
- screenshots:
  - `sub-01-init`
  - `sub-02-sub-osc-only`
  - `sub-03-env-and-mono`
  - `mid-01-oscillators`
  - `mid-02-filter`
  - `mid-03-amp-envelope`
  - `mid-04-lfo-shape`
  - `mid-05-lfo-routing`
  - `mid-06-distortion`
  - `mid-07-eq`
  - `bass-midi-01-root-path`
  - `bass-midi-02-release-vocabulary`
  - `bass-midi-03-gate-variation`
  - `bass-bus-01-overview`
  - `bass-bus-02-saturator`
  - `sidechain-01-sub`
  - `sidechain-02-mid`
- audio:
  - `checkpoint-bass-floor.wav`
- notes:
  - what changed during A/B
  - which reference caused the main adjustment
  - which tempting wrong turn got removed

## Lesson Conversion Notes
When this becomes the guided lesson:
- split it into:
  - patch build
  - MIDI phrase
  - bus chain
  - A/B checkpoint
- keep the troubleshooting visible
- surface the core doctrine repeatedly:
  - `the bass is the floor, not the hook`
