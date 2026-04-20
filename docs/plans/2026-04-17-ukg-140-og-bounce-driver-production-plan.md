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
- `160 bars`
- `~4.57 minutes`
- emotional target: `dark but hopeful`

Reference role split:
- `KETTAMA - It Gets Better`: pressure, weight, density
- `Interplanetary Criminal - Slow Burner`: swing, hat drag, phrase-end groove
- `Y U QT - U Belong 2 Me (4x4 Mix)`: public rolling-bass proxy
- `Sammy Virji - I Guess We're Not the Same`: vocal/hook clarity, harmonic readability

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
- `vocal-sample-source`
  - current anchor: none selected yet
  - issue: final vocal sample must be found, cleared, key-checked, time-checked, and placed

### Active pairwise conflicts
- `bass-foundation` vs `vocal-sample-source`
  - a low / muddy vocal chop can mask the rolling bass if it is not filtered or chosen carefully
- `chord-bed` vs `vocal-sample-source`
  - a melodic vocal can imply notes that fight the staged chord bloom

### Resolution direction
- remove the old synth hook/answer from the core production path
- build `Vocal Audition`, `Vocal Full Chorus`, `Vocal Chops`, and `Vocal Throw` audio lanes instead
- if no vocal is found yet, keep muted guide clips rather than filling the lane with a synth
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
- restrained `Bb` for `Intro / Break A / Drop A / Drop A Lift / Re-entry Build`: `Bb2 F3 C4`
- bloomed `Bbmaj7` for `Break B / Drop B`: `Bb2 F3 A3 C4`

### Voice-leading strategy
- preserve common tones where possible
- keep upper voices moving by short steps
- avoid bouncing every chord in root position in the chord register

Practical voice-leading rule:
- let `A` and/or `C` act as anchors where possible from `Dm9` into the restrained `Bb` state
- let top-voice motion step into `Fadd9` and `Cadd9`

### Vocal-aware chord register strategy
The current vocal analysis shows the useful singer range is roughly `G#3-C5`.

The setup / verse-like material mostly lives `G#3-F4`.
The full chorus mostly lives `F4-C5`.

The danger pitch classes are `F`, `Bb`, `A`, and `G` because those are the notes the vocal holds most often.

Production rule:
- do not solve vocal masking by making the vocal thin
- first move the sustained pad note away from the active vocal register
- keep chord body below the vocal and use only deliberate octave-5 shimmer above it

First-pass register-safe chord variants:
- lower vocal setup variant for `Break A`:
  - `Dm9`: `D2 A2 C3 E3`
  - restrained `Bb`: `Bb2 F3 C4`
  - `Fadd9`: `F2 C3 A3`
  - `Cadd9`: `C3 E3 G3`
- hook-safe variant for `Drop A`, `Drop B`, and any full-chorus placement:
  - `Dm9`: `D2 A2 E3`, optional `E5` air
  - restrained `Bb`: `Bb2 F3 C4`, optional `F5` air only if the vocal leaves space
  - bloomed `Bbmaj7`: `Bb2 F3 A3 C4`, optional `F5` air
  - `Fadd9`: `F2 C3 A3`, optional `C5` or `G5` air only if it does not mask the lead
  - `Cadd9`: `C3 G3 E4`, optional `E5` air

Universal fallback if the pad still fights the vocal:
- keep chord body in octaves `2-3`
- keep color shimmer in octave `5`
- leave octave `4` mostly empty

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
- `Break A`: restrained suspended bed that leaves room for first vocal
- `Drop A`: one-bar-per-chord pulse over sustained emotional bed
- `Drop A Lift`: same harmony, slightly brighter pulse only
- `Break B`: 2-bar stretched voicings, upward bloom
- `Re-entry Build`: rhythmic pulse returns, but harmonic density stays restrained
- `Drop B`: same loop, obvious bloom
- `Drop B Lift`: same harmony, more width and top release, not reharmonization

