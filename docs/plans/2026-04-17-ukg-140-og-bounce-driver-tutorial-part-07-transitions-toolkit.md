# UKG 140 OG Bounce Driver: Tutorial Part 7 — Transitions Toolkit

## Purpose
Teach the learner how to make the section boundaries in `ukg-140-og-bounce-driver` feel exciting, intentional, and genre-native without turning the track into an FX demo.

This part should turn the static arrangement from `Part 6` into a moving club record by writing:
- phrase-end fills
- section risers
- pre-drop cuts
- reverse / downshift moments
- drum-bus filter sweeps
- targeted send and width automation

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-part-06-arrangement-build.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-06-arrangement-build.md)

## Outcome
By the end of this part, the learner should have:
- a clear transition job for every major boundary
- a clear transition job for every minor boundary too
- phrase-end drum fills and groove drops where needed
- drum-bus filter and subtraction moves written at intros / transitions
- send and width throws written only where they strengthen the handoff
- one boundary-only bounce plus one full-song rough bounce with transitions in place

## Time Estimate
- `45–60 minutes`

## Prerequisites
- learner has completed or can reference:
  - `Part 2` groove
  - `Part 4` harmonic bed
  - `Part 5` identity
  - `Part 6` arrangement build
- the arrangement is already stable enough that section lengths and lane assignments are no longer moving
- the learner can automate:
  - filters
  - sends
  - volume / clip mutes
  - utility width when needed

## What The Learner Should Understand Before Starting
Transitions here are not:
- the same riser copy-pasted everywhere
- noise sweep plus crash on every boundary
- filling every phrase end until the return feels smaller than the build

Transitions here are:
- job-specific
- bar-specific
- partly subtractive
- tied to the section growth mechanism

Important naming note:
- every section handoff in this song is a transition
- `Intro A -> Intro B` is a transition
- `Drop A -> Drop A Lift` is a transition
- `Drop A Lift -> Break B` is a transition
- `Break B -> Re-entry Build` is a transition
- `Re-entry Build -> Drop B` is a transition
- the old label `Transition B` was confusing because it made one full `16`-bar section sound like the only transition in the arrangement
- in this tutorial, the dedicated `97–112` block is called the `Re-entry Build` because it is a full section whose job is to wake the groove back up before `Drop B`

If every transition uses the same timing and same FX, the whole arrangement will flatten out even if the sounds are good.

Timing reminder for this part:
- every bar number in this chapter is a full Arrangement View position
- if you open a local fill clip while following this chapter, its internal `1.1.1` starts wherever you place that clip in the arrangement

## Reference Axis
Primary A/B for this part:
- `Interplanetary Criminal - Slow Burner`
  - listen for how re-entry energy is created through drum language and pocket, not only white noise
- `KETTAMA - It Gets Better`
  - listen for how stripped moments still feel physically connected to the record

Secondary check:
- `Sammy Virji - I Guess We're Not the Same`
  - listen for how hook and harmonic reveals arrive in distinct stages instead of all at once

## Files / Assets Needed
- the full arranged project from `Part 6`
- one dedicated `FX` group containing:
  - riser
  - downshifter / reverse reverb
  - impact
  - reverse cymbal
- access to returns:
  - `Return B`: short plate
  - `Return C`: long filtered hall
  - `Return D`: filtered delay
- drum-bus filter ready to automate
- Utility on the premaster for quick mono checks

## Frozen Boundary Jobs
Use this as the source of truth.

Minor boundaries:
- `16 -> 17`
  - intro reveal
  - no giant riser
  - filtered opening into `Intro B`
- `64 -> 65`
  - lift activation
  - phrase-end drum pressure, not a new section identity
- `128 -> 129`
  - second-drop lift
  - pressure increase, not a whole new reset
- `144 -> 145`
  - peak to outro
  - remove top pressure first

Major boundaries:
- `32 -> 33`
  - intro to `Break A`
  - open vocal space without full drop weight
- `48 -> 49`
  - `Break A` to `Drop A`
  - first intact chorus landing
  - full bass and drop drums return
