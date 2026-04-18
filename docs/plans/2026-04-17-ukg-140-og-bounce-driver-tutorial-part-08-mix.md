# UKG 140 OG Bounce Driver: Tutorial Part 8 — Mix

## Purpose
Teach the learner how to mix `ukg-140-og-bounce-driver` so it feels:
- heavy
- open
- club-readable
- translation-safe

This part should turn the arranged song into a controlled premaster by locking:
- gain staging
- bus structure
- sidechain network
- EQ ownership
- stereo placement
- return / FX balance
- reference A/B workflow

It should not try to solve unresolved sound-selection problems with processing. If a lane still fundamentally sounds wrong, replace or simplify it before pushing the mix harder.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-full-song-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-part-07-transitions-toolkit.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-07-transitions-toolkit.md)

## Outcome
By the end of this part, the learner should have:
- one working premaster with healthy headroom
- stable buses for:
  - drums
  - bass
  - music
  - FX / returns
  - premaster
- a working sidechain network
- a believable stereo map
- one premaster bounce plus one mono-check bounce

## Time Estimate
- `60–90 minutes`

## Prerequisites
- all arrangement decisions are stable enough that the learner is no longer rewriting sections
- the learner has completed or can reference:
  - `Part 1` foundation
  - `Part 2` groove
  - `Part 3` bass floor
  - `Part 4` harmonic bed
  - `Part 5` identity
  - `Part 6` arrangement
  - `Part 7` transitions
- the learner can use:
  - `EQ Eight`
  - `Glue Compressor`
  - `Saturator`
  - `Utility`
  - send / return routing

## What The Learner Should Understand Before Starting
Mixing here is not:
- making everything loud
- solving bad sound selection with EQ alone
- adding top end because the low-mid feels crowded

Mixing here is:
- separation
- lane ownership
- depth control
- translation

If the learner tries to “win” the mix with mastering tricks before the buses and balances are right, the track will get louder and worse at the same time.

Plain-English Ableton words used in this chapter:
- `bus`: a parent group track that several child tracks feed into
- `Drum Bus`: the parent group above the kick, clap, hats, shaker, and fill tracks
- `Bass Bus`: the parent group above `Bass Sub` and `Bass Mid`
- `Music Bus`: the parent group above `Chords`, `Hook`, `Answer`, and `Air`
- `return`: one of the `A/B/C/D` send-effect tracks on the far right side of Ableton
- `sidechain`: a compressor or level-control device that turns one lane down when the kick hits

## Reference Axis
Judge one axis at a time:

- `KETTAMA - It Gets Better`
  - kick weight
  - low-end size
  - density before brightness
- `Interplanetary Criminal - Slow Burner`
  - ghost-hat drag
  - loop bounce
  - phrase-end pocket
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - rhythmic-first bass roll
  - stable sub underneath
- `Sammy Virji - I Guess We're Not the Same`
  - hook clarity
  - harmonic readability

## Files / Assets Needed
- full arranged session
- buses:
  - `Drum Bus`
  - `Bass Bus`
  - `Music Bus`
  - `Premaster`
- returns:
  - `Return A`: short room / ambience
  - `Return B`: short plate
  - `Return C`: long filtered hall
  - `Return D`: filtered delay
- one `Utility` on the premaster for mono checks

## Mix Targets
### Gain staging
- individual tracks generally around `-12` to `-8 dBFS` peak before major bus work
- buses around `-8` to `-6 dBFS` peak
- premaster around `-6 dBFS` peak headroom

### Band ownership
- `30–90 Hz`: kick + sub
- `120–200 Hz`: bass character leads
- `200–300 Hz`: chord warmth can live more confidently
- `300 Hz–2 kHz`: chord emotion + hook readability
- `2–6 kHz`: presence owner
- `8 kHz+`: air

### Stereo map
- kick: mono / center
- sub: mono / center
- mid-bass: mono to narrow stereo above crossover
- chords: medium-wide to wide depending on section state
- hook: center to slight stereo
- answer: slightly wider than hook, still controlled
- air: wide but quiet

## Step 1: Set Gain Staging Before Processing
### Action
Pull all track and group levels into the working range:
- track peaks around `-12` to `-8 dBFS`
- buses around `-8` to `-6 dBFS`
- premaster around `-6 dBFS`