### Chord-bed patch
- engine: `Serum 2`
- oscillator direction:
  - Osc A: warm saw / triangle-saw main body
  - Osc B: quieter triangle / rounded support oscillator
  - restrained unison only
  - starting levels:
    - `Osc A`: `70%`
    - `Osc B`: `15–20%`
  - starting detune:
    - `Osc A`: `0.03–0.04`
    - `Osc B`: `0.00`
- filter:
  - smooth low-pass, not a band-pass or notch for the first pass
  - tucked lower in `Drop A`
  - opened and widened in `Break / Drop B`
  - starting values:
    - cutoff range `1.8–2.2 kHz`
    - resonance range `5–8%`
    - drive range `0–3%`
  - section automation may open as high as roughly `2.6 kHz` for `Drop B Lift`, but do not return to the old `3 kHz+` chord-bed values unless the patch is clearly too dull in context
- envelope direction:
  - enough sustain to feel like a bed
  - enough decay / articulation that the pulse layer can still speak
  - starting values:
    - attack `30–45 ms`
    - hold `0.0 ms`
    - decay `1.0–1.3 s`
    - sustain `-5 to -7 dB` if shown in dB, or `60–70%`
    - release `400–550 ms`
- FX direction:
  - chorus or gentle width source only after the dry chord works
  - filtered reverb send
  - no in-patch reverb, delay, compressor, or distortion on the first pass
- role:
  - warm sustained chord layer first
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
- sub unison: no setting required in the Serum 2 sub oscillator view
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

## Vocal Sample Spec
### Lane design
- `Vocal Audition`: workbench track for testing candidates
- `Vocal Full Chorus`: clean intact hook take lane
- `Vocal Chops`: dry chopped fragment lane
- `Vocal Throw`: shorter tail / breath / syllable / delayed response lane
- muted `Vocal Guide MIDI`: optional visual ruler only, not final audio

### Sample selection target
- dry or mostly dry
- euphoric phrase, one-shot, breath, ad-lib, or chop
- harmonically safe against `D minor`
- does not fight the `Bbmaj7` bloom
- no printed bass / drums / huge reverb that cannot be removed
- human enough to replace the old synth hook identity

### Phrase-led mode
- A full clean chorus is allowed and expected in `Drop A` and `Drop B`.
- The first intact chorus should land before the aggressive chop deconstruction, not after it.
- Chops, tails, reverses, and throws are still needed, but they support and deconstruct the chorus instead of replacing it.
- If using a commercial stem for a private sketch, keep the lesson labels functional and do not publish lyric text in the public tutorial unless the vocal is cleared.

### Two-chain vocal prep
- `Vocal Full Chorus` chain:
  - cleaner
  - more forward
  - gentle compression / de-essing if needed
  - short plate or hall only enough to place it in the track
- `Vocal Chops` chain:
  - drier
  - tighter gate / clip fades
  - stronger EQ cleanup
  - optional drive, reverse tails, pitch variants, and delay throws

Why:
- the intact chorus should feel singable and recognizable
- the chopped sections should feel edited, clubby, and aggressive enough to stop the record becoming a straight cover

### Phonetic loop policy
- Open-`oh` endings are best for repeated drop hooks.
- Open-`eye` endings are strong for one-time pre-drop tension.
- Nasal endings are useful for punctuation and build, but can feel flat if looped.
- Consonant clusters should be used once, crossfaded, reversed, or gated tightly.
- If two open-`oh` phrases exist, test them as an intercut `A/B/A/B` loop before looping one phrase alone.

