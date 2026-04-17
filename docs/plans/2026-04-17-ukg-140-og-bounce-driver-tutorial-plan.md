# UKG 140 OG Bounce Driver: Tutorial Plan

## Goal
Turn the frozen `ukg-140-og-bounce-driver` song plan into a handheld tutorial that can later become:
- a written walkthrough
- an in-app guided lesson
- or a build-session companion for later Ableton execution

This document is the pedagogy companion to:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)

It should not invent new musical decisions. It should teach the reader how to rebuild the frozen plan clearly and intentionally.

## Format Assumption
- text-first
- screenshot-friendly
- designed for later conversion into a guided lesson flow
- based on `Ableton Live 12` + `Serum 2`
- assumes downloadable companion assets later:
  - MIDI clips
  - Serum 2 patches
  - checkpoint audio bounces

Asset delivery target:
- one downloadable project bundle or zip containing:
  - Ableton project
  - Serum 2 presets
  - core MIDI
  - checkpoint WAVs
  - screenshot pack or embedded screenshots in the written tutorial

This means every important move should be:
- clickable in Ableton
- rebuildable in Serum
- explainable in plain language
- checkpointed with a listening task

## Audience
- producer with basic Ableton and Serum familiarity
- has finished a few tracks already
- understands MIDI, sidechain, EQ, and buses at a beginner-to-intermediate level
- wants to understand `why` the choices work, not just copy settings

## Who This Is Not For
- not for someone who has never finished a track at all
- not for someone who needs Ableton basics explained from zero
- not for someone looking for a one-page shortcut instead of a full build walkthrough
- if the learner already mixes professionally, the highest-value parts are likely `Parts 6–9`

## Tutorial Promise
By the end, the learner should be able to:
- build a modern rolling UKG floor without turning the bass into the lead
- stage harmonic bloom so `Drop B` feels earned
- write a low-note-count hook that still carries an instrumental
- program drums with real groove rather than generic global swing
- arrange a `144`-bar club track that grows by substitution, not just stacking
- mix the track so it feels open, heavy, and club-readable

## Teaching Principles
- teach one musical job at a time
- use references for calibration, not copying
- explain the emotional role of each decision
- keep anti-goals visible so the learner knows what to avoid
- capture exact settings where needed, but always explain the reason behind them

## Tutorial Deliverables
At the end of the tutorial, the learner should have:
- the full Ableton project
- Serum 2 patches for:
  - bass sub
  - bass mid
  - chord bed
  - hook
  - answer
  - air layer
- all core MIDI:
  - drums
  - bass
  - chords
  - hook / answer
- bounced checkpoints:
  - drums only
  - drums + bass
  - drums + bass + chords
  - Drop A
  - Drop B
  - premaster

## Screenshot Standard
For every major Serum 2 patch, capture at least:
- initialized patch / starting state
- oscillator state
- filter + envelope state
- modulation state
- FX state
- final patch state in context

For every major Ableton lane, capture at least:
- device-chain overview
- one close-up per important device
- MIDI clip or automation lane where the musical behavior lives

## Reference Kit
Use these references consistently during the tutorial:
- `KETTAMA - It Gets Better`
  - listen for kick weight, low-end size, mix density
- `Interplanetary Criminal - Slow Burner`
  - listen for ghost-hat drag, phrase-end motion, re-entry pocket
- `Y U QT - NRG`
  - listen for rhythmic-first bass roll and stable sub support
  - internal repo source is still `docs/transcripts/yuqt2_spans.json` until a named public Y U QT or SMTS replacement is locked
- `Sammy Virji - I Guess We're Not the Same`
  - listen for hook clarity and harmonic readability

Use loudness-matched references in the project so the learner is not fooled by master volume.

## Recommended Authoring Order
If this tutorial is written section-by-section, author it in this order:
1. `Part 3: Bass Floor`
2. `Part 2: Groove`
3. `Part 4: Harmonic Bed`
4. `Part 5: Identity`
5. `Part 6: Arrangement Build`
6. `Part 7: Transitions Toolkit`
7. `Part 8: Mix`
8. `Part 9: Master`
9. `Part 0 / Part 1` can be filled in early as setup/foundation scaffolding

Reason:
- the bass defines the lane
- the drums define the pocket
- everything else should build on those two identities

Detailed template available now:
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-part-03-bass-floor.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-03-bass-floor.md)

## Estimated Scope
- `Part 0`: `10–20 min`
- `Part 1`: `20–30 min`
- `Part 2`: `45–75 min`
- `Part 3`: `60–90 min`
- `Part 4`: `45–75 min`
- `Part 5`: `40–60 min`
- `Part 6`: `45–75 min`
- `Part 7`: `30–45 min`
- `Part 8`: `45–75 min`
- `Part 9`: `20–30 min`