- `80 -> 81`
  - first lift to `Break B`
  - phrase-end fill
  - drum thinning
  - widening reverb / chord bloom
- `96 -> 97`
  - `Break B` to `Re-entry Build`
  - re-entry drum switch
  - tighter chord pulse
  - filtered bass re-implication
- `112 -> 113`
  - `Re-entry Build` to `Drop B`
  - pre-drop cut
  - filtered vocal pickup resolving
  - full body return

## Automation Ownership In This Part
Write these here:
- drum-bus high-pass moves at intros and transitions
- vocal phrase-end throws
- air-bed level moves around break and outro
- obvious width handoffs already defined in `Part 4`
- boundary mutes / cuts / returns

Do not over-finish these here:
- micro-mix rides within phrases
- mastering-stage polish
- late-stage creative FX experiments that change the song structure

## Step 1: Mark Every Boundary And Its Job
### Action
Create locators or text notes at:
- `16 -> 17`
- `32 -> 33`
- `48 -> 49`
- `64 -> 65`
- `80 -> 81`
- `96 -> 97`
- `112 -> 113`
- `128 -> 129`
- `144 -> 145`

Add the transition job next to each boundary:
- e.g. `96->97 = pre-drop cut + full body return`

Exact locator placement:
1. Add locators at:
   - `16.1.1`
   - `32.1.1`
   - `48.1.1`
   - `64.1.1`
   - `80.1.1`
   - `96.1.1`
   - `112.1.1`
   - `128.1.1`
   - `144.1.1`
2. Rename each one with the job written directly into the locator name so the transition role is visible while you edit automation.
3. Use naming like:
   - `16->17 intro reveal`
   - `32->33 break A vocal space`
   - `48->49 lift pressure`
   - `64->65 break release`
   - `80->81 re-entry wakeup`
   - `96->97 redrop land`
   - `112->113 lift pressure 2`
   - `128->129 outro handoff`

### Why
Every boundary needs its own reason.

If the learner only thinks “I need a riser here,” the transitions will all collapse into the same gesture.

### Screenshot
- `transitions-01-boundary-map`

## Step 2: Prep The Transition Toolkit Lanes
### Action
Create or label the exact tools you will use:
- `FX-Riser`
- `FX-Downshifter`
- `FX-Impact`
- `FX-Reverse-Cymbal`
- `FX-Reverse-Reverb` if separate

Then confirm:
- drum bus has a high-pass filter ready
- `Return B`, `Return C`, and `Return D` are visible
- the `Vocal Full Chorus`, `Vocal Chops`, and `Vocal Throw` lanes can automate send levels
- the chord lane can automate width and brightness if needed
- if using the current phrase, the transition-ready vocal clips exist:
  - `VOC i just wanna tease`
  - `VOC believe reverse`
  - `VOC in throw`
- if using a big trance / rave vocal stem, the transition-ready clips exist:
  - `VOC hook title chop`
  - `VOC isolation throw`
  - `VOC reverse tail`

### Why
Transitions become slow and messy when the tools are not prepared before writing automation.

### Rule
- one tool can serve multiple jobs
- but no tool should appear at every boundary in the same way

### Screenshot
- `transitions-02-toolkit-lanes`

## Step 3: Write Phrase-End Fills Inside The Sections First
### Action
Before touching the major section boundaries, write the phrase-end pressure at:
- bar `16`
- bar `32`
- bar `48`
- bar `64`
- bar `80`
- bar `96`
- bar `112`
- bar `128`

Starting moves:
- short snare / clap fill in the last `1–2` beats
- ghost-hat density increase in the last `1` bar
- optional brief groove drop on the very last beat before the next section

Exact first-pass fill pattern for any boundary bar:
1. In the final bar before the boundary, add hits at:
   - `x.3.3`
   - `x.4.1`
   - `x.4.3`
   - `x.4.4`
2. Replace `x` with the actual boundary bar number:
   - `16`, `32`, `48`, `64`, `80`, `96`, `112`, `128`, or `144`
