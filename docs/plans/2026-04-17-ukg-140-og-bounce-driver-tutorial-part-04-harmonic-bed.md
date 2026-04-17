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
  - `Transition B`
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
- `Dm9`: `D3 A3 C4 E4 F4`
- restrained `Bb`: `Bb2 F3 C4`
- bloomed `Bbmaj7`: `Bb2 F3 A3 C4`
- `Fadd9`: `F2 C3 G3 A3`
- `Cadd9`: `C3 G3 D4 E4`

## Step 1: Create The Chord Lane
### Action
1. Create one MIDI track named `Chords`.
2. Route it to the `Music` or `Chords` group.
3. Color it differently from bass and hook lanes.
4. Create one empty MIDI clip for the drop loop and one empty MIDI clip for the break clip.

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
3. Set `Osc A` to `Basic Shapes`.
4. Choose a warm saw / triangle-leaning frame:
   - somewhere between saw and triangle, not a bright full saw
5. Set `Osc A Level` around `85%`.
6. Set `Osc B` to `Basic Shapes`.
7. Choose a quieter support shape:
   - slightly brighter than `Osc A`
8. Set `Osc B Level` around `25–35%`.
9. Keep both oscillators in the same octave to start.
10. Use restrained unison:
    - `Osc A`: `2 voices`
    - `Osc B`: `1–2 voices`
11. Set detune lightly:
    - start around `0.03–0.05`
12. Route the patch through a smooth low-pass filter:
    - `MG Low 12` or equivalent
13. Set initial filter settings:
    - cutoff: start around `2.2–3.2 kHz`
    - resonance: `8–12%`
    - drive: `5–10%`
14. Set amp envelope:
    - attack: `5–15 ms`
    - decay: `700–1200 ms`
    - sustain: `55–75%`
    - release: `250–450 ms`

### Why
This patch needs to behave like:
- an emotional bed first
- a pulse-capable layer second

It should not sound like:
- a huge trance supersaw
- a dry organ stab
- a long washy pad with no front edge

### Final Chord-Bed Starting Spec
- engine: `Serum 2`
- Osc A: warm saw / triangle-leaning body
- Osc B: quieter upper support
- unison: restrained
- detune: `0.03–0.05`
- filter: smooth low-pass
- cutoff: `~2.2–3.2 kHz` start
- resonance: `8–12%`
- drive: `5–10%`
- amp env:
  - A `5–15 ms`
  - D `700–1200 ms`
  - S `55–75%`
  - R `250–450 ms`

### Screenshot Set
- `chords-02-oscillators`
- `chords-03-filter-and-env`

## Step 3: Add Width And Glue Inside The Patch
### Action
1. Add a gentle width source:
   - chorus or subtle hyper/dimension type movement
2. Keep it restrained:
   - enough to widen the bed
   - not enough to hollow the center
3. Add mild saturation if needed.
4. Do not solve the whole space story with in-patch reverb.

### Why
Most of the section-dependent space should come from:
- bus decisions
- return sends
- automation

If the patch is already huge before the mix, the break has nowhere to open.

### Starting FX Direction
- chorus / width: subtle
- saturation: glue, not fuzz
- in-patch reverb: off or minimal

### Screenshot Set
- `chords-04-width`
- `chords-05-fx`

## Step 4: Program The Restrained Drop Loop
### Action
Create a `4`-bar MIDI clip for the drop state:
- Bar 1: `Dm9` = `D3 A3 C4 E4 F4`
- Bar 2: restrained `Bb` = `Bb2 F3 C4`
- Bar 3: `Fadd9` = `F2 C3 G3 A3`
- Bar 4: `Cadd9` = `C3 G3 D4 E4`

Starting placement:
- one chord per bar
- hold each chord long enough to feel like a bed
- leave enough space at the bar edges that pulse articulation can still speak later

