# UKG 140 OG Bounce Driver: Full Song Plan

## Purpose
- Package the full song direction for `ukg-140-og-bounce-driver` into one reviewer-facing plan.
- Freeze the current musical decisions before later Ableton execution and lesson authoring.
- Keep the process model-led and design-led, with scripts acting as guardrails rather than the composition brain.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)

## Track Overview
- `Brief ID`: `ukg-140-og-bounce-driver`
- `Tempo`: `140 BPM`
- `Key`: `D minor`
- `Length`: `144 bars`
- `Estimated runtime`: `~4.11 minutes`
- `Emotional target`: `dark`, `hopeful`
- `Current readiness`: `needs_work`

Current unresolved issues:
- `3` fallback-heavy synth selections
- `2` pairwise synth conflicts
- still partially param-driven until later audio verification

These are now production-readiness issues, not composition-architecture issues. The remaining work is exact sound ownership, low-mid separation, and resolving fallback sound choices before the later Ableton build.

Named production blockers:
- `chord-bed`: `bl3ss-camrinwatsin-kisses:pad-1:i7`
  - reason: selected under `mix_only` fallback, no actionable mutation suggestions yet
- `hook-response`: `interplanetary-criminal-slow-burner:organ:i4`
  - reason: selected under `mix_only` fallback, involved in `1` remaining pairwise conflict
- `og-reese-answer`: `bl3ss-camrinwatsin-kisses:organ-bass:i1`
  - reason: selected under `mix_only` fallback, involved in `2` remaining pairwise conflicts, no actionable mutation suggestions yet

Named sound conflicts:
- `bass-foundation` vs `og-reese-answer`
  - issue: both read as `low_end_anchor`, so the low end may stack too heavily
- `hook-response` vs `og-reese-answer`
  - issue: both want the forward midrange position

## Core Thesis
Build a `140 BPM` `D minor` modern UKG / speed-garage record whose center is:
- `Kettama`-level low-end pressure and density
- `Interplanetary Criminal` swing, bounce, and phrase pocket
- `Soul Mass Transit System` rolling bass-floor behavior
- `Sammy Virji / Y U QT` harmonic clarity and hook readability

The record should move from:
- `Drop A`: restrained, physical, dark
- `Break / transition_b / Drop B`: wider, more hopeful, more open

It should get bigger through:
- substitution
- harmonic bloom
- top-end release
- phrase-end conversation

It should **not** get bigger through:
- stacking more and more layers
- adding a second bass voice
- revealing harmonic bloom too early

## Reference Role Split
- `Kettama`: low-end pressure, mix density, physicality
- `Interplanetary Criminal`: groove pocket, phrase-end movement, hat swing
- `Soul Mass Transit System`: rolling bass-floor architecture
- `Sammy Virji / Y U QT`: hook clarity, chord color, emotional readability

Creative references used for musical calibration:
- `KETTAMA - It Gets Better`
- `Interplanetary Criminal - Slow Burner`
- `Sammy Virji - I Guess We're Not the Same`
- `Y U QT - NRG`

Verification note:
- public track names were checked against public catalog / press results on `2026-04-17`

Local sound/chain anchors are separate:
- ALS anchor profiles later in this document are for sound-function inspiration only
- they are not the same thing as the creative references above

## Anti-Goals
- no OG speed-garage bass-hook writing
- no second melodic bass voice in `Drop B`
- no over-clipped techno-hard drum attitude
- no sample dependency for `v1`
- no direct lifting of full note paths, section logic, or hook contours from ALS/transcript sources
- no robotic “if this then that” arrangement feel

## Architectural Decisions
### Intro B bass gesture
- Hold a mono sub/root for the first two beats.
- Add one short envelope-opened octave hint every second bar.
- No pitch bend.
- No full release run yet.

Why:
- keeps the intro physically grounded
- gives the track an early bass teaser without spending the drop

### Rolling bass mechanism
- Stable clean sub underneath
- Moving harmonic layer above it
- Motion comes from:
  - note-length variation
  - internal rhythmic pulse
  - filter / saturation breathing
  - only small phrase-end pitch events

Why:
- modern UKG roll should feel alive inside the sustain
- a static held sub with FX on top is not enough

### Rolling bass proportion
- `rhythmic-primary`
- `tonal-secondary`

Meaning:
- rhythmic pulse should do most of the rolling work
- tonal movement should support the pulse, not replace it

