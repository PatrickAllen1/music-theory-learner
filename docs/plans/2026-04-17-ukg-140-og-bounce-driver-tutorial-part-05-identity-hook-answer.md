# UKG 140 OG Bounce Driver: Tutorial Part 5 — Identity (Hook + Answer)

## Purpose
Teach the learner how to build the hook and answer lanes for `ukg-140-og-bounce-driver` so they:
- carry the instrumental without a vocal
- stay rhythm-first and phrase-end-led
- feel like one instrument family in conversation
- get bigger in `Drop B` by substitution, not stacking

This part should turn the identity plan into exact patch, MIDI, and send/automation choices.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)

## Outcome
By the end of this part, the learner should have:
- one `Serum 2` hook patch
- one derived `Serum 2` answer patch
- one `Hook` MIDI lane
- one `Answer` MIDI lane
- one `4`-bar `Drop A` hook phrase
- one `4`-bar `Drop B` hook/answer conversation phrase
- one hook/answer bus or processing lane
- one bounce of:
  - `drums + bass + chords + hook`
  - `Drop B` phrase with answer included

## Time Estimate
- `40–60 minutes`

## Prerequisites
- learner has completed or can reference:
  - `Part 2` groove
  - `Part 3` bass floor
  - `Part 4` harmonic bed
- learner can program short MIDI phrases and automate return sends
- learner can duplicate a Serum patch and edit it without losing the original

## What The Learner Should Understand Before Starting
Part `5` depends on the Part `4` chord bed being basically correct.

Before writing the hook, verify the chord lane:
- `Chords` Serum patch has `Mono` off
- `Legato` is off
- `Poly` is at least `8`
- the safe first-pass `Dm9` is `D3 F3 A3 C4 E4`
- the chord sound is a soft garage organ/pad hybrid, not a single-note beep
- the old `D3 A3 C4 E4 F4` color is not the default; save it for a later audition only

If the chord bed still sounds like a beep, stop and fix Part `4` before continuing. Do not build a brighter or louder hook to compensate for a broken chord bed.

The hook is not a full topline.

It exists to:
- give the instrumental a recognisable center
- speak late in the phrase
- leave room for the drums and bass to remain the real physical engine

The answer is not a second melody.

It exists to:
- punctuate phrase endings in `Drop B`
- make the section feel bigger by alternation
- sound related to the hook, not like a different song arriving

Timing reminder for this part:
- positions such as `4.3.4` are local positions inside a `4`-bar hook or answer clip
- positions such as `100.3.4` are full-song Arrangement View positions
- local `4.3.4` and arrangement `4.3.4` are not the same thing

Plain-English routing reminder:
- the `dry` hook is the original hook sound before reverb or delay
- a `return` is a shared effect track, such as a plate reverb or filtered delay
- a `send` is the amount of copy you send from the hook or answer track into that return effect
- the hook should stay mostly dry and centered so the rhythm stays clear
- the return effects should add space after the note, not replace the note

## Reference Axis
Primary A/B for this part:
- `Sammy Virji - I Guess We're Not the Same`
  - listen for low-note-count hook clarity
  - listen for how the hook stays readable without swallowing the groove
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - listen for how hook energy can sit inside a rolling bass-led track

Secondary check:
- `Interplanetary Criminal - Slow Burner`
  - listen for phrase-end punctuation and how little can still feel memorable

## Files / Assets Needed
- current project with:
  - `Drums`
  - `Bass`
  - `Chords`
- one MIDI track named `Hook`
- one MIDI track named `Answer`
- one group named `Identity` if the project does not already group these lanes
- access to the Production Plan sections:
  - `Hook and Answer Spec`
  - `Top-End, Air, and Stereo`
  - `Return B: short plate`
  - `Return D: filtered delay`

## Core Musical Material
Use this as the source of truth:
- `Drop A` hook cell: `A3 -> C4 -> D4`
- `Drop B` hook cell: `A3 -> C4 -> D4 -> F4`
- answer cell: `G3 -> A3 -> C4`
- the old higher register `A4 -> C5 -> D5 -> F5` is no longer the default
- only audition the higher octave later if the lower organ hook gets buried after drums, bass, and chords are all playing