### First-pass placement states
- `Intro A`: no vocal
- `Intro B`: no vocal
- `Break A`: `VOC mystery statement` at `40.1.1`
- `Break A`: optional `VOC mystery seed` at `44.1.1`
- `Break A`: `VOC question pre-drop` at `48.3.3`, ending before `49.1.1`
- `Drop A`: `VOC full chorus clean` starts at `49.1.1` and ends before `65.1.1`
- `Drop A`: keep only short end-of-line throws if the intact chorus has natural gaps
- `Drop A Lift`: `VOC chop A` at `68.3.4`
- `Drop A Lift`: `VOC chop B` at `72.3.4`
- `Drop A Lift`: `VOC exposed core` at `76.3.4`
- `Break B`: `VOC question pre-drop` or `VOC mystery seed` at `88.1.1`
- `Break B`: optional `VOC vulnerable phrase` at `92.1.1`
- `Re-entry Build`: filtered pickup at `109.3.4` or `110.3.4`
- `Re-entry Build`: `VOC question pre-drop` at `112.3.3`, ending before `113.1.1`
- `Drop B`: `VOC full chorus clean` returns at `113.1.1` and ends before `129.1.1`
- `Drop B`: add low-level chop texture only in chorus gaps, not over every sung line
- `Drop B Lift`: strongest cuts / stacks at `132.3.4`, `136.3.4`, `140.3.4`, and optionally `144.3.4`
- `Outro`: tails and throws only after `145.1.1`

### D-minor trance vocal alternate
- `VOC mystery seed`: filtered build punctuation, strongest in `Break A` and `Break B`
- `VOC question pre-drop`: starts at `48.3.3` before `Drop A`, then returns at `112.3.3` before `Drop B`
- `VOC full chorus clean`: starts at `49.1.1` in `Drop A` and returns at `113.1.1` in `Drop B`
- `VOC chop A`: starts at `68.3.4` in `Drop A Lift`
- `VOC chop B`: starts at `72.3.4` in `Drop A Lift`
- if the chop lift crowds the chorus memory, remove `VOC chop B` first and keep `VOC exposed core`
- `VOC vulnerable phrase`: break-only unless the consonant ending is crossfaded cleanly

### Current D-minor trance vocal arc
- early restraint: no vocal in `Intro A` or `Intro B`
- first vocal introduction: `VOC mystery statement` at `40.1.1`, optional `VOC mystery seed` at `44.1.1`
- first question setup: `VOC question pre-drop` starts at `48.3.3` and ends before `49.1.1`
- first full-chorus answer: `VOC full chorus clean` at `49.1.1`
- first lift intensifier: `VOC chop A` at `68.3.4`, `VOC chop B` at `72.3.4`, and `VOC exposed core` at `76.3.4`
- darker return: `VOC question pre-drop` or `VOC mystery seed` at `88.1.1`; optional `VOC vulnerable phrase` at `92.1.1`
- second question setup: filtered pickup at `109.3.4` or `110.3.4`, then `VOC question pre-drop` at `112.3.3`
- final answer: `VOC full chorus clean` returns at `113.1.1`
- peak edit: strongest cuts / stacks at `132.3.4`, `136.3.4`, `140.3.4`, and optionally `144.3.4`

### Current vocal MIDI arrangement facts
- useful vocal range: roughly `G#3-C5`
- setup / verse-like material: mostly `G#3-F4`
- full chorus material: mostly `F4-C5`
- longest-held pitch classes: `F`, `Bb`, `A`, `G`
- low-content / breath bars inside the full chorus: local bars `4`, `7-8`, `10`, and `12`

Arrangement translation:
- `Drop A` full-chorus breath windows: bars `52`, `55-56`, `58`, and `60`
- `Drop B` full-chorus breath windows: bars `116`, `119-120`, `122`, and `124`

Use those windows for fills, throws, and bass answers.
Do not add busy fills under the densest sung lines.

### Processing direction
- high-pass enough to stay out of the bass lane
- short plate on `Return B` only if it helps the vocal sit
- filtered delay on `Return D` for throws
- keep `Vocal Full Chorus` more forward and dry than `Vocal Chops` / `Vocal Throw`

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
  - vocal attack
  - vocal throw edge

### EQ ownership direction
- `30–90 Hz`: sub / kick
- `120–300 Hz`: carefully split between bass character and chord warmth
- `300 Hz–2 kHz`: emotion + vocal intelligibility
- `2–6 kHz`: presence
- `8 kHz+`: air