Total likely guided runtime:
- roughly `6–10 hours` of build time depending on learner speed

Suggested session split:
- `Session 1`: Parts `0–3`
  - setup through bass floor
  - by the end, the lane identity should already be clear
- `Session 2`: Parts `4–6`
  - harmony, hook/answer, and arrangement
  - by the end, the song should fully exist
- `Session 3`: Parts `7–9`
  - transitions, mix, master
  - by the end, the track should translate and export cleanly

## Part 0: Setup
### Prerequisites
- learner can create groups, returns, and audio/MIDI tracks in Ableton
- learner can load Serum 2 and save a preset

### Learning objectives
- prepare an Ableton project that supports fast iteration
- load references and meters before writing anything
- understand the track's lane and anti-goals

### What the learner builds
- `140 BPM` Ableton 12 session
- track groups:
  - drums
  - bass
  - chords
  - hook
  - answer
  - air
  - FX
  - premaster
- return tracks for:
  - short room / ambience
  - short plate
  - long filtered hall
  - filtered delay

### What must be shown
- project tempo and timeline markers
- grouped routing
- return-track naming
- reference track loading / gain matching
- initial premaster headroom setup

### Common mistakes
- starting with a limiter and mixing into loudness too early
- not loading references until late in the session
- leaving the routing vague and solving it ad hoc later

### Listening checkpoint
- play 8 bars of silence + references loaded
- confirm the learner knows what each reference axis is for

### Troubleshooting
- if the project already feels disorganized before any music exists, stop and clean the routing now
- if the references are noticeably louder, trim them before any comparison

## Part 1: Foundation (Kick + Air Ceiling)
### Prerequisites
- the learner understands Simpler or can at least load and tune one-shot samples

### Learning objectives
- build the physical center of the track before melodic material
- understand why a constant quiet air ceiling matters

### What the learner builds
- layered kick tuned to `D`
- basic clap placeholder
- air layer that can live across the whole song

### What must be shown
- kick body sample choice
- kick click sample choice
- kick tuning workflow
- Simpler / sampler settings
- kick bus processing
- air-layer Serum 2 recipe or noise-source workflow

### Core teaching points
- kick must be heavy and short enough for the bass to breathe
- air should create ceiling, not become a melodic distraction

### Common mistakes
- long kick tails that force over-sidechaining later
- air layers that are too bright or too loud
- tuning the kick by feel without checking it against the tonic

### Listening checkpoint
- `4` bars of kick + air
- A/B against Kettama reference for body and scale

### Troubleshooting
- if the kick feels huge solo but disappears with bass later, the tail is probably too long
- if the air layer sounds like hiss instead of height, it is too loud or too broadband

## Part 2: Groove (Top Drums)
### Prerequisites
- the learner can edit MIDI note timing and velocity confidently

### Learning objectives
- build IC-style bounce with MIDI and timing, not just sample choice
- understand why ghost hats need intentional lateness, not random looseness

### What the learner builds
- closed hat pattern
- ghost hat pattern
- open-hat pattern
- clap layering
- shaker lane
- drum micro-architecture inside a `16`-bar section

### What must be shown
- exact MIDI placement for:
  - offbeat hats
  - ghost hats
  - open hats
- velocity ranges by element
- manual timing offsets
- phrase-end fills
- drum-bus chain

### Core teaching points
- kick and clap stay on-grid
- ghost hats arrive late and low in velocity
- groove comes from consistent asymmetry, not global swing presets
- each `16`-bar section needs internal development:
  - establish
  - deepen
  - lift
  - push

### Common mistakes
- using one swing preset on the whole drum rack
- making ghost hats too loud
- repeating the exact same 2-bar hat loop for 16 bars
- over-clipping the drum bus and flattening the groove

### Listening checkpoint
- full drum loop
- A/B against IC reference for pocket

### Troubleshooting
- if the groove feels random instead of swung, the hats are too loose rather than consistently late
- if the drop feels stiff, the problem is often MIDI timing before it is sample choice

## Part 3: Bass Floor
### Prerequisites
- the learner can route sidechain in Ableton
- the learner knows how to assign one LFO or envelope destination in Serum 2

### Learning objectives
- layer a modern rolling UKG bass floor
- understand `rhythmic-primary, tonal-secondary` bass motion
- keep the bass feeling alive without turning it into the hook

### What the learner builds
- Serum 2 sub patch
- Serum 2 mid-bass patch
- bass bus
- root path and release-note vocabulary

### What must be shown
- exact Serum 2 oscillator/filter/envelope setup for sub
- exact Serum 2 setup for the mid layer
- crossover / EQ split
- sidechain settings
- gate and note-length ranges
- phrase-end note rules

### Core teaching points
- the sub is the floor
- the mid layer carries character
- the roll should be mostly rhythmic
- tonal movement should support the rhythm, not replace it
- no ornamental note should imply a new chord