### Drop B answer architecture
- No second melodic bass voice
- Recast the answer lane as a short warm organ / piano-family phrase-end stab above the sub

Why:
- keeps `Drop B` bigger by color and punctuation
- avoids turning it into `Drop A` plus more low-mid weight

### Break sample lane target
- Reserve the break center lane for a narrow future vocal/chop or phrase-end texture
- Safe range: roughly `A3–F5`
- Avoid long tonal samples that introduce new thirds outside the progression

### Hook voice identity
- Clipped organ-pluck / woody garage stab
- Late offbeat entry
- Enough transient bite to read through the drums
- Core rhythmic placement:
  - late in beat `3`
  - on beat `4`
  - late in beat `4`
- Drop B answer is:
  - same family
  - shorter
  - slightly dirtier

### Top-end section map
- `Intro A`: quiet air only
- `Intro B`: filtered tease of open-hat / presence layer
- `Drop A`: first full opening
- `Break`: presence steps back, air + widened chords breathe
- `Drop B`: return to first-drop presence level
- `Drop B Lift`: strongest top-end release
- `Outro`: whisper of air remains

### Drop B conversation rule
- Answer is phrase-end only
- Hook drops to half density in `Drop B`
- Hook and answer alternate rather than stack

### Break chord widening
- “Stretch the chords” means:
  - longer notes
  - upward voicing spread
- upper chord tones and reverb tail should do more work than low mids

### Transition B re-entry design
- Use the extra `16` bars as a dedicated re-entry switch
- It should have:
  - different transition drums
  - filtered bass teaser
  - rising phrase pressure
  - pulsing restrained chords that sit between break-width and Drop B bloom
- It should use the restrained `Bb` state: `Bb2 F3 C4`, not the bloomed `Bbmaj7` state
- It should **not** feel like:
  - just a longer break
  - or a delayed second drop

## Harmonic Plan
### Progression
- `Dm9 -> Bbmaj7 -> Fadd9 -> Cadd9`

### Root path
- `D -> Bb -> F -> C`

### Emotional jobs
- `Dm9`: dark center
- `Bbmaj7`: hopeful lift
- `Fadd9`: open forward motion
- `Cadd9`: suspended pre-return tension

### Voicing palette
- `Dm9`: `D3 A3 C4 E4 F4`
- `Bb` restrained state for `Intro / Drop A / Drop A Lift / Transition B`: `Bb2 F3 C4`
- `Bbmaj7` bloomed state for `Break / Drop B`: `Bb2 F3 A3 C4`
- `Fadd9`: `F2 C3 G3 A3`
- `Cadd9`: `C3 G3 D4 E4`

### Harmonic restraint rule
- `Drop A`: keep `Bb` triad/add9-led, no obvious major-7 bloom
- `Break / Drop B`: let the `Bbmaj7` color open up

### Voice-leading strategy
- preserve common tones where possible
- keep upper voices moving by short steps
- avoid bouncing every chord in root position in the chord register

Practical rule:
- let `A` and/or `C` anchor the handoff from `Dm9` into the restrained `Bb` state where possible
- let the top line move stepwise into `Fadd9` and `Cadd9`

### Chord delivery mode
- hybrid
- sustained emotional bed
- restrained rhythmic pulse / stab articulation in transitions and lifts

Meaning:
- not a pure pad track
- not a pure stab track

## Bass Plan
### Thesis
The bass is the `floor`, not the topline.

### Four-bar root path
- `D2 -> Bb1 -> F2 -> C2`

### Release-note vocabulary
- over `Dm9`: `D2 D3 A2 C3`
- over `Bbmaj7`: `Bb1 Bb2 F2 D2`
- over `Fadd9`: `F2 F3 C3 G3`
- over `Cadd9`: `C2 C3 G2 D3`

### Main rule
- No ornamental note is allowed if it implies a new chord.
- Save the strongest release gestures for phrase ends, not metronomic bar-2/bar-4 punctuation.

### Section behavior
- `Intro A`: no full bass line, only implication
- `Intro B`: held root plus occasional octave hint
- `Drop A`: full rolling floor, restrained phrase-end release
- `Drop A Lift`: same pitch vocabulary, bigger only by tone and feel
- `Break`: occasional root reminders only
- `Transition B`: filtered teaser with more urgent phrase-end pull
- `Drop B`: same rolling shape, but phrase-end lift can touch color tones
- `Drop B Lift`: strongest phrase-end release bars of the track
- `Outro`: reduce to root implication and closure

