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

Current full-depth tutorial template:
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-part-02-groove.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-02-groove.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-part-03-bass-floor.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-03-bass-floor.md)

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
- `Y U QT - U Belong 2 Me (4x4 Mix)`: public rolling-bass proxy
- `Sammy Virji - I Guess We're Not the Same`: hook clarity, harmonic readability

Verification note:
- public track names checked against public catalog / press results on `2026-04-17`
- maintainer note:
  - these public references are also grounded by local ALS / transcript analysis inside this repo
  - use those internal artifacts when finer-grained note or function evidence is needed during authoring
- production-plan values are ranges and directions
- tutorial parts are where exact starting values get locked for the learner

## Named Production Blockers
### Fallback-heavy parts
- `chord-bed`
  - current anchor: `bl3ss-camrinwatsin-kisses:pad-1:i7`
  - issue: `mix_only` fallback, no actionable mutation suggestions
- `hook-response`
  - current anchor: `interplanetary-criminal-slow-burner:organ:i4`
  - issue: `mix_only` fallback, involved in `1` remaining conflict
- `og-reese-answer`
  - current anchor: `bl3ss-camrinwatsin-kisses:organ-bass:i1`
  - issue: `mix_only` fallback, involved in `2` remaining conflicts, no actionable mutation suggestions

### Active pairwise conflicts
- `bass-foundation` vs `og-reese-answer`
  - both read as `low_end_anchor`, so the low end stacks too heavily
- `hook-response` vs `og-reese-answer`
  - both want the forward midrange position

### Resolution direction
- `og-reese-answer` is the most replaceable lane because the composition plan now wants a warm phrase-end answer rather than a second bass-heavy voice
- `hook-response` should stay in the plan, but needs a stronger non-fallback patch choice
- `chord-bed` needs a real final pad/stab patch instead of a fallback wide pad placeholder

## Harmony Spec
### Progression
- `Dm9 -> Bb -> Fadd9 -> Cadd9`

### Why these chords
- `Dm9` gives darkness with more emotional color than plain `Dm`
- `Bb` is the hope chord, but its bloom is staged
- `Fadd9` and `Cadd9` keep forward motion and suspended lift without turning bright too early
- the emotional effect comes from staging the bloom, not from having every color tone exposed all the time

### Bb voicing states
- restrained `Bb` for `Intro / Drop A / Drop A Lift / Re-entry Build`: `Bb2 F3 C4`
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

### Chord duality mechanism
- use one core chord-bed patch for the sustained emotional layer
- create section-dependent articulation with MIDI length, velocity, and bus/sidechain behavior rather than inventing a second unrelated chord instrument first
- if a second stab layer is later needed, it must stay clearly subordinate to the main bed

### Chord articulation by section
- `Intro A`: filtered wash hints only
- `Intro B`: tucked full progression, long enough to feel bed-like
- `Drop A`: one-bar-per-chord pulse over sustained emotional bed
- `Drop A Lift`: same harmony, slightly brighter pulse only
- `Break`: 2-bar stretched voicings, upward bloom
- `Re-entry Build`: rhythmic pulse returns, but harmonic density stays restrained
- `Drop B`: same loop, obvious bloom
- `Drop B Lift`: same harmony, more width and top release, not reharmonization

### Chord-bed patch
- engine: `Serum 2`
- oscillator direction:
  - Osc A: warm saw / triangle-leaning main body
  - Osc B: quieter support oscillator for upper tone or gentle motion
  - restrained unison only
  - starting levels:
    - `Osc A`: `85%`
    - `Osc B`: `30%`
  - starting detune:
    - `0.03–0.05`
- filter:
  - smooth low-pass or band-softening filter
  - tucked lower in `Drop A`
  - opened and widened in `Break / Drop B`
  - starting values:
    - cutoff range `2.2–3.2 kHz`
    - resonance range `8–12%`
    - drive range `5–10%`
- envelope direction:
  - enough sustain to feel like a bed
  - enough decay / articulation that the pulse layer can still speak
  - starting values:
    - attack `5–15 ms`
    - decay `700–1200 ms`
    - sustain `55–75%`
    - release `250–450 ms`
- FX direction:
  - chorus or gentle width source
  - filtered reverb send
  - mild saturation for glue
- role:
  - emotional bed first
  - rhythmic pulse second

## Bass Spec
### Bass architecture
- bass is the `floor`, not the main hook
- stable sub layer + moving harmonic layer
- rolling motion is `rhythmic-primary`, `tonal-secondary`

### Sub patch
- engine: `Serum 2`
- source: `Sub oscillator` on sine
- main oscillators: `off`
- sub level: `100%` while designing, trim later at track level
- unison: `1`
- mono: `on`
- velocity sensitivity: `off`
- glide: start at `8 ms`; keep allowed adjustment range inside `5–20 ms`
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
  - Osc A: `Basic Shapes`, square-leaning frame
  - Osc B: `Basic Shapes`, saw-leaning support
  - start blend at `Osc A 75%` / `Osc B 30%`
  - keep detune inside `0.03–0.07` on Serum's `0.00–1.00` scale
