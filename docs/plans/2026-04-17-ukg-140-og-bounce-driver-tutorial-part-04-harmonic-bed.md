# UKG 140 OG Bounce Driver: Tutorial Part 4 — Harmonic Bed

## Purpose
Teach the learner how to build the harmonic bed for `ukg-140-og-bounce-driver` so it:
- feels emotional without spending the bloom too early
- supports the bass floor instead of clouding it
- opens upward in the break and `Drop B`
- stays readable in a club mix

This part should turn the harmony plan into exact patch, MIDI, width, and automation choices.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)

## Outcome
By the end of this part, the learner should have:
- one `Serum 2` chord-bed patch
- one `Chords` MIDI track and one `Chords` group
- a `4`-bar restrained drop chord loop
- one `8`-bar break / bloom chord clip
- clear restrained and bloomed `Bb` voicing states
- chord-bus EQ and sidechain routing
- width and reverb-send automation for:
  - `Drop A`
  - `Break`
  - `Re-entry Build`
  - `Drop B`
- one bounce of `drums + bass + chords`

## Time Estimate
- `45–75 minutes`

## Prerequisites
- learner has completed or can reference:
  - `Part 0` setup
  - `Part 2` groove
  - `Part 3` bass floor
- learner can enter multi-note MIDI chords in Ableton
- learner can automate device parameters and return sends

## What The Learner Should Understand Before Starting
The harmony in this track is not trying to impress by being “complicated.”

It is trying to do three jobs:
- hold the emotional center
- delay the hopeful bloom until it matters
- widen upward later without smearing the low-mid

If the chords sound huge too early, the arrangement loses its staircase.

Timing reminder for this part:
- positions like `1.1.1`, `2.4.4`, and `8.1.1` are local positions inside the chord clips
- if a step explicitly says `Arrangement View` and uses bars such as `33.1.1` or `65.1.1`, those are full-song positions

Plain-English routing reminder:
- a `bus` is just a group channel that several tracks feed into so one EQ, compressor, or volume move can affect them together
- a `Music bus` or `Chords bus` means: route the `Chords` track into that group before it reaches the master output
- a `return` is an effect track, usually reverb or delay, that receives a copy of the sound from a send knob
- a `send` is the knob on the track that decides how much copy goes to that return effect
- `width` controls how far left/right the sound feels; it should widen the chords without moving the low end out of the center

## Reference Axis
Primary A/B for this part:
- `Sammy Virji - I Guess We're Not the Same`
  - listen for harmonic readability and hook/chord coexistence
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - listen for how harmonic support stays present without swallowing the groove

Secondary check:
- `KETTAMA - It Gets Better`
  - listen for how density can stay physical even when the harmonic layer is not oversized

## Files / Assets Needed
- current project with:
  - `Drums` group
  - `Bass` group
- one empty MIDI track named `Chords`
- one group track named `Music` or `Chords` if not already created
- access to the Production Plan sections:
  - `Harmony Spec`
  - `Chord-bed patch`
  - `Chord duality mechanism`
  - `Top-End, Air, and Stereo`

## Voicing Palette
Use this as the source of truth:
- `Dm9`: `D3 F3 A3 C4 E4`
- restrained `Bb`: `Bb2 F3 C4`
- bloomed `Bbmaj7`: `Bb2 F3 A3 C4`
- `Fadd9`: `F2 C3 G3 A3`
- `Cadd9`: `C3 G3 D4 E4`

## Step 1: Create The Chord Lane
### Action
1. Create one MIDI track named `Chords`.
2. Click the track header once.
3. Press `Cmd+R` on Mac or `Ctrl+R` on Windows.
4. Type `Chords` and press `Enter`.
5. Right-click the `Chords` track header and choose a color swatch that is clearly different from:
   - `Bass`
   - `Hook`
   - `Answer`
6. Route the `Chords` track to the `Music` or `Chords` group.
7. In Session View, create:
   - one empty `4`-bar MIDI clip for the restrained drop loop
   - one empty `8`-bar MIDI clip for the break / bloom state
8. If you are in Arrangement View instead:
   - create one blank `4`-bar MIDI clip from bar `33.1.1` to `37.1.1`
   - create one blank `8`-bar MIDI clip from bar `65.1.1` to `73.1.1`

### Why
The chord bed is one identity lane, not three unrelated layers at this stage.

Keeping it on one main track first makes:
- the restrained/bloomed contrast easier to hear
- sidechain easier to tune
- troubleshooting easier later

