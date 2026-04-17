# UKG 140 OG Bounce Driver: Production Plan

## Goal
Take `ukg-140-og-bounce-driver` from a strong composition plan to a production-ready build spec for later Ableton execution.

This document is the technical companion to:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)

It focuses on:
- exact sound ownership
- production choices
- transition design
- mix/master scaffolding
- reference calibration

It is not the tutorial sequence. That lives in:
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)

## Current Status
### Composition-ready
- Yes

### Production-ready
- Not fully yet

Remaining blockers:
- `3` fallback-heavy synth choices
- `2` pairwise sound conflicts
- no audio-verification pass yet

Interpretation:
- the song architecture is effectively frozen
- the remaining work is exact sound selection, lane ownership, and execution

## Track Identity
- `140 BPM`
- `D minor`
- `144 bars`
- `~4.11 minutes`
- emotional target: `dark but hopeful`

Reference role split:
- `KETTAMA - It Gets Better`: pressure, weight, density
- `Interplanetary Criminal - Slow Burner`: swing, hat drag, phrase-end groove
- `Y U QT lane study 2`: rolling bass motion proxy until a direct SMTS track study exists
- `Sammy Virji - I Guess We're Not the Same`: hook clarity, harmonic readability

## Harmony Spec
### Progression
- `Dm9 -> Bb -> Fadd9 -> Cadd9`

### Why these chords
- `Dm9` gives darkness with more emotional color than plain `Dm`
- `Bb` is the hope chord, but its bloom is staged
- `Fadd9` and `Cadd9` keep forward motion and suspended lift without turning bright too early
- the emotional effect comes from staging the bloom, not from having every color tone exposed all the time

### Bb voicing states
- restrained `Bb` for `Intro / Drop A / Drop A Lift / Transition B`: `Bb2 F3 C4`
- bloomed `Bbmaj7` for `Break / Drop B`: `Bb2 F3 A3 C4`

### Voice-leading strategy
- preserve common tones where possible
- keep upper voices moving by short steps
- avoid bouncing every chord in root position in the chord register

Practical voice-leading rule:
- let `A` and/or `C` act as anchors where possible from `Dm9` into the restrained `Bb` state
- let top-voice motion step into `Fadd9` and `Cadd9`

### Chord delivery mode
- hybrid
- sustained emotional bed
- restrained rhythmic pulse / stab behavior in transitions and lifts

This means:
- not a pure pad track
- not a pure stab track

### Chord articulation by section
- `Intro A`: filtered wash hints only
- `Intro B`: tucked full progression, long enough to feel bed-like
- `Drop A`: one-bar-per-chord pulse over sustained emotional bed
- `Drop A Lift`: same harmony, slightly brighter pulse only
- `Break`: 2-bar stretched voicings, upward bloom
- `Transition B`: rhythmic pulse returns, but harmonic density stays restrained
- `Drop B`: same loop, obvious bloom
- `Drop B Lift`: same harmony, more width and top release, not reharmonization

## Bass Spec
### Bass architecture
- bass is the `floor`, not the main hook
- stable sub layer + moving harmonic layer
- rolling motion is `rhythmic-primary`, `tonal-secondary`

### Sub patch
- engine: `Serum 2`
- source: `Sub oscillator` on sine
- mono: `on`
- glide: only tiny if needed, `~5–20ms`
- amp envelope:
  - attack `0`
  - sustain `full`
  - release `~40–60ms`
- patch-level processing:
  - keep mostly clean
  - extra grit should happen on the bass bus or harmonic layer, not the raw sub

### Mid-bass / harmonic layer patch
- engine: `Serum 2`
- source direction:
  - Osc A square-leaning body
  - Osc B saw or harmonic support
  - low blend, slight detune only
- filter:
  - low-pass
  - light drive
- role:
  - most motion and character
  - does not become a second hook

### Sub / mid crossover
- keep most sub authority below roughly `120–150 Hz`
- keep most character motion above that

### Gate / note-length behavior
- on-grid body notes: roughly `50–70%` gate feel
- phrase-end releases: shorter and more punctuating, roughly `15–35%` gate feel
- note-length variation is one of the main roll mechanisms