- filter:
  - `MG Low 12` or similar smooth low-pass
  - cutoff as the main motion lane
  - light drive only
- envelope / LFO:
  - short amp attack
  - sustained body
  - one slow-breathing LFO or envelope-driven cutoff motion supporting phrase energy
- role:
  - most motion and character
  - does not become a second hook

### Sub / mid crossover
- keep most sub authority below `120–150 Hz`
- keep most character motion above that

### Gate / note-length behavior
- on-grid body notes: `50–70%` gate feel
- phrase-end releases: shorter and more punctuating, `15–35%` gate feel
- note-length variation is one of the main roll mechanisms

### Sidechain behavior
- kick -> sub: strongest duck
  - fast attack
  - release matched to kick tail, `90–120 ms`
  - ratio direction: `4:1` to `6:1`
  - aim for clear but not collapsing ducking
- kick -> mid-bass:
  - slightly lighter than sub
  - still clearly breathing
  - ratio direction: `2:1` to `4:1`
  - keep upper motion audible between kicks

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
- tail: target `100 ms`; acceptable first-pass window `90–120 ms`
- role: heavy, physical, not harsh

### Clap
- lands on `2` and `4`
- default is clap-first
- add tighter snare/rim support only when the section needs extra presence

### Hats
- closed/offbeat hats provide stable scaffold
- ghost hats create the real swing
- ghost hats should be intentionally late by `+9 ticks` / `+4 ms` on the first pass
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

### Drum sample sourcing policy
- kick body: short, tunable 909/garage-compatible low-end sample
- kick click: short upper-transient click layer
- clap: one main garage clap plus optional tighter snare/rim support
- hats: crisp 909 / garage-usable tops rather than brittle techno hats
- shaker: one source that still reads after filtering and velocity changes

Starting source recommendation:
- use `Ableton Core Library` / stock 909-compatible material as the first pass if exact external packs are not locked yet
- replace only if a stock source cannot hit the required body, tuning, or decay target

Capture requirement:
- once the exact files are chosen in the real build, record the file names verbatim for the later tutorial

## Hook and Answer Spec
### Hook notes
- `Drop A`: `A4 C5 D5`
- `Drop B`: `A4 C5 D5 F5`

### Exact rhythmic identity
- hook enters late and avoids the bar's beat-`1` downbeat
- collisions on beat `4` and next-bar beat `1` are intentional accent points, not mistakes
- in the current plan the core cell lands at:
  - on the `a` of beat `3`
  - on beat `4`
  - on the `a` of beat `4`
- on hook-owned `Drop B` bloom phrases, `F5` lands on beat `1` of the following bar

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

Oscillator direction:
- Osc A: sine / triangle-leaning body
- Osc B: brighter harmonic support for FM color
- use FM from B onto A lightly, just enough to get organ woodiness rather than bell harshness

Filter direction:
- smooth low-pass or gentle band-softening filter
- keep enough upper-mid bite for the hook to read
- starting cutoff should stay in the zone where the hook speaks clearly without getting fizzy

Envelope direction:
- fast attack
- medium-short decay
- low sustain
- short release

Starting ranges:
- attack: `0–5 ms`
- decay: `80–200 ms`
- sustain: `20–40%`
- release: `60–150 ms`
- filter cutoff starting zone: `1.2–3.5 kHz` depending on oscillator brightness

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

Starting deltas from the hook:
- decay and release `30–50%` shorter than the hook
- saturation / bite `20–40%` stronger than the hook
- keep the dry signal slightly shorter before reaching for more FX

### Register relationship
- hook should sit above the core chord bed enough to read clearly
- answer should feel related, not like a different instrument family

## Top-End, Air, and Stereo
### Air source
- use an atonal noise-based air bed
- keep it harmonically safe
- most audible in the break
- present quietly almost throughout

### Air patch
- engine: `Serum 2`
- source:
  - noise oscillator only
  - no tonal oscillators needed by default
- filter:
  - high-pass aggressively so it behaves like ceiling, not pad
- movement:
  - tiny slow filter or level motion only if needed
- space:
  - mostly from `Return C: long filtered hall` rather than a wet in-patch effect
  - this is the same main long-space return used by the chord bed, not a separate secret air-only hall by default

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

Starting split:
- `120–200 Hz`: let bass character lead here
- `200–300 Hz`: let chord warmth and some hook body live here more confidently
- if the low-mid feels cloudy, cut the chord bed first before thinning the bass floor

### Stereo map
- kick: mono / center
- sub: mono / center
- mid-bass: mono to narrow stereo above crossover
- hook: mostly center with stereo support from returns
- answer: a little wider than hook via returns
- chords: wide stereo
- air: widest layer
- loops/tops: stereo but controlled