### Screenshot
- `chords-01-lane-setup`

## Step 2: Build The Chord-Bed Patch In Serum 2
### Action
1. Load a fresh instance of `Serum 2` on `Chords`.
2. Initialize the patch.
3. Before choosing a sound, enter one test chord in the MIDI clip:
   - place `D3`, `F3`, `A3`, `C4`, and `E4`
   - all five notes start at `1.1.1`
   - all five notes end at `1.4.4`
4. Loop that bar while you build the sound.
5. In Serum 2's voicing area, confirm the patch can play chords:
   - `Mono`: off
   - `Legato`: off
   - `Poly`: at least `8`
   - if only one note sounds when five MIDI notes are present, stop and fix this before changing the oscillator tone
   - this was the real cause of the earlier “dull beep” failure mode: a mono patch cannot play a chord bed
6. In Serum 2, turn these sources off:
   - `Sub`: off
   - `Osc C`: off
   - `Noise`: off
7. In Serum 2, turn these FX modules off for now:
   - `Reverb`: off
   - `Delay`: off
   - `Compressor`: off
   - `Distortion`: off
   - `EQ`: off
8. Set `Osc A` to `Basic Shapes`.
9. Choose a warm saw-based frame:
   - do not choose the pure sine shape
   - do not choose the pure square shape
   - choose a saw or triangle-saw blend with enough harmonics to sound like a chord, not a single beep
10. Set `Osc A`:
   - octave: `0`
   - level: about `70%`
   - unison / voices: `3`
   - detune: `0.03–0.04` on Serum's `0.00–1.00` detune scale
   - blend: middle / default first-pass
11. Set `Osc B` to `Basic Shapes`.
12. Choose a softer support shape:
   - triangle or rounded triangle first
   - avoid a bright saw here on the first pass
13. Set `Osc B`:
   - octave: `0`
   - level: `15–20%`
   - unison / voices: `1`
   - detune: `0.00`
14. Route `Osc A` and `Osc B` into `Filter 1`.
15. Set `Filter 1`:
   - type: `MG Low 12` first-pass
   - cutoff: `1.8–2.2 kHz`
   - resonance: `5–8%`
   - drive: `0–3%`
16. Set `ENV 1`, the amp envelope:
   - attack: `30–45 ms`
   - hold: `0.0 ms`
   - decay: `1.0–1.3 s`
   - sustain: around `-5 to -7 dB` if Serum shows dB, or around `60–70%` if it shows percent
   - release: `400–550 ms`
17. Play the test chord.
18. Do not continue until the test chord passes the sound check below.

Sound check before moving on:
- it should sound like several notes forming one warm chord
- it should have a soft front edge, not a click
- it should not sound like one high beep
- it should not sound like a huge trance pad
- it should not need reverb to feel acceptable

Reference description:
- closest mental model: a soft garage organ/pad hybrid sitting behind the drums
- not a piano
- not a lead
- not a pluck
- not a cinematic pad
- it should feel like a warm block of harmony that the bass and hook can sit in front of

If it still sounds like a dull beep:
- confirm all five test-chord notes are present
- confirm `Mono` is off and `Poly` is at least `8`
- watch Serum's mini keyboard or Ableton's MIDI note display; five notes should trigger together
- confirm the `Dm9` notes are `D3 F3 A3 C4 E4`, not the old `D3 A3 C4 E4 F4`
- lower `Osc B` level to `0%` temporarily and listen to `Osc A` alone
- open cutoff slightly toward `2.4 kHz` if the sound is too dull
- lower cutoff toward `1.6 kHz` if the sound is too piercing
- increase `Osc A` unison to `4` only if it sounds too narrow
- do not add reverb yet

### Why
This patch needs to behave like:
- a warm sustained chord layer first
- a pulse-capable layer second

It should not sound like:
- a huge trance supersaw
- a dry organ stab
- a long washy pad with no front edge
- a hospital monitor beep

Plain-English sound target:
- when you hold one chord, it should sound like warm harmonic support underneath the track
- it should not sound like a single thin note
- it should not sound like a lead synth
- it should not poke out harder than the kick or hook
- if you mute it, the track should feel less warm; if you unmute it, the track should feel wider and more musical without becoming busier

If it sounds like a high beep:
- the patch is too narrow, too high, too clean, or too percussive
- do not keep building on that sound
- fix the patch before programming the full chord progression

