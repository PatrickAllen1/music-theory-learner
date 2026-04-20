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
- `vocal-sample-source`: not selected yet
  - reason: the track identity is now vocal-sample-led; the final vocal must be found, cleared, tested against the key, and placed intentionally

Named sound conflicts:
- `bass-foundation` vs `vocal-sample-source`
  - issue: a low or muddy vocal chop can mask the rolling bass if the sample is not filtered / chosen carefully
- `chord-bed` vs `vocal-sample-source`
  - issue: a melodic vocal can imply notes that fight the staged chord bloom

## Core Thesis
Build a `140 BPM` `D minor` modern UKG / speed-garage record whose center is:
- `Kettama`-level low-end pressure and density
- `Interplanetary Criminal` swing, bounce, and phrase pocket
- `Soul Mass Transit System` rolling bass-floor behavior
- `Sammy Virji / Y U QT` harmonic clarity and hook readability

The record should move from:
- `Drop A`: restrained, physical, dark
- `Break / re-entry build / Drop B`: wider, more hopeful, more open

It should get bigger through:
- substitution
- harmonic bloom
- top-end release
- vocal sample reveal / phrase-end human punctuation

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
- `Y U QT - U Belong 2 Me (4x4 Mix)`

Verification note:
- public track names were checked against public catalog / press results on `2026-04-17`

Local sound/chain anchors are separate:
- ALS anchor profiles later in this document are for sound-function inspiration only
- they are not the same thing as the creative references above

## Anti-Goals
- no OG speed-garage bass-hook writing
- no second melodic bass voice in `Drop B`
- no over-clipped techno-hard drum attitude
- no forced synth hook/answer replacing the vocal lane
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

### Vocal sample lane architecture
- The old synth hook/answer idea is removed from the core plan.
- The identity lane is now a vocal sample lane.
- The track should teach sample search, auditioning, phrase placement, chopping, and vocal staging rather than forcing a beepy organ hook.
- Until a final sample is found, use muted guide clips or empty space rather than a substitute synth hook.

Vocal lane states:
- `Intro A`: no vocal
- `Intro B`: filtered teaser near the end only
- `Drop A`: no main vocal; optional quiet teaser only
- `Drop A Lift`: same restraint as `Drop A`
- `Break`: readable lyric phrase or vocal texture is allowed, but it should feel suspended and spacious
- `Re-entry Build`: late filtered pickup hints only
- `Drop B`: first clear hook phrase / title-chop identity
- `Drop B Lift`: strongest vocal presence, with the most complete phrase if it still leaves groove room
- `Outro`: no new vocal idea

Why:
- the vocal becomes a designed presence across the whole arrangement
- the strongest hook reveal is saved for `Drop B`
- the break can carry emotional lyric content before the drop payoff
- earlier sections create anticipation without making the song feel empty

### Top-end section map
- `Intro A`: quiet air only
- `Intro B`: filtered tease of open-hat / presence layer
- `Drop A`: first full opening
- `Break`: presence steps back, air + widened chords breathe
- `Drop B`: return to first-drop presence level
- `Drop B Lift`: strongest top-end release
- `Outro`: whisper of air remains

### Drop B vocal rule
- `Vocal Main` appears first at phrase-defining moments.
- `Vocal Throw` is phrase-end only.
- The main vocal and throw should not crowd the same phrase ending.
- If the vocal is not found yet, preserve the empty lane rather than adding a synth replacement.

### Break chord widening
- “Stretch the chords” means:
  - longer notes
  - upward voicing spread
- upper chord tones and reverb tail should do more work than low mids

### Re-entry Build design (`81–96`)
- Use the extra `16` bars as a dedicated re-entry build section, not as the only “transition” in the song.
- Every section handoff is still a transition:
  - `Intro A -> Intro B`
  - `Intro B -> Drop A`
  - `Drop A -> Drop A Lift`
  - `Drop A Lift -> Break`
  - `Break -> Re-entry Build`
  - `Re-entry Build -> Drop B`
  - `Drop B -> Drop B Lift`
  - `Drop B Lift -> Outro`
- The reason this block gets its own section name is that it has its own drum language, bass teaser, chord pulse, and hook pickup behavior.
- It should have:
  - different re-entry drums
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
- `Dm9`: `D3 F3 A3 C4 E4`
- `Bb` restrained state for `Intro / Drop A / Drop A Lift / Re-entry Build`: `Bb2 F3 C4`
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

Chord duality mechanism:
- keep one main chord-bed instrument and create the section differences with MIDI length, velocity, width, and send behavior before introducing any second chord layer

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
- `Re-entry Build`: filtered teaser with more urgent phrase-end pull
- `Drop B`: same rolling shape, but phrase-end lift can touch color tones
- `Drop B Lift`: strongest phrase-end release bars of the track
- `Outro`: reduce to root implication and closure