Rhythmic identity:
- on the `a` of beat `3` = `x.3.4`
- on beat `4` = `x.4.1`
- on the `a` of beat `4` = `x.4.4`
- on hook-owned `Drop B` bloom phrases, `F4` lands on beat `1` of the following bar

Kick relationship rule:
- do not start the hook on beat `1` of its own bar
- beat `4` and the following bar's beat `1` are allowed accent collisions when they make the phrase hit harder

Conversation rule:
- `Drop B`: hook at half density
- answer phrase-end only
- hook and answer alternate rather than stack

## Step 1: Create The Identity Lanes
### Action
1. Create two MIDI tracks.
2. Rename the first one:
   - click the track header
   - press `Cmd+R` on Mac or `Ctrl+R` on Windows
   - type `Hook`
   - press `Enter`
3. Rename the second one the same way, but type `Answer`.
4. Right-click each track header and assign colors that are clearly different from:
   - `Chords`
   - `Bass`
5. Route both tracks to an `Identity` group if the session is already organized by lane families.
6. Create one `4`-bar clip slot or arrangement region on `Hook` for `Drop A`.
7. Create one `4`-bar clip slot or arrangement region on `Hook` for `Drop B`.
8. Create matching clip slots or regions on `Answer` for `Drop B`.

### Why
The hook and answer need:
- shared family logic
- separate MIDI behavior
- separate send and density control

If they share one MIDI lane too early, it becomes harder to enforce the alternation rule later.

### Screenshot
- `identity-01-lane-setup`

## Step 2: Build The Hook Patch In Serum 2
### Action
1. Load a fresh instance of `Serum 2` on `Hook`.
2. Initialize the patch.
3. Turn `Sub` off.
4. Turn `Noise` off.
5. Turn `Osc C` off if your Serum version shows it.
6. Keep `Osc A` on.
7. Keep `Osc B` on, but treat it as quiet color only.
8. Set `Mono` off.
9. Set `Poly` to at least `8`.
10. Set `Legato` off.
11. Set `Porta` off or leave it at `0`.
12. Set `Osc A` to `Basic Shapes`.
13. Choose a square-leaning or triangle-square frame:
    - do not use a pure sine frame
    - do not use a pure triangle frame if it sounds like a beep
    - do not use a bright saw frame on the first pass
    - if you are unsure, move the wavetable position until the note says `duh` more than `ding`
14. Set `Osc A Level` to `90%`.
15. Set `Osc B` to `Basic Shapes`.
16. Choose a soft triangle or soft square support shape:
    - avoid bright saw on the first pass
    - avoid metallic / glassy frames
17. Set `Osc B Level` to `10%`.
18. Leave FM off on the first pass.
19. If the patch feels too plain after the lower octave hook is programmed, turn on `FM from B` and keep it very low:
    - starting amount: `0–6%`
    - hard first-pass maximum: `10%`
20. Route the patch through a smooth low-pass or softening filter:
    - `MG Low 12` or similar
21. Set filter values:
    - cutoff: `1.4 kHz`
    - resonance: `0–5%`
    - drive: `0–4%`
22. Set amp envelope:
    - attack: `2–5 ms`
    - hold: `0 ms`
    - decay: `260 ms`
    - sustain: about `-10 dB` to `-7 dB`
    - release: `150 ms`
23. Do not turn on Serum reverb, delay, chorus, hyper, or compressor while building the dry hook.

Immediate sound check:
1. Play `A3 -> C4 -> D4`.
2. The sound should read as `duh-duh-duh`, not `ding-ding-ding`.
3. If it sounds like an electric notification:
   - turn FM off
   - lower `Osc B Level` to `5–8%`
   - lower filter cutoff toward `1.2 kHz`
   - use a more square-leaning `Osc A` frame
4. If it sounds like a plain beep:
   - move `Osc A` away from sine/triangle toward square
   - raise decay toward `300 ms`
   - raise sustain slightly, but do not turn it into a pad
5. If the lower octave sounds organ-like and the higher octave sounds like a beep, keep the lower octave.

### Why
The hook should feel:
- warm
- woody
- readable
- not vocal-dependent

If the patch sounds too glossy, too wide, or too bell-like, it will stop feeling like garage identity and start feeling like pop garnish.