Do this before:
- bus compression
- saturation
- premaster processing

Ableton action order:
1. Disable or bypass any non-essential loudness plugins on the premaster first.
2. Play the loudest drop section, usually around `97.1.1` to `113.1.1`.
3. Watch the channel meters while adjusting the plain track faders, not the master fader.
4. Bring the loudest individual lanes down first:
   - kick
   - bass
   - hook if needed
5. Only after track levels are reasonable, adjust the bus levels.

### Why
If the session is already too hot before the buses exist, every later decision gets biased by level.

### Screenshot
- `mix-01-gain-staging`

## Step 2: Build The Bus Structure
### Action
Route the session so each major job owns a bus:
- `Drum Bus`
- `Bass Bus`
- `Music Bus`
- `Premaster`

Bus membership:
- `Drum Bus`: kick, clap, hats, shaker, loops
- `Bass Bus`: sub + mid-bass / bass harmonic layer
- `Music Bus`: chords, hook, answer, air

If the learner wants `Air` on its own group, that is acceptable, but the first-pass tutorial route should still feed it into the `Music Bus`.

Exact Ableton translation:
1. Click the child tracks you want together.
2. Press `Cmd+G` on Mac or `Ctrl+G` on Windows.
3. Ableton creates a parent group lane above them.
4. Rename that parent lane to `Drum Bus`, `Bass Bus`, or `Music Bus`.
5. When this chapter says "put EQ on the bus," click that parent group lane, not the child track below it.

Ableton action order:
1. Select the relevant tracks.
2. Group them with `Cmd+G` on Mac or `Ctrl+G` on Windows if the buses do not already exist.
3. Rename each bus immediately with `Cmd+R` / `Ctrl+R`.
4. Drag the buses so they appear in this order:
   - `Drum Bus`
   - `Bass Bus`
   - `Music Bus`
   - `Premaster`
5. Collapse and expand each bus once so you can visually confirm the right lanes are inside it.

### Why
The buses are where the track starts behaving like a record instead of a stack of channels.

### Screenshot
- `mix-02-bus-routing`

## Step 3: Set The Drum Bus Chain
### Action
Build the `Drum Bus` in this order:
1. `EQ Eight`
2. `Glue Compressor`
3. `Saturator` or soft clip stage
4. `Utility`

Exact Ableton click path:
1. Click the `Drum Bus` group lane.
2. Open the device area at the bottom.
3. Drag `EQ Eight` onto the lane first.
4. Drag `Glue Compressor` to the right of it.
5. Drag `Saturator` to the right of that.
6. Drag `Utility` last.

Starting direction:
- `EQ Eight`
  - remove obvious sub spill below the kick lane only if it is really there
- `Glue Compressor`
  - ratio `2:1` or `4:1`
  - slower attack so the transients still punch
  - release timed to groove, not maximum pumping
- `Saturator`
  - enough to add density
  - not enough to flatten hats and clap movement

First-pass settings:
- `Glue Compressor`
  - ratio `2:1`
  - attack: use a slower setting
  - release: start on `Auto`
- `Saturator`
  - start at the first clearly audible step above zero, not a heavy drive move

### Why
The drum bus should feel denser and more unified, but the groove still needs to breathe.

### Screenshot Set
- `mix-03a-drum-bus-overview`
- `mix-03b-drum-bus-devices`

## Step 4: Set The Bass Bus Chain
### Action
Build the `Bass Bus` in this order:
1. `EQ Eight`
2. `Saturator`
3. sidechain / control compression
4. `Utility`

Exact Ableton click path:
1. Click the `Bass Bus` group lane.
2. Add the devices in this order:
   - `EQ Eight`
   - `Saturator`
   - compressor or control device for sidechain
   - `Utility`

Starting direction:
- `EQ Eight`
  - keep the sub clean
  - let the mid layer own character above the crossover
- `Saturator`
  - most extra density should happen here
  - not on the sine sub patch itself
- `Utility`
  - keep the low end centered

### Why
The bass bus should add character and cohesion without blurring the sub.

### Screenshot Set
- `mix-04a-bass-bus-overview`
- `mix-04b-bass-bus-devices`