### Final Chord-Bed Starting Spec
- engine: `Serum 2`
- Osc A: `Basic Shapes`, warm saw or triangle-saw blend
- Osc A Level: `70%`
- Osc A Unison: `3 voices`
- Osc A Detune: `0.03–0.04`
- Osc B: `Basic Shapes`, triangle / rounded triangle support
- Osc B Level: `15–20%`
- Osc B Unison: `1 voice`
- filter: smooth low-pass
- cutoff: `1.8–2.2 kHz`
- resonance: `5–8%`
- drive: `0–3%`
- amp env:
  - A `30–45 ms`
  - H `0.0 ms`
  - D `1.0–1.3 s`
  - S `-5 to -7 dB`, or `60–70%`
  - R `400–550 ms`

### Screenshot Set
- `chords-02-oscillators`
- `chords-03-filter-and-env`

## Step 3: Add Width And Glue Inside The Patch
### Action
Only do this after Step `2` passes the sound check.

1. In Serum's FX area, add one gentle width effect:
   - use `Chorus`, `Dimension`, or the closest stock width-style effect available in your Serum build
2. Set the width effect lightly:
   - mix: `8–12%`
   - rate: slow, around `0.10–0.20 Hz`
   - depth: `15–25%`
3. Do not add in-patch reverb.
4. Do not add delay.
5. Do not add compressor.
6. Do not add distortion yet.
7. Play the `Dm9` test chord again.
8. If the width effect makes the chord phasey, seasick, or fake-wide, lower mix to `5%` or bypass it.
9. If the chord still feels too plain after the MIDI and section automation are added later, use return reverb and width automation first. Do not fix it by loading a huge preset.

### Why
Most of the section-dependent space should come from:
- bus decisions
- return sends
- automation

If the patch is already huge before the mix, the break has nowhere to open.

### Starting FX Direction
- width effect: `Chorus` / `Dimension` / equivalent
- width mix: `8–12%`
- width rate: `0.10–0.20 Hz`
- width depth: `15–25%`
- saturation drive: off for the first pass
- compressor: off
- in-patch reverb: `off`

### Screenshot Set
- `chords-04-width`
- `chords-05-fx`

## Step 4: Program The Restrained Drop Loop
### Action
Create a `4`-bar MIDI clip for the drop state:
1. Open the `4`-bar drop clip so the piano roll is visible.
2. Set the MIDI grid to `1/16`.
3. In bar `1`, place these notes so they all start at `1.1.1` and all end at `1.4.4`:
   - `D3`
   - `F3`
   - `A3`
   - `C4`
   - `E4`
4. In bar `2`, place these notes so they all start at `2.1.1` and all end at `2.4.4`:
   - `Bb2`
   - `F3`
   - `C4`
5. In bar `3`, place these notes so they all start at `3.1.1` and all end at `3.4.4`:
   - `F2`
   - `C3`
   - `G3`
   - `A3`
6. In bar `4`, place these notes so they all start at `4.1.1` and all end at `4.4.4`:
   - `C3`
   - `G3`
   - `D4`
   - `E4`
7. Read the clip left to right and make sure there is exactly one chord per bar.
8. Leave the final `1/16` of each bar free by stopping each chord at `x.4.4` instead of dragging it all the way into the next bar.

### Why
This is the emotional floor of the song.

The `Dm9` voicing is intentionally `D3 F3 A3 C4 E4`.

Use this safer voicing for the first pass even if the old `D3 A3 C4 E4 F4` voicing sounded bad mainly because `Mono` was accidentally on.

The old `E4/F4` top cluster is not banned forever. It is an optional color audition after:
- the patch is confirmed polyphonic
- the safe voicing works
- the chords are playing in context with drums and bass

Do not use the old `D3 A3 C4 E4 F4` voicing as the default. Putting `E4` and `F4` next to each other at the top can still make this patch feel tense, whistly, or over-focused.

The crucial move is bar 2:
- restrained `Bb`
- no exposed `A`
- no early `Bbmaj7` bloom

### Rule
If the `Bb` bar already sounds openly hopeful in `Drop A`, it is too bloomed.

### Screenshot
- `chords-midi-01-restrained-drop-loop`

### Visual MIDI Requirement
- show all `4` bars in one screenshot
- label the restrained `Bb` state clearly

## Step 5: Apply Voice Leading Deliberately
### Action
1. Play the 4-bar loop slowly.
2. Identify the common tones first:
   - `Dm9` and restrained `Bb` can share `F` and `C`