3. If the fill feels too loud, lower the fill lane by `2 dB` before deleting notes.

Keep the intensity ranked:
- smallest fills:
  - `16 -> 17`
  - `64 -> 65`
  - `128 -> 129`
  - `144 -> 145`
- medium:
  - `32 -> 33`
  - `80 -> 81`
  - `96 -> 97`
- biggest:
  - `48 -> 49`
  - `112 -> 113`

### Why
The large transition effects only work if the groove is already signaling a phrase boundary.

### Screenshot
- `transitions-03-phrase-end-fills`

### Visual Requirement
- show one `16`-bar section with the fill bar clearly visible
- show at least one major boundary and one minor boundary for comparison

## Step 4: Write The Intro-To-Drop Entry (`32 -> 33`)
### Action
On bars `31–33`:
- add a `1`-bar section riser
- automate the drum-bus high-pass to clear off through bar `32`
- let the filtered bass teaser open into the full `Drop A` body
- allow a very short pre-drop subtraction only if the landing gets bigger, not weaker
- stop the riser cleanly at the downbeat of `33`

Exact first-pass timing:
1. Place the riser clip from `32.1.1` to `33.1.1`.
2. On the drum-bus high-pass filter, create automation points at:
   - `31.1.1`
   - `32.1.1`
   - `32.4.4`
   - `33.1.1`
3. Set the cutoff values:
   - `31.1.1`: `20 Hz`, effectively open
   - `32.1.1`: `80 Hz`, enough to start thinning the drum weight
   - `32.4.4`: `180 Hz`, strongest filtered moment before the drop
   - `33.1.1`: `20 Hz`, fully open again
4. Start the filter mostly open at `31.1.1`.
5. Push the high-pass effect strongest at `32.4.4`.
6. Return the filter to fully open again at `33.1.1`.
7. If you use a pre-drop cut, make it happen only in the last beat:
   - `32.4.1` to `33.1.1`
8. On the drum lanes:
   - keep `Kick Body` and `Kick Click` active through `32.4.1`
   - mute `Open Hat` at `32.4.3`
   - let the phrase-end fill own `32.4.3` and `32.4.4`
   - if `Shaker` is busy, lower it by exactly `2 dB` from `32.4.1` to `33.1.1`

### Why
This is the first full landing of the track.

It should feel like the floor arrives, not like a cinematic fake-out.

### Mechanical shape
- bar `31`: start the riser quietly
- bar `32`: drum-bus HP opens further, teaser bass becomes more obvious
- beat `1` of bar `33`: riser off, filter open, full body on

### Screenshot Set
- `transitions-04a-intro-drop-overview`
- `transitions-04b-intro-drop-automation-close`

## Step 5: Write The Drop-A-To-Lift Activation (`64 -> 65`)
### Action
On bars `63–65`:
- use a phrase-end drum fill, not a giant riser
- keep the same harmonic state
- increase top pressure into `65`
- do not add a new bass note or chord color
- keep the first beat of `65` feeling like the same drop lifting, not a new section

Exact first-pass timing:
1. Start the fill move late in bar `63` or at `64.1.1`, not two bars early.
2. Raise top pressure at `64.3.1`.
3. Keep chord width restrained through `64.4.4`.
4. Let the denser top state be fully in place by `65.1.1`.
5. Do not use a downshifter here unless the lift feels too abrupt.
6. On the drum lanes:
   - keep the kick on `64.1.1`, `64.2.1`, and `64.3.1`
   - remove the `Open Hat` from `64.4.3`
   - keep the final kick at `64.4.1` unless it masks a vocal chop
   - keep the fill hits at `64.3.3`, `64.4.1`, `64.4.3`, `64.4.4` quieter than the `32 -> 33` landing

### Why
The lift transition should feel like the same drop getting more urgent.

The mistake here is revealing the `Break B` / `Drop B` bloom too early.

### Mechanical shape
- late bar `63` / bar `64`: fill and slight drum thinning begin
- downbeat of `65`: same section world, more top pressure

