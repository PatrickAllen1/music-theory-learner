# UKG 140 OG Bounce Driver: Tutorial Part 6 — Arrangement Build

## Purpose
Teach the learner how to turn the finished lanes for `ukg-140-og-bounce-driver` into a full `144`-bar club arrangement that:
- grows by different mechanisms in different sections
- keeps `Drop A` restrained enough for `Drop B` to matter
- makes `Transition B` a real re-entry, not a second break
- feels designed rather than blocky

This part should convert the frozen architecture into exact section assembly, phrase planning, and energy control.

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
  - `81–96 Transition B`
  - `97–112 Drop B`
  - `113–128 Drop B Lift`
  - `129–144 Outro`
- all core lanes assigned by section:
  - drums
  - bass
  - chords
  - hook
  - answer
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
- learner can duplicate clips, create locators, and automate mutes or arrangement edits in Ableton

## What The Learner Should Understand Before Starting
Arrangement here is not:
- copy-pasting one 4-bar loop for 4 minutes
- muting and unmuting entire lanes with no phrase design
- making every section feel bigger by adding one more layer

Arrangement here is:
- section purpose
- phrase pressure
- selective removal
- earned returns

If every section uses the same growth move, the record will flatten out even if the sound design is good.

## Reference Axis
Primary A/B for this part:
- `Interplanetary Criminal - Slow Burner`
  - listen for how the section changes feel rhythmic and pocket-based, not just FX-based
- `KETTAMA - It Gets Better`
  - listen for how pressure is maintained even when the arrangement strips down

Secondary check:
- `Sammy Virji - I Guess We're Not the Same`
  - listen for how harmonic and hook information arrive in controlled stages

## Files / Assets Needed
- current project with:
  - working drums
  - bass
  - chords
  - hook
  - answer
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
- `81–96 Transition B`
- `97–112 Drop B`
- `113–128 Drop B Lift`
- `129–144 Outro`

Growth rule by section:
- `Drop A`: force and restraint
- `Drop A Lift`: top-end density and pocket only
- `Break`: upward harmonic bloom and air
- `Transition B`: rhythmic re-engagement
- `Drop B`: harmonic bloom plus answer conversation
- `Drop B Lift`: strongest release through alternation and top-end opening

## Step 1: Mark The Timeline
### Action
1. Create locators or timeline markers for all `9` sections.
2. Label each with both bar range and section name.
3. Add a short note in each locator if Ableton allows it:
   - e.g. `Drop A = force / restraint`

### Why
The arrangement needs a visible map before clips start flying around.

If the learner only arranges by ear with no timeline structure:
- the middle sections will drift
- `Transition B` will often disappear
- the outro will be too short or too empty

### Screenshot
- `arrangement-01-timeline-markers`

## Step 2: Lay In The Section Skeleton
### Action
Place the section-level clip families first, before micro-edits:

- `Intro A`
  - drums: `drum_intro_core_2bar`
  - chords: `chord_intro_hint_4bar`
- `Intro B`
  - drums: `drum_intro_b_tease_2bar`
  - bass: `bass_intro_b_tease_4bar`
  - chords: `chord_intro_full_4bar`
  - hook: `hook_intro_pickup_4bar`
- `Drop A`
  - drums: `drum_drop_core_2bar`
  - bass: `bass_drop_a_core_4bar`
  - chords: `chord_drop_core_4bar`
  - hook: `hook_drop_a_phrase_4bar`
  - answer support: `answer_drop_a_tail_4bar`
- `Drop A Lift`
  - drums: `drum_drop_lift_2bar`
  - bass: `bass_drop_a_lift_4bar`
  - chords: `chord_drop_a_lift_4bar`
  - hook: `hook_drop_a_lift_4bar`
- `Break`
  - drums: `drum_break_sparse_2bar`
  - bass: `bass_break_sparse_4bar`
  - chords: `chord_break_stretch_8bar`
  - hook texture: `hook_break_ghost_4bar`
- `Transition B`
  - drums: `drum_transition_switch_2bar`
  - bass: `bass_transition_b_tease_4bar`
  - chords: `chord_transition_b_pulse_4bar`
  - hook: `hook_transition_b_pickup_4bar`