## Hook and Answer Plan
### Hook thesis
- small, memorable, late-offbeat identity lane
- carries the instrumental without becoming a full topline

### Hook cells
- `Drop A`: `A4 -> C5 -> D5`
- `Drop B`: `A4 -> C5 -> D5 -> F5`
- secondary answer cell: `G4 -> A4 -> C5`

### Rhythmic behavior
- stay off the kick
- enter:
  - late in beat `3`
  - on beat `4`
  - late in beat `4`
- phrase-end punctuation is the identity

### Drop B conversation
- answer is phrase-end only
- hook is half-density
- hook and answer alternate by phrase

### Timbral relationship
- hook = cleaner, slightly longer tail
- answer = shorter, slightly dirtier

## Drum Philosophy
- 4x4 body-forward kick core
- swingy tops
- loop bounce
- pressure from weight and density, not flattening

### Kick
- heavy
- tuned
- physical
- not harsh

Practical spec:
- tune the kick body to `D`
- layer a body/sub sample with a shorter click/attack layer
- keep the tail short, roughly `90–120ms`
- let the kick and bass breathe together instead of relying on extreme sidechain

### Tops
- ghost hats
- offbeat hats
- open-hat shimmer
- filtered loop motion
- subtle velocity / timing life

Practical groove spec:
- no single global swing preset
- kick and clap stay on-grid
- ghost hats are intentionally late by a small consistent amount
- open hats mark offbeats and phrase ends, not every possible space
- shakers carry a lot of the `5–8 kHz` lift energy

### Core rule
- never rewrite the kick pattern to create growth
- energy changes come from:
  - hat density
  - shaker brightness
  - loop support
  - phrase pressure

### Drum micro-architecture
- `Bars 1–4`: establish groove
- `Bars 5–8`: deepen the pocket with ghost-hat / loop life
- `Bars 9–12`: increase shaker / open-hat energy slightly
- `Bars 13–16`: phrase-end fill, riser, or short groove drop into the next section

### Drum transition toolkit
- phrase-end fills at selected `8` / `16` bar boundaries
- section risers before major returns
- pre-drop cut bars before the biggest landings
- drum-bus high-pass filter moves during intros and transitions
- increased ghost-hat density in the last `4` bars of big sections

## Frequency and Top-End Plan
### Bands
- `30–90 Hz`: bass-foundation owns center
- `120–300 Hz`: bass character and harmonic warmth, carefully carved
- `300 Hz–2 kHz`: chord emotion + hook identity
- `2–6 kHz`: presence owner
- `8 kHz+`: quiet constant air owner

### Movement rule
- intro filtered and narrowed
- first drop opens presence
- break breathes into air and upward chord spread
- `Drop B Lift` is biggest by width + top-end release, not more sub layers

### Support layers
#### Top presence
- filtered open-hat tease in `Intro B`
- full open-hat/presence lane in drops
- sharper transition hats in `transition_b`
- hook attack + phrase-end answer edge

#### Air bed
- quiet shimmer/noise bed from `Intro A` onward
- most audible in the break
- tucked back in the drops

## Full 144-Bar Arrangement Plan
### 1–16: Intro A
- filtered groove
- chord hint only
- no full bass line yet
- whisper of air already present
- one delayed / filtered hook pickup only near end

Arrangement assignment:
- drums: `drum_intro_core_2bar`
- chords: `chord_intro_hint_4bar`

### 17–32: Intro B
- full progression appears but tucked
- bass teaser starts
- top end is only teased
- hook uses only a filtered pickup fragment

Arrangement assignment:
- drums: `drum_intro_b_tease_2bar`
- bass: `bass_intro_b_tease_4bar`
- chords: `chord_intro_full_4bar`
- hook: `hook_intro_pickup_4bar`

### 33–48: Drop A
- full rolling bass foundation
- restrained hook punctuation
- no exposed harmonic bloom yet
- bass owns the section

Arrangement assignment:
- drums: `drum_drop_core_2bar`
- bass: `bass_drop_a_core_4bar`
- answer support: `answer_drop_a_tail_4bar`
- chords: `chord_drop_core_4bar`
- hook: `hook_drop_a_phrase_4bar`

### 49–64: Drop A Lift
- bigger by top-end density and tighter pocket only
- no new bass harmonic content
- no new hook melodic reveal
- same harmonic content as `Drop A`, only brighter pulse / dynamics
- chord variant here must not add new harmonic color; it only tightens rhythm / dynamics