### Screenshot Set
- `transitions-05a-lift-break-overview`
- `transitions-05b-lift-break-send-width-close`

## Step 6: Write The Drop-A-Lift-To-Break-B Release (`80 -> 81`)
### Action
On bars `79–81`:
- release pressure into the darker second break
- thin the drums at `81`
- let chord bloom / air become more audible
- do not bring re-entry drums in yet
- keep the re-entry vocal pickup out until the end of `Re-entry Build`

Exact first-pass timing:
1. Keep the final lift pressure through `79.4.4`.
2. Start thinning the drums at `80.3.1`.
3. Let the break state land exactly at `81.1.1`.
4. Pull full bass body back at `81.1.1`.
5. Let the vocal / chord space become readable before adding new fills.
6. On the drum lanes at `81.1.1`:
   - remove `Open Hat`
   - remove or reduce `Ghost Hat`
   - keep only sparse closed-hat / shaker support if needed
7. If the handoff feels dead, add one quiet fill hit at `80.4.3` before adding a riser.

### Why
`Break B` is the darker breath before the re-entry.

It should not already sound like `Re-entry Build`.

### Mechanical shape
- bar `79`: last wide break state
- bar `80`: hint of re-entry pressure
- beat `1` of bar `81`: new drum language, tighter chord pulse, filtered low-end implication back

### Rule
- if this handoff feels more harmonic than rhythmic, it is too open

### Screenshot Set
- `transitions-06a-break-reentry-build-overview`
- `transitions-06b-break-reentry-build-close`

## Step 7: Write The Main Re-Entry (`112 -> 113`)
### Action
On bars `109–113`:
- keep the filtered vocal pickup visible only near the end of `Re-entry Build`
- use a pre-drop cut on the last beat or last half-bar of `112`
- stop any riser before `113`, do not smear over the landing
- let full body return on `113`:
  - full bass
  - reopened harmonic bloom
  - restored drop drum weight

Exact first-pass timing:
1. Place optional filtered pickup so the first clear vocal attack starts at `109.3.4`.
2. Optional repeat: duplicate the pickup so the next attack starts at `110.3.4`.
3. Place `VOC question pre-drop` so the first clear attack starts at `112.3.3`.
4. Keep these pickup clips filtered and quieter than the `Drop B` full chorus.
5. Optional reverse pull: place `VOC reverse tail` so the reversed tail ends exactly at `113.1.1`.
6. Do not place `VOC full chorus clean` anywhere before `113.1.1`.
7. Make bar `111` feel tense without cutting the body away yet.
8. Start the true pre-drop subtraction at `112.4.1`.
9. If the cut is too weak, extend it only to `112.3.3`, not earlier.
10. Kill the riser and release the cut exactly at `113.1.1`.
11. Make the riser clip itself end at `113.1.1`.
12. If the riser audio has a tail that smears past the drop, crop or fade it so the audible tail is gone by `112.4.4`.
13. If the riser is too long to crop cleanly, automate the `FX-Riser` lane volume to drop to `-inf` at `113.1.1`.
14. Make sure the full bass, drums, and bloom chord state all return on `113.1.1`, not staggered loosely across the bar.
16. On the drum lanes:
   - mute `Open Hat` and reduce `Shaker` during the cut from `112.4.1` to `113.1.1`
   - let the fill lane own `112.4.3` and `112.4.4`
   - restore `Kick Body`, `Kick Click`, `Clap`, `Closed Hat`, `Ghost Hat`, `Open Hat`, and `Shaker` together at `113.1.1`
   - mute `Drum Fill FX` again immediately after the landing so the fill does not smear over bar `113`

### Why
This is the most important transition after the first drop.

If it is weak, the whole second half feels like a repeat instead of a payoff.

### Mechanical shape
- bars `109–110`: filtered vocal pickup appears
- bar `111`: tension is already visible
- bar `112`: subtraction and final push
- beat `1` of `113`: full body return