### Common mistakes
- too much melodic motion in the mid layer
- using portamento as a feature
- letting the mid layer invade the sub lane
- phrase-end notes that accidentally reharmonize the loop

### Listening checkpoint
- drums + bass
- A/B against Y U QT lane study for roll

### Troubleshooting
- if the bass feels static, first change gate and phrase pulse before adding more modulation
- if the bass feels melodic, remove note events before removing tone
- if the kick loses authority, shorten the kick or reduce mid-bass low content before increasing sidechain depth

## Part 4: Harmonic Bed
### Prerequisites
- the learner can enter chord MIDI and duplicate clips by section

### Learning objectives
- write a loop that feels emotional without spending the bloom too early
- understand why the `Bb` chord has restrained and bloomed states

### What the learner builds
- chord-bed Serum 2 patch
- Drop A chord voicings
- Break / Drop B chord voicings
- chord bus and returns

### What must be shown
- voicing palette:
  - `Dm9`
  - restrained `Bb`
  - bloomed `Bbmaj7`
  - `Fadd9`
  - `Cadd9`
- voice-leading strategy
- chord rhythm / pulse behavior by section
- sidechain and EQ carve decisions
- widening automation

### Core teaching points
- staging bloom is more important than having “fancy” chords everywhere
- the restrained `Bb` keeps hope latent
- the bloomed `Bbmaj7` reveals hope later
- chord delivery can be hybrid: sustained bed + pulse layer

### Common mistakes
- exposing the `Bbmaj7` too early
- bouncing the top voice around with root-position voicings
- widening the chords before the break
- forgetting to carve room for bass and hook

### Listening checkpoint
- drums + bass + chords
- A/B against Virji reference for emotional readability

### Troubleshooting
- if Drop A already feels “open,” the restrained `Bb` state is probably too bloomed
- if the chords feel stiff, check voice leading before changing the patch

## Part 5: Identity (Hook + Answer)
### Prerequisites
- the learner can program short melodic clips and automate send effects

### Learning objectives
- build an instrumental-first hook that carries the track
- use conversation by substitution, not stacking

### What the learner builds
- Serum 2 hook patch
- Serum 2 answer patch
- hook MIDI
- answer MIDI
- hook/answer processing chain

### What must be shown
- exact rhythmic placement of:
  - `A4`
  - `C5`
  - `D5`
  - and `F5` when bloom arrives
- repetition pattern across a `16`-bar drop
- answer placement at phrase ends only
- send automation / throws

### Core teaching points
- low note count can still be memorable if rhythm and timbre are strong
- the hook should stay readable by avoiding kick collisions
- the answer should feel like family, not a different song
- when the answer enters, the hook yields space

### Common mistakes
- making the hook too busy
- giving the answer full-phrase density
- using the same patch at the same envelope and register for hook and answer
- making the hook feel like a placeholder waiting for vocals

### Listening checkpoint
- full Drop A
- A/B against Y U QT / Virji lane for hook clarity

### Troubleshooting
- if the hook feels generic, fix rhythm first, not note count
- if the answer makes Drop B smaller, it is probably too dense or too continuous

## Part 6: Arrangement Build
### Prerequisites
- all core MIDI and sound lanes exist, even if some sounds are still placeholders

### Learning objectives
- shape a `144`-bar club record with distinct growth mechanisms by section
- understand why section growth must not all come from adding layers

### What the learner builds
- all nine sections:
  - Intro A
  - Intro B
  - Drop A
  - Drop A Lift
  - Break
  - Transition B
  - Drop B
  - Drop B Lift
  - Outro

### What must be shown
- section goals
- section-specific removals and additions
- where the hook appears
- where the answer appears
- how the top-end opens/closes
- where the bass is full, teased, or implied

### Core teaching points
- `Drop A Lift` gets bigger by pocket and top-end only
- `Break` gets bigger by upward harmonic bloom and air
- `Transition B` re-engages rhythm without spending the Drop B reveal
- `Drop B` gets bigger by harmonic bloom and phrase-end answer
- `Drop B Lift` gets bigger by alternation and top release

### Common mistakes
- making `Transition B` feel like a second break
- adding new harmonic information in `Drop A Lift`
- letting `Drop B` become “Drop A plus more”
- muting/unmuting blocks without internal phrase design

### Listening checkpoint
- full arrangement bounce
- check perceived energy curve from section to section

### Troubleshooting
- if a section feels blocky, add phrase architecture before adding new layers
- if Drop B does not feel bigger than Drop A, a bloom mechanism probably leaked early

## Part 7: Transitions Toolkit
### Prerequisites
- the learner can automate filters, sends, and volume

### Learning objectives
- make section changes exciting without turning the track into an FX demo
- use transition elements deliberately and at known bar positions