- `Drop B`
  - drums: `drum_drop_core_2bar`
  - bass: `bass_drop_b_core_4bar`
  - chords: `chord_drop_b_bloom_4bar`
  - hook: `hook_drop_b_phrase_4bar`
  - answer: `answer_drop_b_conversation_4bar`
- `Drop B Lift`
  - drums: `drum_drop_lift_2bar`
  - bass: `bass_drop_b_lift_4bar`
  - chords: `chord_drop_b_bloom_4bar`
  - hook: `hook_drop_b_lift_4bar`
  - answer: `answer_drop_b_lift_4bar`
- `Outro`
  - drums: `drum_outro_strip_2bar`
  - bass: `bass_break_sparse_4bar`
  - chords: `chord_intro_hint_4bar`

### Why
This gets the whole song on the page fast.

You want to hear the architecture first, before spending an hour polishing one transition.

### Screenshot
- `arrangement-02-section-skeleton`

### Visual Requirement
- show the whole song on screen if possible
- if not, show `Intro A` through `Break`, then `Transition B` through `Outro`

## Step 3: Shape Intro A And Intro B
### Action
`Intro A`:
- keep the groove filtered and spare
- no full bass language yet
- let the air layer quietly establish ceiling

`Intro B`:
- bring in the full progression in a tucked way
- add the bass teaser:
  - held root for the first two beats
  - one short octave hint every second bar
- let the top-end tease open slightly
- keep the hook as a filtered pickup only, not a full phrase

### Why
The first `32` bars need to feel like:
- something is coming
- the low-end world already exists
- the drop is not already here

### Rule
- if `Intro B` already feels like a drop with filters on it, too much has been revealed

### Screenshot Set
- `arrangement-03-intro-a`
- `arrangement-04-intro-b`

## Step 4: Build Drop A
### Action
For `33–48`:
- let the full rolling bass foundation enter
- let the hook appear only as restrained phrase-end punctuation
- keep the `Bb` chord in its restrained state
- keep the answer lane only as tail/support, not a full new voice
- open the top end to its first full state

### Why
`Drop A` is the force section.

It needs to hit physically while still leaving:
- harmonic bloom
- full answer behavior
- widest top release

for later.

### Rule
- if `Drop A` already sounds emotionally open, `Drop B` will have nothing new to say

### Screenshot
- `arrangement-05-drop-a`

## Step 5: Build Drop A Lift Without Leaking Bloom
### Action
For `49–64`:
- keep the same harmonic content as `Drop A`
- do not expose new `Bbmaj7` bloom
- do not add new hook notes
- make the section bigger through:
  - denser ghost-hat / shaker pressure
  - slightly more open top end
  - stronger phrase-end momentum
  - bass tone / feel, not bass reharmonization

### Why
This is the section most likely to cheat.

If the learner reaches for:
- new chord color
- a more melodic bassline
- an extra hook note

they are stealing from `Break` and `Drop B`.

### Mechanical checks
- compare `Drop A` and `Drop A Lift` side by side
- if the note content changed meaningfully, fix that before changing mix or FX

### Screenshot
- `arrangement-06-drop-a-lift`

## Step 6: Build The Break
### Action
For `65–80`:
- thin the drums
- stretch the chords
- switch to the bloomed `Bbmaj7` state
- let upward voicing and air become obvious
- keep the bass sparse:
  - root reminders only
- keep any hook ghost as texture, not a real phrase

### Why
The break should feel like the record opening upward, not like it ran out of energy.

This is where the hope becomes audible.

### Rule
- if the break feels empty instead of suspended, the air/chord bloom is too weak
- if it feels like a new song, the harmony drifted too far

### Screenshot
- `arrangement-07-break`

## Step 7: Build Transition B As A Re-Entry
### Action
For `81–96`:
- change the drum language so the re-entry feels fresh
- bring back the bass as a filtered implication, not full body yet
- pulse the chords rhythmically
- return to the restrained `Bb2 F3 C4` state
- let the filtered hook pickup appear only near the end

### Why
`Transition B` exists so `Drop B` feels earned.

It should feel like:
- rhythm waking back up
- tension rebuilding
- the low-end world approaching