Arrangement assignment:
- drums: `drum_drop_lift_2bar`
- bass: `bass_drop_a_lift_4bar`
- answer support: `answer_drop_a_tail_4bar`
- chords: `chord_drop_a_lift_4bar`
- hook: `hook_drop_a_lift_4bar`

### 65–80: Break
- stretched chords
- upward voicing bloom
- drums thinned
- air most audible here
- center lane should still feel intentional without a sample
- any hook ghost here should be texture, not a real phrase

Arrangement assignment:
- drums: `drum_break_sparse_2bar`
- bass: `bass_break_sparse_4bar`
- chords: `chord_break_stretch_8bar`
- hook: `hook_break_ghost_4bar`

### 81–96: Transition B
- dedicated re-entry switch
- different transition drums
- filtered bass return
- tighter chord pulse
- filtered hook pickup only near the end
- chord state should stay more restrained than `Drop B`, even while the rhythm re-engages
- use the restrained `Bb2 F3 C4` state here, not the bloomed `Bbmaj7` state

Arrangement assignment:
- drums: `drum_transition_switch_2bar`
- bass: `bass_transition_b_tease_4bar`
- chords: `chord_transition_b_pulse_4bar`
- hook: `hook_transition_b_pickup_4bar`

### 97–112: Drop B
- harmonic bloom arrives
- phrase-end warm answer arrives
- hook steps back to half density
- bigger by color and dialogue, not low-end stacking

Arrangement assignment:
- drums: `drum_drop_core_2bar`
- bass: `bass_drop_b_core_4bar`
- answer: `answer_drop_b_conversation_4bar`
- chords: `chord_drop_b_bloom_4bar`
- hook: `hook_drop_b_phrase_4bar`

### 113–128: Drop B Lift
- strongest energy point
- tops and widened chords carry most of the lift
- hook and answer alternate by phrase

Arrangement assignment:
- drums: `drum_drop_lift_2bar`
- bass: `bass_drop_b_lift_4bar`
- answer: `answer_drop_b_lift_4bar`
- chords: `chord_drop_b_bloom_4bar`
- hook: `hook_drop_b_lift_4bar`

### 129–144: Outro
- DJ-safe stripdown
- stable groove identity remains
- whisper of air remains
- no need to hard-seal the record shut

Arrangement assignment:
- drums: `drum_outro_strip_2bar`
- bass: `bass_break_sparse_4bar`
- chords: `chord_intro_hint_4bar`

## Part Writing Plan
### Drums
- `drum_intro_core_2bar`: kick/clap/off-hat skeleton
- `drum_intro_b_tease_2bar`: tease open-hat / presence lane
- `drum_drop_core_2bar`: main UKG drop groove with ghost hats
- `drum_drop_lift_2bar`: second-drop / lift density
- `drum_break_sparse_2bar`: thinner break support
- `drum_transition_switch_2bar`: fresh re-entry drum language
- `drum_outro_strip_2bar`: stable mix-out groove
- overlay tools:
  - `drum_phrase_end_fill_1bar`
  - `drum_section_riser_1bar`
  - `drum_pre_drop_cut_1bar`

### Bass
- `bass_intro_b_tease_4bar`: teaser only
- `bass_drop_a_core_4bar`: main rolling floor
- `bass_drop_a_lift_4bar`: same notes, more feel / tone
- `bass_break_sparse_4bar`: occasional root reminders
- `bass_transition_b_tease_4bar`: filtered re-entry pull
- `bass_drop_b_core_4bar`: bloom-phase rolling floor
- `bass_drop_b_lift_4bar`: strongest release bars

### Chords
- `chord_intro_hint_4bar`
- `chord_intro_full_4bar`
- `chord_drop_core_4bar`
- `chord_drop_a_lift_4bar`
- `chord_break_stretch_8bar`
- `chord_transition_b_pulse_4bar`
- `chord_drop_b_bloom_4bar`

### Hook / answer
- `hook_intro_pickup_4bar`
- `hook_drop_a_phrase_4bar`
- `hook_drop_a_lift_4bar`
- `hook_break_ghost_4bar`
- `hook_transition_b_pickup_4bar`
- `hook_drop_b_phrase_4bar`
- `hook_drop_b_lift_4bar`
- answer variants:
  - `answer_drop_a_tail_4bar`
  - `answer_drop_b_conversation_4bar`
  - `answer_drop_b_lift_4bar`