## Vocal Sample Plan
### Vocal thesis
- sample-led identity lane
- human phrase / chop / ad-lib preferred over synth hook
- vocal is part of the whole arrangement, but not active constantly
- earlier sections use absence, filtering, texture, or short teasers
- `Break` can hold a readable lyric phrase if the phrase is spacious and not drum-looped
- `Drop B` gets the first real hook phrase / title-chop reveal

### First-pass placements
- `Intro B`: optional filtered teaser at `29.3.4` and `30.3.4`
- `Drop A`: optional quiet teaser at `40.3.4` and `48.3.4`
- `Drop A Lift`: optional quiet teaser at `56.3.4` and `64.3.4`
- `Break`: lyric phrase or texture at `72.1.1` or `76.4.4`
- `Re-entry Build`: optional pickups at `93.3.4`, `94.3.4`, and `96.4.4`
- `Drop B`: main hook phrase / title chop at `100.3.4` and `108.3.4`
- `Drop B`: vocal throw at `104.4.4` and `112.4.4`
- `Drop B Lift`: longer hook phrase can appear at `116.3.4` and `124.3.4`
- `Drop B Lift`: vocal throw at `120.4.4` and `128.4.4`

### Sample search criteria
- euphoric phrase, one-shot, breath, ad-lib, or chop
- dry enough to place in the mix
- harmonically safe against `D minor`
- does not fight the `Bbmaj7` bloom
- does not contain printed drums / bass / wide reverb that cannot be removed

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
- keep the tail short inside `90–120 ms`
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
- `Bars 9–12`: raise existing shaker velocities by `+6` and add selected `& of 2` open-hat energy where the section needs lift
- `Bars 13–16`: phrase-end fill, riser, or short groove drop into the next section

### Drum transition toolkit
- phrase-end fills at selected `8` / `16` bar boundaries
- section risers before major returns
- pre-drop cut bars before the biggest landings
- drum-bus high-pass filter moves during intros and transitions
- increased ghost-hat density in the last `4` bars of big sections

### Boundary transition jobs
Every section handoff has a transition job, even when there is no dedicated `16`-bar section for it.

Minor handoffs:
- `16 -> 17`
  - filtered reveal into `Intro B`
  - no giant riser
- `48 -> 49`
  - phrase-end drum pressure into `Drop A Lift`
  - more top pressure, no new harmonic reveal
- `112 -> 113`
  - phrase-end drum pressure into `Drop B Lift`
  - more release, no new section identity

Major handoffs:
- `32 -> 33`
  - intro-to-drop landing
  - section riser
  - drum-bus HP opening off
  - bass teaser opening into full body
- `64 -> 65`
  - lift-to-break release
  - phrase-end fill
  - drum thinning
  - upward chord bloom
- `80 -> 81`
  - break into `Re-entry Build`
  - different re-entry drums
  - tighter chord pulse
  - filtered bass re-implication
- `96 -> 97`
  - `Re-entry Build` into `Drop B`
  - pre-drop cut
  - filtered vocal pickup resolving
  - full body return
- `128 -> 129`
  - drop-lift into outro
  - remove top pressure first
  - keep the air whisper

## Frequency and Top-End Plan
### Bands
- `30–90 Hz`: bass-foundation owns center
- `120–300 Hz`: bass character and harmonic warmth, carefully carved
- `300 Hz–2 kHz`: chord emotion + vocal intelligibility
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
- sharper re-entry hats in the `Re-entry Build`
- vocal attack + phrase-end throw edge

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
- no main vocal yet; optional tiny vocal atmosphere only if the sample has usable air

Arrangement assignment:
- drums: `drum_intro_core_2bar`
- chords: `chord_intro_hint_4bar`

### 17–32: Intro B
- full progression appears but tucked
- bass teaser starts
- top end is only teased
- vocal uses only a filtered pickup fragment near the end

Arrangement assignment:
- drums: `drum_intro_b_tease_2bar`
- bass: `bass_intro_b_tease_4bar`
- chords: `chord_intro_full_4bar`
- vocal: `vocal_intro_b_teaser`

### 33–48: Drop A
- full rolling bass foundation
- vocal mostly withheld; optional quiet teaser only
- no exposed harmonic bloom yet
- bass owns the section

Arrangement assignment:
- drums: `drum_drop_core_2bar`
- bass: `bass_drop_a_core_4bar`
- chords: `chord_drop_core_4bar`
- vocal: `vocal_drop_a_teaser_optional`

### 49–64: Drop A Lift
- bigger by top-end density and tighter pocket only
- no new bass harmonic content
- no main vocal reveal
- same harmonic content as `Drop A`, only brighter pulse / dynamics
- chord variant here must not add new harmonic color; it only tightens rhythm / dynamics

Arrangement assignment:
- drums: `drum_drop_lift_2bar`
- bass: `bass_drop_a_lift_4bar`
- chords: `chord_drop_a_lift_4bar`
- vocal: `vocal_drop_a_lift_teaser_optional`

### 65–80: Break
- stretched chords
- upward voicing bloom
- drums thinned
- air most audible here
- center lane should feel like intentional vocal space
- any vocal here should be a suspended break phrase or texture, not the final drop hook phrase