### Final Hook Starting Spec
- engine: `Serum 2`
- family: warm organ-pluck / woody garage stab
- Sub: `Off`
- Noise: `Off`
- Osc A: square-leaning or triangle-square body
- Osc A Level: `90%`
- Osc B: soft triangle/square support
- Osc B Level: `10%`
- FM mode: `Off` first pass, optional `FM from B` only if needed
- FM amount: `0–6%`, hard first-pass maximum `10%`
- filter: `MG Low 12`
- cutoff: `1.2–1.6 kHz`
- resonance: `0–5%`
- drive: `0–4%`
- amp env:
  - A `2–5 ms`
  - H `0 ms`
  - D `240–320 ms`
  - S about `-10 dB` to `-7 dB`
  - R `140–180 ms`
- voicing:
  - Mono `Off`
  - Poly at least `8`
  - Legato `Off`
  - Porta `Off`

### Screenshot Set
- `identity-02-hook-oscillators`
- `identity-03-hook-filter-env`

## Step 3: Add Hook Character Processing
### Action
1. After `Serum 2`, add `Saturator`.
2. Set `Saturator` like this:
   - mode: `Analog Clip`
   - drive: `+1 dB`
   - output: `-1 dB`
   - soft clip: `On`
3. Add `EQ Eight` after `Saturator`.
4. Turn on band `1`.
5. Set band `1` to high-pass.
6. Set the high-pass frequency to `220 Hz`.
7. Set the high-pass slope to `12 dB/oct`.
8. Leave compressor off on the first pass.
9. Add `Utility` after `EQ Eight`.
10. Set `Utility Width` to `105%`.
11. Keep the track pan centered.

Compressor rule:
- only add a compressor if one hook note peaks more than `6 dB` louder than the other hook notes
- if that happens, add `Compressor` after `EQ Eight`, ratio `2:1`, attack `5 ms`, release `80 ms`, and lower threshold until the loudest note dips `1–2 dB`

### Why
The hook should speak clearly in the middle of the mix.

Its width should mostly come from:
- returns
- filtered delay throws
- short plate support

not from smearing the dry signal left-right.

### Screenshot Set
- `identity-04-hook-fx`
- `identity-05-hook-eq`

## Step 4: Build The Answer Patch From The Hook
### Action
1. Duplicate the hook patch onto the `Answer` track.
2. On the `Answer` Serum patch, keep the same oscillator choices as the hook.
3. Keep `Sub` off and `Noise` off.
4. Keep FM off unless you already turned on a very low FM amount for the hook.
5. If FM is on, keep the answer FM amount at or below the hook amount.
6. Change the amp envelope:
   - attack: `2 ms`
   - hold: `0 ms`
   - decay: `100 ms`
   - sustain: about `-12 dB`
   - release: `70 ms`
7. Raise filter cutoff slightly above the hook, but keep it warm:
   - if the hook is at `1.4 kHz`, start the answer around `1.6 kHz`
   - do not jump straight to `2.4 kHz` unless the answer is buried
8. Keep filter resonance low:
   - `0–5%`
9. Keep filter drive low:
   - `0–4%`
10. On the `Answer` Saturator, set:
   - drive: `+1.5 dB`
   - output: `-1.5 dB`
   - soft clip: `On`
11. On the `Answer` EQ Eight, keep the high-pass at `220 Hz`.
12. On the `Answer` Utility, set width to `105–110%`.
13. Keep the answer in the same instrument family.
14. Do not widen it into a separate cinematic layer.

### Why
The answer should feel like:
- the same family
- a shorter reply
- rougher by `+0.5 dB` more saturation drive than the hook

not a second lead synth.

### Final Answer Starting Spec
- same patch family as the hook
- Sub and Noise: `Off`
- envelope: A `2 ms`, H `0 ms`, D `100 ms`, S about `-12 dB`, R `70 ms`
- filter cutoff: about `1.6 kHz`
- resonance: `0–5%`
- drive: `0–4%`
- saturation drive: `+1.5 dB`
- Utility width: `105–110%`
- phrase-end punctuation only

### Screenshot Set
- `identity-06-answer-deltas`
- `identity-07-hook-vs-answer`