3. If your `Dm9` has `C4` and your restrained `Bb` has `C5`, drag one of them so the common tone stays in the same register.
4. Keep upper voices moving by short steps where possible.
5. Avoid bouncing every top note around by large leaps.

### Why
The chords should feel written, not pasted.

Voice leading is what makes the loop:
- emotional
- readable
- expensive-feeling

without adding more notes.

### Practical Rule
- from `Dm9` into restrained `Bb`, let `C` remain if possible
- into `Fadd9` and `Cadd9`, move the upper voices stepwise before making bigger interval jumps

### Screenshot
- `chords-midi-02-voice-leading-pass`

## Step 6: Build The Break / Bloom State
### Action
Create an `8`-bar break clip or duplicate the loop and edit it into the bloom state:
1. Open the `8`-bar break clip.
2. Set the MIDI grid to `1/16`.
3. Enter the same chord progression, but give each harmony two bars instead of one:
   - bars `1–2`: `Dm9`
   - bars `3–4`: bloomed `Bbmaj7`
   - bars `5–6`: `Fadd9`
   - bars `7–8`: `Cadd9`
4. For bars `1–2`, place:
   - `D3`, `A3`, `C4`, `E4`, `F4`
   - start all of them at `1.1.1`
   - end all of them at `2.4.4`
5. For bars `3–4`, place:
   - `Bb2`, `F3`, `A3`, `C4`
   - start all of them at `3.1.1`
   - end all of them at `4.4.4`
6. For bars `5–6`, place:
   - `F2`, `C3`, `G3`, `A3`
   - start all of them at `5.1.1`
   - end all of them at `6.4.4`
7. For bars `7–8`, place:
   - `C3`, `G3`, `D4`, `E4`
   - start all of them at `7.1.1`
   - end all of them at `8.4.4`
8. Double-check bar `3` specifically:
   - this is where the `A3` enters
   - if `A3` is missing, the break has not actually bloomed

### Why
The break should feel wider because:
- the voicing opens upward
- the `A` in the `Bbmaj7` finally appears
- the bed sustains longer

not because a totally different harmony shows up.

### Rule
- break bloom is a reveal of the same harmonic world, not reharmonization

### Screenshot
- `chords-midi-03-break-bloom`

### Visual MIDI Requirement
- show enough of the break clip that the learner can see the longer sustain and the bloomed `Bbmaj7` state

## Step 7: Define Section Articulation States
### Action
Build these section behaviors from the same chord-bed lane:
- `Intro B`: tucked, filtered, long enough to feel bed-like
- `Drop A`: sustained bed plus restrained pulse
- `Drop A Lift`: same harmony, brighter pulse only
- `Break`: stretched sustain, widest voicing state
- `Re-entry Build`: pulse returns, but keep the restrained `Bb` state
- `Drop B`: bloomed harmony plus stronger width/reverb support

Exact first-pass clip behavior:
1. `Intro B`
   - use the restrained `4`-bar clip
   - set chord note velocity to `70`
   - set each chord to end at `x.4.4`
   - set filter cutoff to `2.0 kHz`
   - set Utility width to `100%`
2. `Drop A`
   - use the same restrained `4`-bar clip
   - set chord note velocity to `78`
   - set each chord to end at `x.4.2`
   - set filter cutoff to `2.0 kHz`
   - set Utility width to `120%`
   - let sidechain create the pulse feel
3. `Drop A Lift`
   - keep the same notes and same basic chord-end points as `Drop A`
   - set chord note velocity to `86`
   - keep each chord ending at `x.4.2`
   - raise filter cutoff from `2.0 kHz` to `2.2 kHz`
   - keep Utility width at `120%`
4. `Break`
   - switch to the `8`-bar bloom clip
   - keep the two-bar sustains exactly as written
   - set chord note velocity to `80`
   - set filter cutoff to `2.5 kHz`
   - set Utility width to `150%`
5. `Re-entry Build`
   - return to the restrained `4`-bar clip
   - set chord note velocity to `76`
   - set each chord to end at `x.4.1`
   - set filter cutoff to `1.9 kHz`
   - set Utility width to `130%`
6. `Drop B`
   - return to the bloomed state
   - if using the `4`-bar bloomed clip, make sure the `Bbmaj7` bar is active again before widening the sends
   - set chord note velocity to `84`
   - set filter cutoff to `2.4 kHz`
   - set Utility width to `140%`