## Sample Strategy
- `v1` must work instrumentally
- a future sample version is a re-version, not a dependency
- if a sample appears later:
  - keep it narrow
  - phrase-end based
  - keep it roughly inside `A3–F5`
  - avoid a long dominant topline
- in the instrumental:
  - hook pocket
  - air bed
  - chord spread
  - arrangement discipline
  should already fill the role of “completeness”

## Originality Guardrails
- ALS clips and transcript spans are mechanism evidence only
- do not lift:
  - full note paths
  - bar-length phrase shapes
  - exact hook contours
- when a useful move comes from a source, change at least two of:
  - root path
  - interval contour
  - register
  - rhythmic placement
  - section placement
  - harmonic context
- if something starts sounding too close to `Yosemite`, `Raw`, or another source:
  - simplify
  - keep the function
  - push emotion via harmony, filtering, or arrangement instead

## Sound-Function Anchors (Inspiration Only)
- `bass-foundation`: `interplanetary-criminal-slow-burner:bass:i1`
- `hook/organ support`: `interplanetary-criminal-slow-burner:organ:i4`
- `chord-bed`: `bl3ss-camrinwatsin-kisses:pad-1:i7`
- `hook-support / answer support`: `bl3ss-camrinwatsin-kisses:organ-bass:i1`

These are inspiration anchors for chain/function, not copying targets.

## Energy Curve
- `Intro A`: `2/10`
- `Intro B`: `3/10`
- `Drop A`: `7/10`
- `Drop A Lift`: `8/10`
- `Break`: `4/10`
- `Transition B`: `6/10`
- `Drop B`: `8/10`
- `Drop B Lift`: `9/10`
- `Outro`: `5/10`

Rule:
- if a later section does not feel meaningfully more released than the one before it, the growth mechanism probably leaked early
- treat the numbers as architectural signals, not rigid meter readings
- the size of the jumps matters:
  - `3 -> 7` is the first big drop-entry jump
  - `7 -> 8` is controlled lift rather than a whole new section identity
  - `8 -> 4` is an intentional release into the break

## Studio Build Order
### 1. Kick, core groove, and air ceiling
- lock 4x4 body
- lock swingy tops
- add quiet air bed

### 2. Rolling bass floor
- build stable sub + moving harmonic layer
- confirm the roll feels rhythmic-primary

### 3. Chord bed and break bloom
- keep Drop A restrained
- save the harmonic bloom for break / Drop B

### 4. Hook identity and conversation logic
- warm organ-stab hook
- phrase-end answer in same family
- hook steps back in Drop B

### 5. Section writing and variant placement
- place exact variants section by section
- humanize within each variant family so sections do not loop identically
- ensure each section has a different growth mechanism

### 6. Returns, automation, and A/B
- build the return structure
- A/B each reference axis separately
- preserve the whisper of air in the outro

## Critical Checks
- resolve fallback-heavy synth choices and pairwise sound conflicts before the main Ableton build
- the bass roll must feel rhythmic-primary
- `Drop A Lift` must not reveal new harmonic information
- when the `Drop B` answer arrives, the hook must step back to half density
- the break must widen upward, not only sustain longer
- if a section loops identically for all `16` bars, it is not finished
- the top-end map must stay intact across sections
- if a phrase sounds too close to a source, change contour/register/rhythm immediately
- the break sample lane must remain harmonically safe

## Reviewer Focus
1. Does the bass read as a proper modern rolling UKG floor?
2. Does `Drop A` stay restrained enough for `Drop B` to bloom?
3. Is the hook / answer conversation strong enough for an instrumental-first version?
4. Does the track grow by substitution and opening instead of stacking?
5. Is the top-end map believable enough to avoid a closed-in mix?
6. Does the overall lane feel right:
   - `Kettama` pressure
   - `Interplanetary Criminal` bounce
   - `Soul Mass Transit System` bass roll
   - `Virji / Y U QT` harmonic intelligence
   - without sounding derivative?

## Later Handoff Notes
- when the track is built later, bounce each major section and compare it to the section targets before changing the arrangement
- capture final MIDI for bass, chords, hook, and answer so the guided lesson can point to exact note decisions
- keep the composition pass and MIDI plan beside the Ableton session; they are the authority, not late-session instinct
- if a future sample arrives, treat it as a re-version decision, not a reason to reopen the whole composition