## Step 5: Program The Drop A Hook Phrase
### Action
Create one `4`-bar `Drop A` hook clip using:
- `A3 -> C4 -> D4`

Starting rhythm:
- on the `a` of beat `3`
- on beat `4`
- on the `a` of beat `4`

Starting density rule:
- use the hook as phrase-end punctuation, not every bar
- first pass:
  - place it in the last bar of the `4`-bar phrase
  - do not add hook notes to bars `1`, `2`, or `3` during the first pass
  - only after the full `Drop A` A/B check may you copy the same bar-`4` phrase to bar `2`
  
Exact first-pass MIDI placement inside the `4`-bar clip:
1. Leave bars `1`, `2`, and `3` empty.
2. In bar `4`, set the piano-roll grid to `1/16`.
3. Place `A3` at `4.3.4`.
4. Give `A3` a `1/16` length so it ends at `4.4.1`.
5. Place `C4` at `4.4.1`.
6. Give `C4` a `1/8` length so it ends at `4.4.3`.
7. Place `D4` at `4.4.4`.
8. Give `D4` a short `1/16` length so it acts like a phrase-end jab rather than a long held note.
9. Do not move this phrase up to `A4 -> C5 -> D5` unless the lower register disappears in the full mix.

### Why
The hook has to feel memorable because of:
- timing
- timbre
- repetition discipline

not because it has lots of notes.

This phrase is allowed to collide with selected kicks:
- beat `4` is a deliberate accent
- `F4` on the next bar's beat `1` is the bloom accent

### Screenshot
- `identity-midi-01-drop-a-hook`

### Visual MIDI Requirement
- show the full `4`-bar clip
- label the `A3`, `C4`, and `D4`
- annotate the `3a -> 4 -> 4a` rhythm clearly

## Step 6: Program The Drop B Hook Variant
### Action
Duplicate the `Drop A` hook clip and edit it for `Drop B`:
- `A3 -> C4 -> D4 -> F4`

Rules:
- `F4` is the bloom note
- it should not appear in `Drop A` or `Drop A Lift`
- keep the same rhythmic identity
- when used, `F4` lands on beat `1` of the following bar as the phrase re-opens

Starting density rule:
- keep the hook at half density in `Drop B`
- do not simply add the `F4` to every phrase ending

Exact first-pass placement for the first hook-owned `Drop B` phrase in Arrangement View:
1. Use the first hook-owned `Drop B` phrase at bar `100` as your model.
2. Place `A3` at `100.3.4`.
3. Place `C4` at `100.4.1`.
4. Place `D4` at `100.4.4`.
5. Place `F4` at `101.1.1`.
6. Use these exact note lengths:
   - `A3`: `1/16`, ending at `100.4.1`
   - `C4`: `1/8`, ending at `100.4.3`
   - `D4`: `1/16`, ending at `101.1.1`
   - `F4`: `1/8`, ending at `101.1.3`
7. If you are sketching this in a loop clip instead of Arrangement View, temporarily extend the clip long enough to place the `F4` on the following bar, then trim and duplicate once the phrase reads correctly.

### Why
`Drop B` gets bigger because:
- the harmony blooms
- the hook blooms
- the answer enters

But if the hook keeps full density while the answer arrives, the section will feel crowded instead of bigger.

### Screenshot
- `identity-midi-02-drop-b-hook`

## Step 7: Program The Phrase-End Answer
### Action
Create one `4`-bar `Drop B` answer clip using:
- `G3 -> A3 -> C4`

Placement rules:
- answer lives at phrase ends only
- it should land on alternate phrase endings from the hook
- do not let it speak in every bar

Starting placement:
- in a first `16`-bar `Drop B` pass:
  - let the hook own bars `4` and `12`
  - let the answer own bars `8` and `16`
- treat the answer as punctuation after the groove has already spoken

Exact first-pass MIDI placement for the first answer-owned phrase ending:
1. Use bar `104` as the first answer-owned phrase ending in the full song.
2. Set the piano-roll grid to `1/16`.
3. Place `G3` at `104.3.3`.
4. Give `G3` a `1/16` length so it ends at `104.3.4`.
5. Place `A3` at `104.4.1`.
6. Give `A3` a `1/16` length so it ends at `104.4.2`.
7. Place `C4` at `104.4.4`.
8. Give `C4` a `1/16` length on the first pass so it ends at `105.1.1`.
9. Repeat the same rhythmic idea at bar `112` for the second answer-owned phrase ending:
   - `G3` at `112.3.3`, length `1/16`
   - `A3` at `112.4.1`, length `1/16`
   - `C4` at `112.4.4`, length `1/16`