### Screenshot Set
- `transitions-07a-main-redrop-overview`
- `transitions-07b-main-redrop-cut-close`

## Step 8: Write The Minor Lift Boundaries (`64 -> 65` and `128 -> 129`)
### Action
Treat these as pressure increases, not section resets.

For `64 -> 65`:
- add phrase-end fill and slightly more top pressure
- do not add a new harmonic reveal
- do not use a dramatic riser

Exact first-pass move:
- add the phrase-end fill in bar `48`
- add the phrase-end fill in bar `64`
- raise the `Open Hat` or `Shaker` lane by `+1 dB` at `65.1.1`
- do not touch the chord MIDI or bass MIDI at `65.1.1`
- if both `Open Hat` and `Shaker` are already busy, raise only one of them, not both

For `128 -> 129`:
- add phrase-end fill and top release
- keep the section feeling like `Drop B` becoming more released, not a new song

Exact first-pass move:
- add the phrase-end fill in bar `128`
- raise the `Vocal Chops` / `Vocal Throw` `Return B` sends by `+2 dB` at `129.1.1`
- keep that lift through `115.1.1`, then return the sends to their previous levels
- first-pass values:
  - `Vocal Chops` Send B: `-18 dB` -> `-16 dB`
  - `Vocal Throw` Send B: `-16 dB` -> `-14 dB`
- leave `Return C` unchanged on the first pass so the lift comes from vocal release, not extra chord wash
- do not add any new MIDI note at `113.1.1`
- if the lift still feels flat, add one extra `Open Hat` hit at `113.2.3` before inventing a new FX lane

### Why
These boundaries exist to intensify the same world, not replace it.

### Screenshot
- `transitions-08-lift-boundaries`

## Step 9: Write The Outro Handoff (`144 -> 145`)
### Action
On bars `143–145`:
- remove top pressure first
- use a downshifter, reverse tail, or filtered decay if needed
- keep the air whisper alive
- preserve enough drum / bass identity that the outro still feels mixable

Exact first-pass timing:
1. Let the last strongest top-pressure state run through `143.4.4`.
2. Start removing top pressure at `144.1.1`.
3. Reduce the most energetic hats or shakers further by `144.3.1`.
4. Land the stripped outro state at `145.1.1`.
5. Keep the air lane audible past `145.1.1` instead of muting it at the boundary.
6. On the drum lanes:
   - keep `Kick Body`, `Kick Click`, and `Clap` active at `145.1.1`
   - lower or remove `Open Hat` before `145.1.1`
   - keep `Shaker` only if the outro still needs motion after the first pass

### Why
The outro should feel like controlled release, not like the session stopped.

### Mechanical shape
- bar `143`: last strongest top state
- bar `144`: subtraction starts
- beat `1` of `145`: groove remains, emotional lanes reduced

### Screenshot Set
- `transitions-09a-outro-handoff-overview`
- `transitions-09b-outro-handoff-close`

## Step 10: Write The Core Automation Pass
### Action
Write the automation that makes the handoffs actually move:

Drum-bus high-pass:
- filtered intros and transitions
- fully open in main drops

Vocal send levels:
- `Vocal Full Chorus` mostly readable and dry
- `Vocal Throw` gets selected phrase-end throws only

Air-bed level:
- constant but low
- loudest in `Break B`
- keep a whisper in the outro

Exact first-pass automation points:
1. On the drum-bus filter lane, create points at:
   - `31.1.1`: `20 Hz`
   - `32.1.1`: `80 Hz`
   - `32.4.4`: `180 Hz`
   - `33.1.1`: `20 Hz`
   - `48.4.1`: `160 Hz`
   - `49.1.1`: `20 Hz`
   - `96.1.1`: `120 Hz`
   - `97.1.1`: `20 Hz`
   - `111.1.1`: `20 Hz`
   - `112.4.1`: `160 Hz`
   - `113.1.1`: `20 Hz`
2. On the vocal send lanes, create phrase-end throw points at:
   - `68.3.4`
   - `72.3.4`
   - `76.3.4`
   - `132.3.4`
   - `136.3.4`
   - `140.3.4`