7. `Drop B Lift`
   - keep the same bloomed notes as `Drop B`
   - set chord note velocity to `88`
   - set filter cutoff to `2.6 kHz`
   - set Utility width to `145%`

### Why
This is the “single patch, section-dependent articulation” rule in practice.

You are not making:
- one pad patch
- one stab patch
- one break patch

You are making one harmonic identity that behaves differently by section.

Mechanical changes:
- `Intro B`: velocity `70`, filter `2.0 kHz`, chords end `x.4.4`
- `Drop A`: velocity `78`, filter `2.0 kHz`, chords end `x.4.2`
- `Drop A Lift`: velocity `86`, filter `2.2 kHz`, chords end `x.4.2`
- `Break`: switch to the bloomed `Bbmaj7` clip, longer note values, wider send/width state
- `Re-entry Build`: velocity `76`, filter `1.9 kHz`, chords end `x.4.1`
- `Drop B`: velocity `84`, filter `2.4 kHz`, bloomed `Bbmaj7` active
- `Drop B Lift`: velocity `88`, filter `2.6 kHz`, bloomed `Bbmaj7` active

### Screenshot
- `chords-06-section-articulation-map`

## Step 8: Add Chord Bus EQ And Sidechain
### Action
On the `Chords` track or `Music` bus, build this starting chain:
1. `EQ Eight`
2. `Compressor` for kick sidechain or groove-ducking
3. `Utility`

What the bus means here:
- if `Chords` is inside a `Music` group, put this chain on the `Chords` track first
- if later the project has several music tracks, move the same chain to the `Music` group only after the single-track version works

Set `EQ Eight` like this:
1. Turn on band `1`.
2. Set band `1` to high-pass.
3. Set frequency to `180 Hz`.
4. Set slope to `12 dB/oct`.
5. Turn on one bell band at `250 Hz`.
6. Set that bell to `0 dB` on the first pass.
7. If low-mid mud appears, cut that bell to `-2 dB`, Q `1.0`.

Set the sidechain compressor like this:
1. Open Ableton `Compressor`.
2. Click the sidechain triangle to open the sidechain panel.
3. Turn `Sidechain` on.
4. Set `Audio From` to the kick lane or drum lane that carries the kick body.
5. Set ratio to `2:1`.
6. Set attack to `1 ms`.
7. Set release to `150 ms`.
8. Lower threshold until each kick causes `1–2 dB` of gain reduction on the chord bed.

Set `Utility` like this on the first pass:
- `Drop A`: width `120%`
- `Break`: width `150%`
- `Re-entry Build`: width `130%`
- `Drop B`: width `140%`
- `Drop B Lift`: width `145%`

### Why
The chords should move with the groove but not collapse.

If the sidechain is too deep:
- raise the compressor threshold until gain reduction is only `1 dB` on each kick
- if the threshold move is not enough, reduce ratio from `2:1` to `1.5:1`

If it is too weak:
- lower the compressor threshold until each kick creates at least `1 dB` of gain reduction
- do not exceed `3 dB` of gain reduction on the first pass

### Screenshot Set
- `chords-bus-01-eq`
- `chords-bus-02-sidechain`

## Step 9: Automate Width And Returns By Section
### Action
1. Keep `Drop A` narrower and drier than the break.
2. Raise `Return C: long filtered hall` send in the break from `-22 dB` to `-14 dB`.
3. Pull that send back to `-20 dB` in the `Re-entry Build`.
4. Let `Drop B` reopen at width `140%` and `Return C` send `-16 dB`.
5. Let `Drop B Lift` reach width `145%` and `Return C` send `-15 dB`.

Create these first-pass automation values:

Utility `Width`:
- `Intro B`: `100%`
- `Drop A`: `120%`
- `Drop A Lift`: `120%`
- `Break`: `150%`
- `Re-entry Build`: `130%`
- `Drop B`: `140%`
- `Drop B Lift`: `145%`

`Return C: long filtered hall` send on the `Chords` track:
- `Intro B`: `-24 dB`
- `Drop A`: `-22 dB`
- `Drop A Lift`: `-21 dB`
- `Break`: `-14 dB`
- `Re-entry Build`: `-20 dB`
- `Drop B`: `-16 dB`
- `Drop B Lift`: `-15 dB`

How to write the automation in Ableton:
1. Press `A` to show automation lanes.
2. On the `Chords` track, choose `Utility` -> `Width`.
3. Draw the width values at the start of each section.
4. Then choose `Mixer` -> `Send C`.
5. Draw the send values at the start of each section.
6. Keep each value flat across the section on the first pass; do not draw constant wiggles yet.