### Why
The answer should make `Drop B` feel more conversational, not denser for density’s sake.

### Rule
If the answer feels like a second full hook, it is too long, too frequent, or too loud.

### Screenshot
- `identity-midi-03-answer-placement`

### Visual MIDI Requirement
- show one `4`-bar `Drop B` phrase with both hook and answer lanes visible
- annotate where the hook yields and where the answer takes over

## Step 8: Build Hook / Answer Sends And Throws
### Action
1. Send both lanes to `Return B: short plate`.
2. Use `Return D: filtered delay` sparingly for phrase-end throws.
3. Keep the hook’s dry center stronger than the return signal.
4. Let the answer have more throw support than the hook, but not more center weight.

First-pass constant send values:
1. On the `Hook` track, set `Send B` to `-18 dB`.
2. On the `Answer` track, set `Send B` to `-16 dB`.
3. On both tracks, set `Send D` to `-inf` / fully off by default.

First-pass delay throws:
1. Press `A` in Ableton to show automation.
2. On the `Hook` track, choose `Mixer` -> `Send D`.
3. Draw `Send D` up to `-20 dB` from `100.4.4` to `101.1.2`.
4. Draw it back to `-inf` at `101.1.3`.
5. Repeat the same hook throw from `108.4.4` to `109.1.2`.
6. On the `Answer` track, choose `Mixer` -> `Send D`.
7. Draw `Send D` up to `-18 dB` from `104.4.4` to `105.1.2`.
8. Draw it back to `-inf` at `105.1.3`.
9. Repeat the same answer throw from `112.4.4` to `113.1.2`.

Starting direction:
- hook:
  - cleaner dry center
  - `Send B` at `-18 dB`
  - occasional filtered delay only at bigger phrase endings
- answer:
  - `Send B` at `-16 dB`
  - `Send D` throws at answer-owned phrase endings
  - shorter dry body

### Why
The hook carries identity.
The answer carries punctuation.

The FX should reinforce that difference.

### Screenshot Set
- `identity-08-plate-send`
- `identity-09-delay-throw`

## Step 9: Check Register And Density Against The Chords
### Action
1. Before judging the hook, check the `Chords` lane again:
   - `Mono`: off
   - `Poly`: at least `8`
   - first chord: `D3 F3 A3 C4 E4`
   - no single-note beep
2. Play `drums + bass + chords + hook`.
3. Mute the `Chords` track and listen to the hook for one pass.
4. Unmute the `Chords` track.
5. The hook should still read without raising the `Hook` track fader by more than `+1 dB`.
6. If the hook disappears and the chords still sound beepy or mono, go back to Part `4`; do not EQ around a broken chord sound.
7. If the chord bed is healthy but the hook disappears, cut the `Chords` track with `EQ Eight`:
   - bell frequency: `2.0 kHz`
   - gain: `-1.5 dB`
   - Q: `1.0`
8. Only after that carve should you raise the `Hook` fader.
9. Play the `Drop B` phrase with answer.
10. Check the full-song bars:
   - hook-owned phrase endings: `100` and `108`
   - answer-owned phrase endings: `104` and `112`
11. If both `Hook` and `Answer` contain notes at the same phrase ending, delete the weaker phrase instead of lowering it.

### Why
This is the main integration test for the identity lane.

If the hook disappears:
- it is either too dark
- too low in level
- or the chords are too open in the same register

If the answer makes the section smaller:
- it is too continuous
- too loud
- or too similar in density to the hook

First correction for each failure:
- hook too dark: raise hook filter cutoff from `1.4 kHz` toward `1.8 kHz`
- hook too low: raise the `Hook` fader by `+1 dB` maximum before changing anything else
- chords too open: cut the `Chords` track at `2.0 kHz` by `-1.5 dB`, Q `1.0`
- answer too continuous: delete any answer notes outside bars `104` and `112`
- answer too loud: lower the `Answer` fader by `-1.5 dB`
- answer too similar: shorten answer decay from `100 ms` to `75 ms`