### Sidechain behavior
- kick -> sub: strongest duck
  - fast attack
  - release matched to kick tail, roughly `90–120ms`
- kick -> mid-bass:
  - slightly lighter than sub
  - still clearly breathing

### Glide behavior
- default: hard-switch or ultra-short glide
- do not use obvious portamento as a musical effect

### Bass root path
- `D2 -> Bb1 -> F2 -> C2`

### Phrase-end vocabulary
- `Dm9`: `D2 D3 A2 C3`
- `Bb`: `Bb1 Bb2 F2 D2`
- `Fadd9`: `F2 F3 C3 G3`
- `Cadd9`: `C2 C3 G2 D3`

### Non-negotiable rule
- no ornament is allowed if it implies a new chord

## Drum Spec
### Kick
- tune body to `D`
- layer:
  - body/sub layer
  - short click/attack layer
- tail: short, roughly `90–120ms`
- role: heavy, physical, not harsh

### Clap
- lands on `2` and `4`
- default is clap-first
- add tighter snare/rim support only when the section needs extra presence

### Hats
- closed/offbeat hats provide stable scaffold
- ghost hats create the real swing
- ghost hats should be intentionally late by roughly `5–15 ticks`
- no single global swing preset

### Open hats
- restrained tease in `Intro B`
- full offbeat / phrase-end role in drops
- use them to mark section lift and phrase endings, not to flood every offbeat equally

### Shakers
- own a lot of the `5–8 kHz` lift energy
- important in lifts and transitions

### MIDI policy
- kick and clap: on-grid
- ghost hats: intentionally late
- closed hats / shakers: lightly humanized

Suggested velocity behavior:
- kick: strong and consistent
- clap: strong with small variation
- closed hats: real variation
- ghost hats: felt more than heard
- open hats: louder than ghosts but not dominating
- shakers: gradually lift toward phrase boundaries

### Section micro-architecture
- bars `1–4`: establish groove
- bars `5–8`: deepen pocket
- bars `9–12`: slightly increase motion
- bars `13–16`: transition pressure

### Drum overlays
- `drum_phrase_end_fill_1bar`
- `drum_section_riser_1bar`
- `drum_pre_drop_cut_1bar`

## Hook and Answer Spec
### Hook notes
- `Drop A`: `A4 C5 D5`
- `Drop B`: `A4 C5 D5 F5`

### Exact rhythmic identity
- hook enters late, not on the kick
- in the current plan the core cell lands around:
  - late in beat `3`
  - on beat `4`
  - late in beat `4`

### Repetition pattern
- `Drop A`: phrase-end only, not every bar
- `Drop A Lift`: same hook language, no new melodic reveal
- `Drop B`: half density when the answer enters
- `Drop B Lift`: strongest answer behavior, but still alternating

### Hook synth
- engine: `Serum 2`
- family: `FM-organ / woody garage stab`
- not:
  - supersaw
  - vocal placeholder

Envelope direction:
- fast attack
- medium-short decay
- low sustain
- short release

Processing direction:
- light saturation
- controlled compression
- short plate reverb send
- filtered delay throws only where useful
- high-pass enough to stay out of the bass lane

### Answer synth
- same family as hook
- shorter envelope
- slightly dirtier tone
- phrase-end only

### Register relationship
- hook should sit above the core chord bed enough to read clearly
- answer should feel related, not like a different instrument family

## Top-End, Air, and Stereo
### Air source
- use an atonal noise-based air bed
- keep it harmonically safe
- most audible in the break
- present quietly almost throughout

### Presence owner
- combination of:
  - open hats
  - top loop bite
  - hook attack
  - answer edge

### EQ ownership direction
- `30–90 Hz`: sub / kick
- `120–300 Hz`: carefully split between bass character and chord warmth
- `300 Hz–2 kHz`: emotion + hook readability
- `2–6 kHz`: presence
- `8 kHz+`: air

### Stereo map
- kick: mono / center
- sub: mono / center
- mid-bass: mono to narrow stereo above crossover
- hook: mostly center with stereo support from returns
- answer: a little wider than hook via returns
- chords: wide stereo
- air: widest layer
- loops/tops: stereo but controlled