### What the learner builds
- riser
- downshifter / reverse reverb
- impact
- phrase-end fills
- pre-drop cuts
- drum-bus filter sweeps
- reverse cymbals

### What must be shown
- exact bars where each tool enters
- which transitions use which tools
- automation shapes for filter / send / volume moves

### Core teaching points
- transitions should have specific jobs
- re-entry energy is often rhythmic, not harmonic
- silence or subtraction can be more exciting than adding noise

### Common mistakes
- using the same riser everywhere
- starting every riser at the same distance from the drop
- over-filling transitions until the return feels smaller than the build

### Listening checkpoint
- listen only to the bars around section boundaries
- confirm each one has a unique personality

### Troubleshooting
- if every transition sounds the same, vary timing and subtraction before inventing new FX
- if the return feels weak, the build probably reveals too much too early

## Part 8: Mix
### Prerequisites
- all arrangement decisions are stable enough that the learner is no longer rewriting the song

### Learning objectives
- keep the track heavy, open, and club-readable
- understand lane ownership by bus, band, and stereo position

### What the learner builds
- bus structure
- sidechain network
- EQ / compression / saturation chains
- reverb and delay sends
- stereo field distribution

### What must be shown
- gain staging targets
- bus chains in order
- sidechain routing
- EQ strategy by element
- stereo policy
- A/B comparison workflow

### Core teaching points
- mix decisions should reinforce the arrangement logic
- the track must feel big because of separation, not because everything is loud
- low-mid clarity matters more than adding treble

### Common mistakes
- trying to solve sound-selection problems with EQ alone
- flattening the drum groove with too much bus compression
- widening the wrong elements
- chasing loudness before balances are right

### Listening checkpoint
- compare premaster against each reference by axis:
  - pressure
  - swing
  - bass roll
  - hook clarity

### Troubleshooting
- if the track only works loud, the balances are wrong
- if the low-mid feels muddy, solve lane ownership before adding more top end

## Part 9: Master
### Prerequisites
- premaster is translating well and has working headroom

### Learning objectives
- finish the track to a club-ready but controlled loudness
- verify translation before final export

### What the learner builds
- master chain
- limiter stage
- export workflow

### What must be shown
- glue compression
- saturation / soft clipping
- limiter setup
- loudness targets
- monitoring checks
- export settings

### Core teaching points
- loudness is the last step, not the first
- a stable premaster beats a loud messy premaster
- mono and small-speaker checks catch problems the studio monitors hide

### Common mistakes
- limiting into distortion
- clipping the kick/bass relationship into blur
- skipping mono checks
- forgetting to loudness-match references

### Listening checkpoint
- export premaster and final
- compare against loudness-matched references

### Troubleshooting
- if loudness removes punch, back out of the limiter and fix the premaster
- if the track folds in mono, the stereo map is wrong upstream, not just at the master

## Concept-To-Technique Map
- `rolling bass floor`
  - stable sine sub
  - rhythmic gate variation
  - light filter / saturation breathing
- `dark but hopeful`
  - minor-center low-end restraint
  - delayed `Bbmaj7` bloom
  - upward voicing spread in break / Drop B
- `instrumental-first identity`
  - warm organ hook
  - phrase-end answer
  - no vocal dependency
- `section growth by substitution`
  - hook half-density in Drop B
  - answer on alternate phrase endings
  - top-end release mapped by section

## Required Capture Checklist
During the actual build session, capture:
- Serum 2 screenshots for every major patch stage
- exact Ableton device chains on every major track/bus
- MIDI screenshots for:
  - drum pocket
  - bass phrase
  - chord voicings
  - hook / answer alternation
- audio bounces at every listening checkpoint
- note on what changed between each major checkpoint

## Tutorial Troubleshooting Philosophy
- always fix the musical cause before the mix symptom
- always fix note density before adding more sound-design motion
- always check timing before replacing samples
- if a learner gets stuck, the tutorial should point them to:
  - the likely cause
  - the fastest diagnostic
  - the safest correction

## Lesson Authoring Implications
When this becomes the guided lesson:
- each major tutorial part can become one lesson chapter
- checkpoints should map to audible artifacts, not abstract prose
- common mistakes should become warning callouts in the lesson
- references should become “listen for this” prompts, not hidden background context

## Remaining Blockers Before Final Tutorial Draft
- lock exact final synth choices in place of fallback-heavy matches:
  - `chord-bed`
  - `hook-response`
  - `og-reese-answer`
- resolve the remaining pairwise sound conflicts:
  - `bass-foundation` vs `og-reese-answer`
  - `hook-response` vs `og-reese-answer`
- do one audio verification pass so the tutorial reflects what actually works in sound, not only on paper

These are not architecture blockers anymore. They are fidelity blockers for the final handheld lesson.