### Screenshot
- `identity-10-lane-balance`

## Step 10: A/B Against References
### Action
Bounce:
- `drums + bass + chords + hook`
- one `Drop B` phrase including answer

Compare against:
- `Sammy Virji - I Guess We're Not the Same`
  - listen for low-note-count hook clarity
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - listen for identity living inside a bass-led track
- `Interplanetary Criminal - Slow Burner`
  - listen for phrase-end punctuation and restraint

### What To Listen For
- does the hook read on first listen without sounding like a full vocal topline?
- does the `F4` feel like a real bloom when it appears?
- does the answer feel like family, not a new instrument?
- does `Drop B` get bigger by alternation rather than by pile-up?

### Expected Answer
- `Drop A` should feel identifiable with only `A3 -> C4 -> D4`
- `Drop B` should feel more open when `F4` appears, but still disciplined
- the answer should sound like a reply, not a second lead

## Troubleshooting
### Problem: “The hook feels generic.”
Fix order:
1. open the MIDI clip and check the note starts are exactly `4.3.4`, `4.4.1`, and `4.4.4`
2. confirm the hook notes are in the lower organ register: `A3`, `C4`, `D4`
3. raise hook filter cutoff from `1.4 kHz` toward `1.8 kHz`
4. if still dull, raise Saturator drive from `+1 dB` to `+1.5 dB`
5. only then consider one phrase-end timing variation; do not add a fourth note to `Drop A`

### Problem: “The hook is fighting the chords.”
Fix order:
1. confirm the chord bed is polyphonic: `Mono` off, `Poly` at least `8`
2. confirm the first chord is the safe `D3 F3 A3 C4 E4` voicing
3. raise the hook high-pass from `220 Hz` to `250 Hz`
4. set hook Utility width from `105%` to `100%`
5. cut the chord bed at `2.0 kHz` by `-1.5 dB`, Q `1.0`
6. only then reduce the hook level by `-1 dB`

### Problem: “The answer sounds like another song.”
Fix order:
1. reduce answer Saturator drive from `+1.5 dB` to `+1.0 dB`
2. if answer Utility width is above `110%`, bring it down to `105%`
3. set answer decay to `75 ms` and release to `50 ms`
4. remove any answer notes outside bars `104` and `112`

### Problem: “Drop B got busier but not bigger.”
Fix order:
1. thin the hook to half density
2. keep the answer phrase-end only
3. check that hook owns bars `100` and `108`
4. check that answer owns bars `104` and `112`
5. remove any phrase where both speak at the same ending

### Problem: “I followed the notes and it still doesn’t stick.”
Fix order:
1. A/B against the references at matched loudness
2. open the hook clip and check the rhythm lands at `4.3.4`, `4.4.1`, and `4.4.4`
3. check that the hook notes are `A3`, `C4`, and `D4`, not the higher `A4`, `C5`, and `D5`
4. check that the hook patch is not in beep mode:
   - Sub off
   - Noise off
   - FM off or below `6%`
   - Osc A square-leaning, not pure sine
5. check that the filter cutoff is around `1.2–1.8 kHz`
6. if the lower octave hook is audible but still bland, raise filter cutoff slightly before adding notes

### Problem: “The hook sounds like a bell, beep, or phone notification.”
Fix order:
1. keep the MIDI in the lower register: `A3 -> C4 -> D4`
2. turn FM off
3. lower `Osc B Level` to `5–8%`
4. make sure `Sub` and `Noise` are off
5. move `Osc A` away from sine/triangle toward a square-leaning `Basic Shapes` frame
6. lower filter cutoff toward `1.2 kHz`
7. set envelope hold to `0 ms`, decay around `260–320 ms`, sustain around `-10 dB` to `-7 dB`, and release around `140–180 ms`

## What Must Be Captured For Later Lesson Conversion
- hook patch screenshots
- answer patch delta screenshots
- `Drop A` hook MIDI screenshot
- `Drop B` hook + answer MIDI screenshot
- plate and delay throw screenshots
- one bounce of:
  - `drums + bass + chords + hook`
  - `Drop B` with answer