## Arrangement and Transition Spec
### Growth rule by section
- `Drop A`: force, restraint
- `Drop A Lift`: top-end density and pocket only
- `Break`: upward harmonic bloom and air
- `Transition B`: rhythmic re-engagement
- `Drop B`: harmonic bloom + answer conversation
- `Drop B Lift`: widest, most released top end

### Transition inventory
#### 32 -> 33
- intro to first drop
- use:
  - section riser
  - filtered bass teaser opening
  - drum-bus HP clearing off

#### 64 -> 65
- first lift to break
- use:
  - phrase-end fill
  - drum thinning
  - widening reverb / chord bloom

#### 80 -> 81
- break to transition_b
- use:
  - re-entry drum switch
  - tighter chord pulse
  - filtered bass re-implication

#### 96 -> 97
- transition_b to Drop B
- use:
  - pre-drop cut
  - filtered hook pickup
  - full body return

#### 128 -> 129
- Drop B Lift to outro
- remove top pressure first
- keep the air whisper

## Automation Spec
- drum-bus high-pass:
  - filtered intros and transitions
  - fully open in main drops
- bass-mid filter breathing:
  - strongest at phrase ends
  - calmer in the middle of phrases
- chord width / brightness:
  - tucked in Drop A
  - widened in break
  - bloomed in Drop B
- hook send levels:
  - mostly readable and dry
  - selected phrase-end throws only
- air-bed level:
  - constant but low
  - loudest in break
- transition FX:
  - used intentionally at named boundaries, not everywhere

## Mix and Master Spec
### Gain staging
- individual tracks generally around `-12` to `-8 dBFS` peak before major bus work
- buses around `-8` to `-6 dBFS` peak
- premaster around `-6 dBFS` peak headroom

### Bus structure
- Drum bus
- Bass bus
- Music bus
- FX / returns
- Premaster

### Sidechain network
- kick -> sub: deepest duck
- kick -> bass mid: lighter duck
- kick -> chords: gentle duck
- kick -> air: very light duck

### Parallel
- drum parallel for density
- optional bass parallel for extra constant attitude
- parallel must not flatten the groove

### Saturation
- kick: subtle body
- bass mid: main saturation character
- chords: warmth only
- hook/answer: identity tone, not fuzz

### Reverb
- short room / ambience if drums need glue
- short plate for hook/answer
- longer hall/plate for chords + air, filtered

### Delay
- filtered delays as throws
- avoid constant wash
- hook can take short rhythmic delay if it strengthens identity

### Master bus
- Utility / trim
- gentle glue comp if needed
- subtle saturation / soft clip
- limiter last

### Loudness direction
- do not chase final loudness early
- get translation right first

### Monitoring checks
- mono
- phone / small speaker
- car / everyday playback
- club-style low-end sanity if possible

## Reference Calibration
### Pressure
- `KETTAMA - It Gets Better`
- check:
  - kick weight
  - low-end size
  - density before brightness

### Groove pocket
- `Interplanetary Criminal - Slow Burner`
- check:
  - ghost-hat drag
  - loop bounce
  - phrase-end pocket

### Bass roll
- `Y U QT lane study 2`
- check:
  - rhythmic-first rolling motion
  - stable sub underneath
  - how much movement the mid layer carries

### Hook and harmony readability
- `Sammy Virji - I Guess We're Not the Same`
- check:
  - low-note-count hook clarity
  - harmonic readability in a club mix

## Originality Tests
- if you hum your hook next to a source hook, it should diverge in contour or rhythm within the first `4` notes
- if a bass phrase feels too source-like, change gate length, phrase-end note choice, or register emphasis
- if a transition feels recognizable, keep the role and change the timing or FX combination

## Production-Ready Checklist
- choose exact final synths instead of fallback-heavy placeholders
- resolve pairwise sound conflicts before mixing around them
- ensure no `16`-bar section loops identically
- verify `Drop A Lift` adds no new harmonic information
- verify `Drop B` answer stays phrase-end only
- verify the break ghost is textural, not a hidden phrase