## Step 5: Set The Music Bus Chain
### Action
Build the `Music Bus` in this order:
1. `EQ Eight`
2. `Glue Compressor` or light bus compression
3. tonal saturation
4. `Utility`

Exact Ableton click path:
1. Click the `Music Bus` group lane.
2. Add the devices in this order:
   - `EQ Eight`
   - `Glue Compressor`
   - tonal saturation device
   - `Utility`

Starting direction:
- keep the music bus breathing around the kick
- avoid flattening:
  - chord bloom
  - hook punctuation
  - answer clarity

First-pass settings:
- keep compression extremely light on the `Music Bus`
- if the bus already feels glued without compression, leave the compressor bypassed on the first pass and only use EQ + Utility

### Why
The music bus is where the emotional layers become one world without becoming one slab.

### Screenshot Set
- `mix-05a-music-bus-overview`
- `mix-05b-music-bus-devices`

## Step 6: Write The Sidechain Network
### Action
Use the kick as the source for:
- kick -> sub: deepest duck
- kick -> bass mid: lighter duck
- kick -> chords: gentle duck
- kick -> air: very light duck

Plain-English sidechain translation:
- the `kick` is the trigger lane
- the other lane is the lane being turned down briefly
- in Ableton this usually means putting a compressor on the lane you want to duck, opening its sidechain panel, and choosing the kick track as the source

Starting direction:
- sub release roughly matched to the kick tail:
  - around `90–120 ms`
- bass mid:
  - enough duck that kick and bass breathe together
  - not so much that the bass loses rhythmic life between kicks
- chords / air:
  - just enough to keep the groove clear

Ableton action order:
1. On `Bass Sub`, drop in a compressor that supports sidechain.
2. Open the sidechain panel.
3. Choose the kick track as the sidechain input.
4. Start with:
   - ratio around `4:1`
   - fast attack
   - release around `100 ms`
5. Repeat on `Bass Mid`, but start lighter:
   - ratio around `2:1`
   - similar attack
   - release around `90–110 ms`
6. On `Chords`, start gentler still:
   - ratio around `2:1`
   - release around `120–180 ms`
7. On `Air`, use the lightest version of all:
   - enough that the ceiling breathes, not enough that it audibly pumps
8. Solo-check each lane with the kick and then return to full mix context before deciding the setting is done.

### Why
Sidechain here is for breathing and lane clarity, not for theatrical pumping.

### Screenshot Set
- `mix-06a-sidechain-routing`
- `mix-06b-sidechain-settings`

## Step 7: Carve The Low-Mid Ownership
### Action
Use the band split as the first-pass ownership map:
- `120–200 Hz`: let bass character lead
- `200–300 Hz`: let chord warmth and some hook body live more confidently

Practical move order:
1. solo-check the low-mid relationship between bass mid and chord bed
2. cut the chord bed first if the low-mid clouds
3. only then thin the bass mid if needed

Exact first-pass move:
1. Put `EQ Eight` on the chord bed or `Music Bus`.
2. Start by trimming a little around `220–280 Hz`.
3. Re-listen with bass and chords together.
4. Only if the cloud is still there, trim the bass mid slightly lower in the range rather than gutting the whole chord layer.

### Why
The low-mid is where warmth and mud live in the same room.

### Rule
- do not solve a cloudy low-mid by just adding treble

### Screenshot
- `mix-07-low-mid-ownership`

## Step 8: Lock The Stereo Policy
### Action
Set the stereo image according to the frozen map:
- kick: mono / center
- sub: mono / center
- mid-bass: mono to narrow stereo above the crossover
- chords:
  - `Drop A` around `120%`
  - `Break` around `150%`
  - `Re-entry Build` around `130%`
  - `Drop B` around `140%`
- hook: center to slight stereo
- answer: slightly wider than hook
- air: wide but quiet

### Why
Width should reinforce the arrangement, not overwrite it.

### Rule
- if the track only sounds exciting in stereo, the center image is weak

### Screenshot Set
- `mix-08a-stereo-map-overview`
- `mix-08b-width-by-lane`

## Step 9: Balance The Returns
### Action
Use the returns for support, not wash.

`Return A: short room / ambience`
- light drum glue only