### Why
This is where the harmonic staging becomes a physical experience.

The bloom must be heard not only in note choice, but in:
- width
- sustain
- return space

### Screenshot Set
- `chords-07-width-automation`
- `chords-08-return-c-send`

## Step 10: A/B Against References
### Action
Bounce or loop `drums + bass + chords`.

Compare against:
- `Sammy Virji - I Guess We're Not the Same`
  - listen for chord readability in a club-weight mix
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - listen for harmonic support sitting around groove rather than swallowing it
- `KETTAMA - It Gets Better`
  - listen for whether the track still feels physical after the chords arrive

### What To Listen For
- does `Drop A` still feel restrained?
- does the bar-2 `Bb` feel like latent hope rather than full bloom?
- does the break feel wider without sounding like a new song?
- do the chords stay above the bass instead of fogging the low-mid?

### Expected Answer
- the harmony should feel emotionally legible by `Drop A`, but clearly more open in the break and `Drop B`
- the biggest emotional reveal should happen when the `Bbmaj7` state and width open together, not before

## Troubleshooting
### Problem: “Drop A already feels too open.”
Fix order:
1. remove the `A` from the restrained `Bb` bar
2. set `Drop A` Utility width from `120%` down to `110%`
3. set `Drop A` `Return C` send from `-22 dB` down to `-26 dB`
4. only then lower the filter cutoff from `2.0 kHz` to `1.8 kHz`

### Problem: “The chords feel stiff.”
Fix order:
1. open the MIDI clip and check that common tones such as `C4` and `F3/F4` do not jump octaves unnecessarily
2. move note ends from `x.4.2` to `x.4.3`
3. if that still feels clipped, move note ends to `x.4.4`
4. only then increase `Return C` by `+2 dB`

### Problem: “The chords are fighting the bass.”
Fix order:
1. raise the chord high-pass from `180 Hz` to `200 Hz`
2. if still cloudy, raise it once more to `220 Hz` maximum on the first pass
3. cut the `250 Hz` bell to `-2 dB`, Q `1.0`
4. reduce `Return C` by `-3 dB` in the affected section

### Problem: “The chords sound like a high hospital monitor beep.”
Fix order:
1. confirm the MIDI clip contains all chord notes, not just one top note
2. for the first chord, confirm `D3`, `F3`, `A3`, `C4`, and `E4` all start at `1.1.1`
3. in Serum voicing, confirm `Mono` is off and `Poly` is at least `8`
4. make sure you are using the safe first-pass voicing before auditioning the old `D3 A3 C4 E4 F4` color
5. lower filter cutoff toward `1.6–2.0 kHz`
6. increase amp attack toward `35–45 ms`
7. reduce `Osc B Level` to `0%` temporarily and judge `Osc A` alone
8. reduce saturation drive to `0` temporarily
9. if the chord is still piercing, lower velocity on the highest note or move only `E4` down to `E3` as a diagnostic

Do not solve the beep by adding reverb. Reverb makes a bad beep wider; it does not turn it into a warm chord bed.

### Problem: “The break got wider, but not more emotional.”
Fix order:
1. open the break MIDI clip and check that bar `3` contains `A3` in the `Bbmaj7` chord
2. check that the break clip uses two-bar sustains ending at `2.4.4`, `4.4.4`, `6.4.4`, and `8.4.4`
3. set break Utility width to `150%`
4. set break `Return C` send to `-14 dB`

### Problem: “I followed the voicings and it still feels flat.”
Fix order:
1. A/B your `Drop A` and break against the references at matched loudness
2. open the restrained clip and check that bar `2` is only `Bb2`, `F3`, `C4`
3. open the bloomed clip and check that the `Bbmaj7` state is `Bb2`, `F3`, `A3`, `C4`
4. if the difference is present but still inaudible, raise break filter cutoff from `2.5 kHz` to `2.7 kHz`
5. if it still reads flat after the hook is added later, cut the chord bed `1.5–2.5 kHz` by `-1.5 dB` instead of raising every melodic lane

## What Must Be Captured For Later Lesson Conversion
- chord-bed patch screenshots
- restrained vs bloomed `Bb` MIDI screenshots
- one full `4`-bar drop chord screenshot
- one full break bloom screenshot
- chord bus chain screenshot
- width/send automation screenshot
- one checkpoint bounce of `drums + bass + chords`
