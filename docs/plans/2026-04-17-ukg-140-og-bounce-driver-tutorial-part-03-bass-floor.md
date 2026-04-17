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

## Reference Axis
Primary A/B for this part:
- `Y U QT - NRG`
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
2. Name them `Bass Sub` and `Bass Mid`.
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
8. Set `Direct Out` to `On` so the sub bypasses unnecessary in-patch coloration.
9. Set `Voices` / unison to `1`.
10. Set `Mono` to `On`.
11. Set portamento / glide to a very small value:
    - start around `8 ms`
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
- glide: `~8 ms` starting point
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
4. Choose the `square-leaning` shape.
5. Set `Osc A Level` around `75%`.
6. Set `Osc B` to `Basic Shapes`.
7. Choose the `saw-leaning` shape.
8. Set `Osc B Level` around `30%`.
9. Leave both at the same octave to start.
10. Set unison conservatively:
    - `Osc A`: `1 voice`
    - `Osc B`: `2 voices`
11. Set `Osc B Detune` lightly:
    - start around `0.05`
12. Route both through a low-pass filter:
    - type: `MG Low 12`
13. Set initial filter settings:
    - cutoff: start around `160 Hz`
    - resonance: low, around `10–15%`
    - drive: light, around `10–20%`
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
- Osc A: `Basic Shapes`, square-leaning
- Osc B: `Basic Shapes`, saw-leaning
- A/B balance: roughly `70/30`
- detune: `~0.05` on Osc B only
- filter: `MG Low 12`
- cutoff: `~160 Hz` initial
- resonance: `~12%`
- drive: `~15%`
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
   - start around `1/2 bar` or `1 bar` synced
3. Drag `LFO 1` onto the filter cutoff.
4. Set the modulation amount by dragging the modulation ring to a small value.
4. Keep the modulation small:
   - enough to feel movement
   - not enough to sound like wobble bass
5. If needed, add a second tiny modulation to distortion drive or oscillator mix, but only after the cutoff movement works.

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
  - rate: `1/2 bar` to `1 bar`
  - destination: filter cutoff
  - depth: start around `10–20%`

### Screenshot Set
- `mid-04-lfo-shape`
- `mid-05-lfo-routing`

## Step 5: Add In-Patch Character FX
### Action
1. Add light distortion in Serum 2 FX:
   - keep it subtle
2. Add EQ if needed:
   - trim extra low-mid buildup
   - leave true sub to the sub track
3. Avoid reverb, delay, chorus, or wide imaging on the mid-bass patch itself at this stage.

### Why
The bass needs attitude, but the width and space belong elsewhere in the mix.

### Starting FX Spec
- distortion:
  - subtle
  - enough to help note identity
- EQ:
  - cleanup only
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
- let each root sustain for roughly `2` beats to just under `3` beats at first
- this should feel like the `50–70%` gate target once the loop is playing at speed

### Gate Strategy
Start with body notes in roughly this range:
- `50–70%` gate feel for the main sustaining notes

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
- roughly `15–35%`

Starting placement:
- first try the release note in the last `1/8` or `1/16` of the bar
- treat it like a pickup into the next bar, not a new sustained event
- do not add one to every bar automatically
- this step is meant to fill the end-of-bar gap left by Step `6`

### Rule
If a release note makes the chord feel like it changed, delete it.

### Why
The release notes are punctuation, not reharmonization.

### Screenshot
- `bass-midi-02-release-vocabulary`

## Step 8: Program Internal Pulse Without Extra Melody
### Action
1. Inside the 4-bar phrase, add small note-length differences.
2. If needed, split one sustaining note into two tied-feel notes around beat `2.5` or beat `3` so the phrase breathes before the phrase-end release note.
3. Do **not** add a bunch of new pitches to create movement.

Starting rhythm rule:
- first try pulse by changing note lengths before adding extra note-ons
- if you do add a second note-on inside a bar, keep it the same pitch before trying a new pitch
- let phrase-end release notes be the first place a different pitch appears
- keep this internal pulse earlier in the bar than the Step `7` release note so they do not collide at the bar end

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
3. `Compressor` or sidechain stage for glue if needed
4. `Utility`

### Starting Settings
#### EQ Eight
- low cut only if a layer is spilling into the wrong range
- use this mainly to separate sub and mid layers, not as a tone crutch

#### Saturator
- drive lightly
- enough to make the bass feel more solid in context
- not enough to blur the phrase

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
- release: similar or slightly shorter than sub
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
- `Y U QT - NRG`
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
- a healthy first pass usually adds roughly `4–8` extra release-note pitch events across those `16` bars, not dozens of interior rewrites

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
4. if needed, reduce modulation depth before changing the MIDI again

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