`Return B: short plate`
- hook / answer family
- keep pre-delay short enough that the attack stays readable

`Return C: long filtered hall`
- chords + air
- high-pass and low-pass it so it adds space without mud

`Return D: filtered delay`
- phrase-end throws only
- avoid constant wash

Ableton action order:
1. Mute all sends first.
2. Bring `Return A` in gently on drums.
3. Bring `Return B` in on hook and answer.
4. Bring `Return C` in on chords and air.
5. Leave `Return D` off until phrase-end moments are working.
6. If a return sounds exciting in solo but clouds the full mix, lower the send before touching the return plugin.

### Why
The returns create depth and section state. They should not cover up weak lane balances.

### Screenshot Set
- `mix-09a-return-overview`
- `mix-09b-return-c-filtering`

## Step 10: Reference Loudness-Matched A/B
### Action
Loudness-match the references before judging tone or weight.

Practical method:
1. start by pulling the references down around `-10 dB` on `Utility`
2. compare at the same monitoring level every time
3. judge one axis at a time:
  - pressure
  - groove pocket
  - bass roll
  - hook / harmony clarity
4. Do the comparison from the same song location each time:
   - use `Drop A` against the first-drop section of the reference
   - use `Drop B` against a full-drop section of the reference
5. Write down one short note per reference instead of trying to remember all four judgments in your head.

Exact Ableton mono-check action:
1. Put `Utility` on the `Premaster` if it is not already there.
2. Use the `Mono` button on that `Utility`.
3. Turn `Mono` on for the check.
4. Turn `Mono` back off before normal balancing continues.

### Why
Without loudness matching, the loudest master wins every argument whether it deserves to or not.

### Screenshot
- `mix-10-reference-gain-match`

## Step 11: Translation Checks
### Action
Check the premaster in:
- mono
- small speaker / phone
- everyday playback if possible

Exact mono-check action:
1. Put `Utility` last on the premaster if it is not already there.
2. Turn `Mono` on.
3. Listen through:
   - a drop
   - the break
   - the `96 -> 97` re-entry
4. Turn `Mono` back off before making stereo decisions again.

Mono tool:
- put `Utility` last on the premaster
- use it to check mono collapse quickly
- also audition the `Bass` group in mono while balancing kick and sub

What to listen for:
- does the kick still land with authority?
- does the sub still read as one center line?
- does the hook remain intelligible?
- does the track still feel open without relying on width tricks?

### Why
A mix that only works on the main speakers is not finished.

### Screenshot Set
- `mix-11a-premaster-mono-check`
- `mix-11b-bass-group-mono-check`

## Step 12: Bounce The Premaster Checkpoints
### Action
Export checkpoint bounces into `Exports / Checkpoints`:
- `kick + air`
- `full drums`
- `drums + bass`
- `drums + bass + chords`
- `Drop A`
- `Drop B`
- `premaster`

### Why
These exports are:
- the fastest way to hear whether the mix is progressing
- the source material for later tutorial delivery
- the safety net if a later change makes the record worse

### Expected Answer
- the premaster should feel heavy and open without relying on the limiter
- the low-mid should feel controlled, not cloudy
- the track should still read by axis against the references

## Troubleshooting
### Problem: “The track only works loud.”
Fix order:
1. rebalance buses
2. reduce over-compression
3. re-check low-mid ownership

### Problem: “The low-mid feels muddy.”
Fix order:
1. cut the chord bed first
2. confirm bass mid is not too wide or too loud
3. only then add any top correction

### Problem: “The drums lost their groove.”
Fix order:
1. reduce drum-bus compression
2. reduce parallel density
3. check whether hats and clap got flattened by saturation

### Problem: “The hook is hard to read.”
Fix order:
1. reduce chord midrange around it
2. reduce answer density
3. check plate / delay is not washing the attack

### Problem: “The mix folds in mono.”
Fix order:
1. narrow the wrong lanes
2. re-check mid-bass and air width
3. confirm the important identity still exists in the center

## What Must Be Captured For Later Lesson Conversion
- bus chain screenshots
- sidechain-routing screenshots
- EQ ownership screenshot
- stereo-map screenshot
- premaster A/B notes
- checkpoint bounces