Arrangement assignment:
- drums: `drum_break_sparse_2bar`
- bass: `bass_break_sparse_4bar`
- chords: `chord_break_stretch_8bar`
- vocal: `vocal_break_texture_optional`

### 81–96: Re-entry Build
- dedicated re-entry switch
- different re-entry drums
- filtered bass return
- tighter chord pulse
- filtered vocal pickup only in the late pickup window:
  - first pickup at `93.3.4`
  - second pickup at `94.3.4`
  - optional final pickup at `96.4.4`
- chord state should stay more restrained than `Drop B`, even while the rhythm re-engages
- use the restrained `Bb2 F3 C4` state here, not the bloomed `Bbmaj7` state

Arrangement assignment:
- drums: `drum_reentry_build_switch_2bar`
- bass: `bass_reentry_build_tease_4bar`
- chords: `chord_reentry_build_pulse_4bar`
- vocal: `vocal_reentry_build_pickup`

### 97–112: Drop B
- harmonic bloom arrives
- first real main vocal sample identity arrives
- phrase-end vocal throw can answer the main chop
- bigger by color, human phrase, and punctuation, not low-end stacking

Arrangement assignment:
- drums: `drum_drop_core_2bar`
- bass: `bass_drop_b_core_4bar`
- chords: `chord_drop_b_bloom_4bar`
- vocal main: `vocal_drop_b_main`
- vocal throw: `vocal_drop_b_throw`

### 113–128: Drop B Lift
- strongest energy point
- tops and widened chords carry most of the lift
- vocal main and throw can become more present, but should not become a nonstop loop

Arrangement assignment:
- drums: `drum_drop_lift_2bar`
- bass: `bass_drop_b_lift_4bar`
- chords: `chord_drop_b_bloom_4bar`
- vocal main: `vocal_drop_b_lift_main`
- vocal throw: `vocal_drop_b_lift_throw`

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
- `drum_reentry_build_switch_2bar`: fresh re-entry drum language
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
- `bass_reentry_build_tease_4bar`: filtered re-entry pull
- `bass_drop_b_core_4bar`: bloom-phase rolling floor
- `bass_drop_b_lift_4bar`: strongest release bars

### Chords
- `chord_intro_hint_4bar`
- `chord_intro_full_4bar`
- `chord_drop_core_4bar`
- `chord_drop_a_lift_4bar`
- `chord_break_stretch_8bar`
- `chord_reentry_build_pulse_4bar`
- `chord_drop_b_bloom_4bar`

### Vocal sample lane
- `vocal_intro_b_teaser`
- `vocal_drop_a_teaser_optional`
- `vocal_drop_a_lift_teaser_optional`
- `vocal_break_texture_optional`
- `vocal_reentry_build_pickup`
- `vocal_drop_b_main`
- `vocal_drop_b_throw`
- `vocal_drop_b_lift_main`
- `vocal_drop_b_lift_throw`

## Sample Strategy
- `v1` is vocal-sample-led, but can be arranged with muted placeholders until the final sample is found
- the sample must be found, cleared, and tested before final release
- keep the sample narrow enough to leave the bass/chord architecture intact
- phrase-end and short-chop behavior is preferred over long topline behavior
- avoid a long dominant vocal loop that rewrites the chord progression
  - air bed
  - chord spread
  - arrangement discipline
  should already fill the role of “completeness”

## Originality Guardrails
- ALS clips and transcript spans are mechanism evidence only
- do not lift:
  - full note paths
  - bar-length phrase shapes
  - exact vocal chop contours
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
- `chord-bed`: `bl3ss-camrinwatsin-kisses:pad-1:i7`
- `vocal-space support`: reference tracks and future vocal sample searches, not the removed organ hook

These are inspiration anchors for chain/function, not copying targets.

## Energy Curve
- `Intro A`: `2/10`
- `Intro B`: `3/10`
- `Drop A`: `7/10`
- `Drop A Lift`: `8/10`
- `Break`: `4/10`
- `Re-entry Build`: `6/10`
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

### 4. Vocal sample search and placement logic
- find and test a real vocal sample
- preserve vocal space across intro, drops, break, and re-entry
- save the first real main vocal identity for `Drop B`

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
- when the `Drop B` vocal arrives, it must feel earned by earlier restraint
- the break must widen upward, not only sustain longer
- if a section loops identically for all `16` bars, it is not finished
- the top-end map must stay intact across sections
- if a phrase sounds too close to a source, change contour/register/rhythm immediately
- the vocal sample lane must remain harmonically safe

## Reviewer Focus
1. Does the bass read as a proper modern rolling UKG floor?
2. Does `Drop A` stay restrained enough for `Drop B` to bloom?
3. Is the vocal sample lane designed across the whole song without revealing the main phrase too early?
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
- capture final MIDI for bass and chords, plus exact vocal audio placements, so the guided lesson can point to exact decisions
- keep the composition pass and MIDI plan beside the Ableton session; they are the authority, not late-session instinct
- the vocal sample is now part of the intended version, not a future re-version add-on