Starting width targets:
- kick: `0–20%`
- sub: `0%`
- mid-bass: `0–40%` above the crossover only
- hook dry signal: `0–30%`
- answer dry signal: `20–40%`
- chords: `120–150%` equivalent width feel
- air: `140–170%` equivalent width feel
- loops/tops: `90–120%`

## Arrangement and Transition Spec
### Growth rule by section
- `Drop A`: force, restraint
- `Drop A Lift`: top-end density and pocket only
- `Break`: upward harmonic bloom and air
- `Re-entry Build`: rhythmic re-engagement
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
- break to re-entry build
- use:
  - re-entry drum switch
  - tighter chord pulse
  - filtered bass re-implication

#### 96 -> 97
- re-entry build to Drop B
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
- individual tracks should peak between `-12` and `-8 dBFS` before major bus work
- buses should peak between `-8` and `-6 dBFS`
- premaster should peak near `-6 dBFS`

### Bus structure
- Drum bus
- Bass bus
- Music bus
- FX / returns
- Premaster

### Device-chain order by bus
#### Drum bus
1. `EQ Eight`
2. `Glue Compressor`
3. `Saturator` or soft clip stage
4. `Utility`

Starting direction:
- EQ Eight:
  - remove obvious sub spill below the kick lane if needed
- Glue Compressor:
  - ratio `2:1` or `4:1`
  - attack on the slower side so transients still punch
  - release timed to groove, not maximum pumping
- Saturator / soft clip:
  - enough to add density
  - not enough to flatten hats and clap movement

#### Bass bus
1. `EQ Eight`
2. `Saturator`
3. sidechain / control compression if needed
4. `Utility`

Starting direction:
- EQ Eight:
  - keep the sub clean and let the mid layer own character above the crossover
- Saturator:
  - most extra density should happen here, not on the sub patch itself
- Utility:
  - keep low end centered

#### Music bus
1. `EQ Eight`
2. `Glue Compressor` or light bus compression if needed
3. tonal saturation if needed
4. `Utility`

Starting direction:
- keep the music bus breathing around the kick
- avoid flattening chord bloom and hook punctuation into one slab

### Track / file organization
- keep one Ableton group per major lane:
  - `Drums`
  - `Bass`
  - `Chords`
  - `Hook`
  - `Answer`
  - `Air`
  - `FX`
- keep sample folders inside the project for:
  - `Drums`
  - `FX`
  - `References`
  - `Exports / Checkpoints`
- save checkpoint sets by milestone, not only one rolling save

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

### Reference loudness matching
- loudness-match references before judging tone or weight
- use a `Utility` gain trim on the reference track so the perceived comparison is not biased by louder masters
- do the comparison at the premaster stage, not only after limiting

Practical method:
- pull references down until they feel subjectively matched against the current premaster
- compare at the same monitoring level every time
- judge one axis at a time:
  - pressure
  - groove pocket
  - bass roll
  - hook/harmony clarity

### Loudness direction
- do not chase final loudness early
- get translation right first

### Monitoring checks
- mono
- phone / small speaker
- car / everyday playback
- club-style low-end sanity if possible

Mono tool:
- put `Utility` last on the premaster and use it to check mono collapse quickly
- also audition the `Bass` group in mono while balancing kick and sub

### CPU and freeze policy
- Serum 2 plus multiple returns can get heavy fast
- once a patch and MIDI are stable enough to teach, freeze or bounce that lane before stacking more sound-design experiments on top
- keep the working session responsive enough that timing edits stay trustworthy

Working expectation:
- assume `30–40` active tracks by the time the arrangement and returns are all present
- expect to start freezing once there are more than `8–12` active Serum instances or the timing edits stop feeling immediate

### Bounce workflow
- export checkpoint bounces after:
  - `kick + air`
  - `full drums`
  - `drums + bass`
  - `drums + bass + chords`
  - `Drop A`
  - `Drop B`
  - `premaster`
- save them into the project `Exports / Checkpoints` folder so A/B and later tutorial capture use the same files

## Return / FX Starting Spec
### Return A: short room / ambience
- use for light drum glue only
- short decay
- low send level

### Return B: short plate
- use for hook / answer family
- keep pre-delay short enough that the attack stays readable

### Return C: long filtered hall
- use for chords and air
- high-pass and low-pass the return so it adds space without mud

### Return D: filtered delay
- use for phrase-end throws
- avoid constant wash

## Master Starting Spec
### Chain
1. `Utility`
2. `Glue Compressor`
3. soft saturation / clip
4. `Limiter`

### Starting settings direction
- Glue Compressor:
  - ratio `2:1`
  - gentle threshold
  - aim for small gain reduction only
- Limiter ceiling:
  - `-1 dBTP` ceiling target

### Loudness direction
- build stage:
  - prioritize translation and punch
- final stage:
  - aim for modern club strength only after the mix works
  - target `-8` to `-10 LUFS integrated` for the final club-ready master
- do not force loudness until kick/bass balance survives mono and small speakers
- keep limiter ceiling at `-1 dBTP`

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
- `Y U QT - U Belong 2 Me (4x4 Mix)`
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