### Why
This is the emotional floor of the song.

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
- keep the same progression
- switch the `Bb` bar to bloomed `Bbmaj7` = `Bb2 F3 A3 C4`
- lengthen the chord values into more stretched `2`-bar-feel movement
- let the upper register breathe more clearly

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
- `Drop A Lift`: same harmony, slightly brighter pulse only
- `Break`: stretched sustain, widest voicing state
- `Transition B`: pulse returns, but keep the restrained `Bb` state
- `Drop B`: bloomed harmony plus stronger width/reverb support

### Why
This is the “single patch, section-dependent articulation” rule in practice.

You are not making:
- one pad patch
- one stab patch
- one break patch

You are making one harmonic identity that behaves differently by section.

Mechanical changes:
- `Intro B`: darker filter, lower velocity, longer note lengths
- `Drop A`: same clip family, but shorten note lengths slightly or increase the sidechain/pulse feel
- `Drop A Lift`: keep the same notes, raise pulse velocity a little and open the filter slightly
- `Break`: switch to the bloomed `Bbmaj7` clip, longer note values, wider send/width state
- `Transition B`: return to restrained `Bb`, shorter pulse values, reduced width and reverb
- `Drop B`: reopen width/send and use the bloomed `Bbmaj7` state again

### Screenshot
- `chords-06-section-articulation-map`

## Step 8: Add Chord Bus EQ And Sidechain
### Action
On the `Chords` track or `Music` bus, build this starting chain:
1. `EQ Eight`
2. `Compressor` for kick sidechain or groove-ducking
3. `Utility`

Starting direction:
- high-pass the chord bed enough to stay out of bass ownership:
  - start around `180 Hz`, then move up if low-mid clouds
- if the low-mid clouds up:
  - cut a little around `200–300 Hz` before thinning the bass floor
- sidechain lightly from the kick:
  - ratio `2:1` to `4:1`
  - fast attack
  - release roughly `120–180 ms`

### Why
The chords should move with the groove but not collapse.

If the sidechain is too deep:
- the harmony disappears

If it is too weak:
- the track slows down and mud gathers.

### Screenshot Set
- `chords-bus-01-eq`
- `chords-bus-02-sidechain`

## Step 9: Automate Width And Returns By Section
### Action
1. Keep `Drop A` narrower and drier than the break.
2. Send more to `Return C: long filtered hall` in the break.
3. Pull some of that space back in `Transition B`.
4. Let `Drop B` reopen with:
   - more width
   - more air around the bed
   - but not so much wash that the hook loses its lane

Starting width behavior:
- `Drop A`: around `120%` equivalent width feel
- `Break`: around `150%`
- `Transition B`: tighten back toward `130%`
- `Drop B`: reopen near `140%`, then widen slightly more again in the lift

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
2. narrow the chord width
3. reduce long-hall send
4. only then darken the patch

### Problem: “The chords feel stiff.”
Fix order:
1. check voice leading
2. lengthen or overlap chord tails slightly
3. only then soften the patch or increase return space

### Problem: “The chords are fighting the bass.”
Fix order:
1. high-pass the chord bed a little more
2. trim `200–300 Hz` before touching the bass floor
3. reduce return buildup in the low-mid

### Problem: “The break got wider, but not more emotional.”
Fix order:
1. confirm the `Bbmaj7` bloom actually appears
2. confirm the upper voicing opens upward
3. then check width / return automation

### Problem: “I followed the voicings and it still feels flat.”
Fix order:
1. A/B your `Drop A` and break against the references at matched loudness
2. confirm the restrained `Bb` and bloomed `Bbmaj7` are actually different in your MIDI
3. verify the chord bed is not too quiet under the hook lane later

## What Must Be Captured For Later Lesson Conversion
- chord-bed patch screenshots
- restrained vs bloomed `Bb` MIDI screenshots
- one full `4`-bar drop chord screenshot
- one full break bloom screenshot
- chord bus chain screenshot
- width/send automation screenshot
- one checkpoint bounce of `drums + bass + chords`