Starting split:
- `120–200 Hz`: let bass character lead here
- `200–300 Hz`: let chord warmth live here, but keep vocal mud controlled
- if the low-mid feels cloudy, cut the chord bed first before thinning the bass floor

### Stereo map
- kick: mono / center
- sub: mono / center
- mid-bass: mono to narrow stereo above crossover
- vocal main: mostly center with stereo support from returns
- vocal throw: wider than vocal main via returns
- chords: wide stereo
- air: widest layer
- loops/tops: stereo but controlled

Starting width targets:
- kick: `0–20%`
- sub: `0%`
- mid-bass: `0–40%` above the crossover only
- vocal main dry signal: `0–20%`
- vocal throw dry signal: `20–50%`
- chords: `120–150%` equivalent width feel
- air: `140–170%` equivalent width feel
- loops/tops: `90–120%`

## Arrangement and Transition Spec
### Growth rule by section
- `Break A`: first vocal space and pre-drop question
- `Drop A`: force, restraint
- `Drop A Lift`: top-end density and pocket only
- `Break B`: upward harmonic bloom and darker vocal return
- `Re-entry Build`: rhythmic re-engagement
- `Drop B`: harmonic bloom + fuller vocal payoff
- `Drop B Lift`: widest, most released top end

### Transition inventory
#### 32 -> 33
- intro to `Break A`
- use:
  - small section riser
  - filtered drum thinning
  - vocal-space opening

#### 48 -> 49
- `Break A` to first drop
- use:
  - pre-drop question cut
  - full bass body return
  - drum-bus HP clearing off

#### 80 -> 81
- first lift to break
- use:
  - phrase-end fill
  - drum thinning
  - widening reverb / chord bloom

#### 96 -> 97
- `Break B` to re-entry build
- use:
  - re-entry drum switch
  - tighter chord pulse
  - filtered bass re-implication

#### 112 -> 113
- re-entry build to Drop B
- use:
  - pre-drop cut
  - filtered vocal pickup
  - full body return

#### 144 -> 145
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
  - restrained in Break A
  - widened in Break B
  - bloomed in Drop B
- vocal send levels:
  - `Vocal Full Chorus` mostly readable and dry
  - `Vocal Chops` tighter and slightly more processed
  - `Vocal Throw` selected phrase-end throws only
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
- avoid flattening chord bloom and vocal punctuation into one slab

### Track / file organization
- keep one Ableton group per major lane:
  - `Drums`
  - `Bass`
  - `Chords`
  - `Vocal Full Chorus`
  - `Vocal Chops`
  - `Vocal Throw`
  - `Vocal Audition`
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
- vocal main / vocal throw: intelligibility and texture, not fuzz

### Reverb
- short room / ambience if drums need glue
- short plate for vocal main / vocal throw
- longer hall/plate for chords + air, filtered

### Delay
- filtered delays as throws
- avoid constant wash
- vocal throw can take short rhythmic delay if it strengthens identity

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
- use for vocal main / vocal throw family
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

### Vocal and harmony readability
- `Sammy Virji - I Guess We're Not the Same`
- check:
  - vocal/hook clarity
  - harmonic readability in a club mix

## Originality Tests
- if the vocal chop feels too close to a source hook, change placement, chop length, filtering, or source sample
- if the vocal phrase is from a commercial stem, treat it as private-sketch material unless it is cleared, recreated, or replaced
- if a bass phrase feels too source-like, change gate length, phrase-end note choice, or register emphasis
- if a transition feels recognizable, keep the role and change the timing or FX combination

## Production-Ready Checklist
- choose exact final synths instead of fallback-heavy placeholders
- resolve pairwise sound conflicts before mixing around them
- ensure no `16`-bar section loops identically
- verify `Drop A Lift` adds no new harmonic information
- verify `Drop B` vocal throw stays phrase-end only
- verify the break vocal phrase feels suspended and intentional, not like a full chorus pasted over the break