It should not feel like:
- another break
- or `Drop B` arriving early

### Rule
- if the harmonic bloom is already obvious here, the section is too open

### Screenshot
- `arrangement-08-transition-b`

## Step 8: Build Drop B Through Substitution
### Action
For `97–112`:
- bring back full bass body
- reopen the harmonic bloom
- let the hook drop to half density
- introduce the answer at phrase ends only
- keep the section bigger by:
  - color
  - dialogue
  - restored body

not by another low-end layer.

### Why
This is the emotional payoff section.

It should feel clearly bigger than `Drop A`, but still disciplined.

### Mechanical placement
- first pass:
  - hook owns bars `4` and `12`
  - answer owns bars `8` and `16`
- keep that alternation visible in the arrangement before refining smaller variations

### Screenshot
- `arrangement-09-drop-b`

## Step 9: Build Drop B Lift And Outro
### Action
`Drop B Lift` (`113–128`):
- keep the same harmonic world as `Drop B`
- let tops and widened chords carry more of the release
- keep hook and answer alternating by phrase
- allow the greatest phrase density here without turning the section into clutter

`Outro` (`129–144`):
- remove the top pressure first
- keep a DJ-safe groove identity
- leave a whisper of air
- reduce harmonic and hook activity before stripping the kick/bass spine

### Why
The lift is the final release.
The outro is the controlled comedown.

Neither section should feel accidental.

### Screenshot Set
- `arrangement-10-drop-b-lift`
- `arrangement-11-outro`

## Step 10: Add Phrase-Level Architecture Inside Each Section
### Action
Inside each `16`-bar section, assign jobs to four-bar blocks:
- `Bars 1–4`: establish
- `Bars 5–8`: deepen
- `Bars 9–12`: increase motion
- `Bars 13–16`: push toward next boundary

Practical examples:
- in `Drop A`, the hook may first appear clearly in the last `4` bars
- in `Break`, the widest chord/air state may arrive after the first `4` bars, not immediately
- in `Transition B`, the hook pickup should stay later in the section, not at bar `81`
- in `Drop B`, the answer should not speak every phrase

### Why
Section labels alone are not enough.

This is what keeps the arrangement from sounding like copy-pasted blocks.

### Screenshot
- `arrangement-12-phrase-architecture`

### Visual Requirement
- show one full `16`-bar drop section
- annotate what changes at bars `5`, `9`, and `13`

## Step 11: Check The Energy Curve
### Action
Bounce the full rough arrangement and compare it to the planned energy staircase:
- `Intro A`: `2/10`
- `Intro B`: `3/10`
- `Drop A`: `7/10`
- `Drop A Lift`: `8/10`
- `Break`: `4/10`
- `Transition B`: `6/10`
- `Drop B`: `8/10`
- `Drop B Lift`: `9/10`
- `Outro`: `3/10`

### Why
This is the easiest way to catch leaks:
- if `Break` is too high, bloom leaked early
- if `Transition B` is too low, it feels like a second break
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
- `KETTAMA - It Gets Better`
  - listen for sustained pressure across stripped and full sections
- `Sammy Virji - I Guess We're Not the Same`
  - listen for how hook and harmonic information arrive in stages

### What To Listen For
- does `Drop A` hit hard enough without spending bloom?
- does `Transition B` feel like a re-entry and not a second break?
- does `Drop B` feel bigger because of substitution and bloom, not pile-up?
- does the outro still feel mixable?

### Expected Answer
- the second half should feel earned, not just louder
- every section should have a different reason for being bigger or smaller
- the arrangement should sound designed even before the final mix pass

## Troubleshooting
### Problem: “The arrangement feels blocky.”
Fix order:
1. add phrase-level change inside the section
2. improve removal/addition timing
3. only then add a new transition effect

### Problem: “Transition B feels like another break.”
Fix order:
1. restore more rhythmic motion
2. reduce harmonic openness
3. push the hook pickup later

### Problem: “Drop B doesn’t feel bigger than Drop A.”
Fix order:
1. check whether bloom leaked in `Drop A Lift`
2. thin the hook to half density
3. make the answer phrase-end only
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