3. On the air level lane, create points at:
   - `1.1.1`
   - `33.1.1`
   - `49.1.1`
   - `81.1.1`
   - `97.1.1`
   - `145.1.1`

Chord width / brightness:
- follow the section states already defined in `Part 4`
- do not improvise a new width story here

Volume / mute cuts:
- use only where the boundary job requires subtraction

Ableton action reminder:
1. Press `A` to show automation lanes in Arrangement View.
2. Write automation directly on:
   - `Drum Bus`
   - `Chords`
   - `Vocal Full Chorus`
   - `Vocal Throw`
   - `Air`
3. Name your automation target before drawing points so you do not accidentally write volume automation when you meant to write filter or send automation.

### Why
Transitions are not only FX clips. Most of the excitement comes from controlled automation on the existing lanes.

### Screenshot Set
- `transitions-10a-drum-bus-hp-automation`
- `transitions-10b-vocal-send-automation`
- `transitions-10c-air-width-automation`

### Visual Automation Requirement
- show the drum-bus high-pass automation lane across bars `30–35` so the `31.1.1`, `32.1.1`, `32.4.4`, and `33.1.1` values are visible
- show the re-entry high-pass automation lane across bars `111–113` so the `111.1.1`, `112.4.1`, and `113.1.1` values are visible
- show the vocal send automation around bars `128–131` so the `+2 dB` lift and return are visible

## Step 11: Boundary-Only A/B
### Action
Bounce or loop only the bars around the boundaries:
- `31–33`
- `47–49`
- `63–65`
- `79–81`
- `95–97`
- `111–113`
- `127–129`
- `143–145`

Compare them against the references one boundary at a time.

What to check:
- does `32 -> 33` land like the floor arriving?
- does `48 -> 49` make the intact chorus land?
- does `64 -> 65` lift without revealing new harmony?
- does `80 -> 81` release into `Break B`?
- does `96 -> 97` wake rhythm back up?
- does `112 -> 113` clearly outclass the earlier re-entries?
- does `144 -> 145` remain playable and mixable?

Targeted reference assignment:
- compare `31–33` mostly against `Interplanetary Criminal - Slow Burner` for first-drop pocket and drum-language entry
- compare `47–49` mostly against `KETTAMA - It Gets Better` for physical first-drop impact
- compare `63–65` mostly against `Interplanetary Criminal - Slow Burner` for controlled lift without over-revealing
- compare `79–81` mostly against `Interplanetary Criminal - Slow Burner` for rhythm waking back up after reduced pressure
- compare `111–113` mostly against `KETTAMA - It Gets Better` for physical second-drop impact
- compare `143–145` against all references only for practical DJ-playable stripdown, not for exact sound design

### Expected Answer
- each major boundary should have a different personality
- the biggest transitions should not all use the same tool at the same distance
- the handoffs should already make sense before the final mix and master stages

## Troubleshooting
### Problem: “Every transition sounds the same.”
Fix order:
1. vary subtraction timing
2. vary which lane carries the transition
3. only then change the FX sound itself

### Problem: “The return feels smaller than the build.”
Fix order:
1. shorten or remove the riser
2. reduce the amount of revealed information before the landing
3. make the downbeat cleaner

### Problem: “The Re-entry Build still feels like a second break.”
Fix order:
1. increase rhythmic motion at `81`
2. reduce harmonic openness
3. push the vocal pickup later

### Problem: “The break handoff feels empty instead of open.”
Fix order:
1. strengthen the chord bloom and air level
2. reduce dramatic FX
3. make sure the first beat of the break still has intention

### Problem: “The outro collapses too hard.”
Fix order:
1. keep the air whisper
2. keep drum / bass identity for longer
3. remove emotional lanes before physical ones

## What Must Be Captured For Later Lesson Conversion
- one screenshot per major boundary
- one screenshot of the core automation lanes
- one bounce containing only the boundary bars
- one note on which transitions required subtraction instead of added FX
