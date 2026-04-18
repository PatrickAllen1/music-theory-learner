# UKG 140 OG Bounce Driver: Tutorial Part 0 — Setup

## Purpose
Teach the learner how to prepare an Ableton session for `ukg-140-og-bounce-driver` before any real music is written.

This part should make the project:
- organized
- reference-ready
- routing-safe
- headroom-safe

It should not invent any musical decisions. It only prepares the environment so later parts can move quickly without re-solving routing, return structure, or reference workflow.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)

## Outcome
By the end of this part, the learner should have:
- a `140 BPM` Ableton 12 session
- organized groups for the major lanes
- separate drum lanes ready from the start for later mixing
- all four returns named and ready
- references loaded and gain-trimmed
- a clean premaster lane with headroom

## Time Estimate
- `10–20 minutes`

## Prerequisites
- learner can open Ableton and save a project
- learner can drag audio files into Ableton
- no routing vocabulary is assumed; this chapter defines the words it uses

## What The Learner Should Understand Before Starting
This setup chapter is not busywork.

If the session is vague at the start:
- later parts get slower
- screenshots get messier
- references get forgotten
- export organization becomes a problem right when the project gets good

The point is to remove friction before creativity starts.

Timing-language rule used throughout this tutorial:
- when a step is talking about a clip or piano roll, positions like `1.1.1` mean the start of that clip
- when a step is talking about the full song in Arrangement View, positions like `100.1.1` mean absolute song bars
- do not mix those two time systems up while entering MIDI

Plain-English Ableton words used in this tutorial:
- `track`: one horizontal lane in Ableton
- `group`: the folder-like parent lane Ableton creates when you select tracks and press `Cmd+G` on Mac or `Ctrl+G` on Windows
- `bus`: in this tutorial, `bus` means a `group` that several child tracks feed into so you can control them together
- `return`: one of Ableton's send-effect lanes at the far right, usually named `A`, `B`, `C`, `D`; you feed signal into it with send knobs
- `premaster`: the last lane before the actual Ableton `Master`; this is where the tutorial keeps headroom under control before mastering
- `sidechain`: a compressor or level-control device that turns one lane down when another lane, usually the kick, hits

## Reference Axis
Load the four references now:
- `KETTAMA - It Gets Better`
- `Interplanetary Criminal - Slow Burner`
- `Y U QT - U Belong 2 Me (4x4 Mix)`
- `Sammy Virji - I Guess We're Not the Same`

Each one has a job:
- KETTAMA: pressure
- IC: groove pocket
- Y U QT: bass roll
- Virji: hook / harmony readability

## Step 1: Start The Session At The Correct Tempo
### Action
1. Create a new Ableton session.
2. Set the tempo to `140 BPM`.
3. Save the project immediately into the intended project folder.

### Why
Tempo and file location are foundational decisions, not details to clean up later.

### Screenshot
- `setup-01-tempo-and-project-save`

## Step 2: Create The Core Groups
### Action
1. Create the top-level lane groups or clearly named lane tracks in this order:
   - `Drums`
   - `Bass`
   - `Chords`
   - `Hook`
   - `Answer`
   - `Air`
   - `FX`
   - `Premaster`
2. Rename each one immediately:
   - click the track or group header once
   - press `Cmd+R` on Mac or `Ctrl+R` on Windows
   - type the exact lane name
   - press `Enter`
3. Color each lane header now so the session is readable later:
   - right-click the track or group header
   - choose a color swatch
   - keep one color family per lane so screenshots stay readable
4. Inside the `Drums` group, create separate tracks from the start:
   - `Kick Body`
   - `Kick Click`
   - `Clap`
   - `Closed Hat`
   - `Ghost Hat`
   - `Open Hat`
   - `Shaker`
   - `Drum Fill FX`
5. Rename and color those drum tracks the same way:
   - single-click the track header
   - `Cmd+R` / `Ctrl+R`
   - type the exact name
   - right-click the header and assign a color
6. Keep the drum tracks in that exact top-to-bottom order.
7. If you do not know what a `group` is yet, do this:
   - create the child tracks first
   - Shift-click the tracks you want together
   - press `Cmd+G` on Mac or `Ctrl+G` on Windows
   - Ableton creates one parent folder lane above them
   - that parent folder lane is the `group`
   - later, when that group is used as one shared control lane, the tutorial may also call it a `bus`

### Why
This mirrors the lane logic used throughout the tutorial and keeps screenshots and routing readable.

### Screenshot
- `setup-02-core-groups`

## Step 3: Create The Return Structure
### Action
Create and name these returns:
- `Return A`: short room / ambience
- `Return B`: short plate
- `Return C`: long filtered hall
- `Return D`: filtered delay

If you do not know what a `return` is yet:
1. Look at the far right side of Ableton's mixer.
2. The vertical lanes named `A`, `B`, `C`, `D` are return tracks.
3. Later, when the tutorial says "send the hook to `Return B`," it means turn up the `B` send knob on the `Hook` lane.

### Why
The tutorial expects these returns to exist from the beginning so later chapters can reference them without rebuilding session plumbing.

### Screenshot
- `setup-03-returns`

## Step 4: Build The Bus Routing
### Action
Build the bus structure explicitly.

First, create the buses:
1. If the `Drums` parent group is not already named `Drum Bus`, click the parent group header, press `Cmd+R` on Mac or `Ctrl+R` on Windows, and rename it `Drum Bus`.
2. If the `Bass` parent group is not already named `Bass Bus`, click the parent group header, press `Cmd+R` / `Ctrl+R`, and rename it `Bass Bus`.
3. Select the `Chords`, `Hook`, `Answer`, and `Air` groups together.
4. Press `Cmd+G` on Mac or `Ctrl+G` on Windows.
5. Ableton creates one new parent group around those four groups.
6. Rename that new parent group `Music Bus`.
7. Keep `Premaster` as its own final audio/group lane before Ableton's real `Master`.

Then route the buses:
1. On `Drum Bus`, find the `Audio To` dropdown in the mixer.
2. Set `Audio To` to `Premaster`.
3. On `Bass Bus`, set `Audio To` to `Premaster`.
4. On `Music Bus`, set `Audio To` to `Premaster`.
5. On `Premaster`, leave `Audio To` set to `Master`.

The result should be:
- `Kick Body`, `Kick Click`, `Clap`, hats, shaker, and fills live inside `Drum Bus`
- bass layers live inside `Bass Bus`
- `Chords`, `Hook`, `Answer`, and `Air` live inside `Music Bus`
- `Drum Bus`, `Bass Bus`, and `Music Bus` all feed `Premaster`
- `Premaster` feeds Ableton's real `Master`

Plain-English routing translation:
- when the tutorial says "put EQ on `Drum Bus`," click the `Drum Bus` parent lane, not `Kick Body`
- when it says "send signal to `Return C`," use the `C` send knob on the source track or group
- when it says "route to `Premaster`," make the bus output feed the `Premaster` lane before the real Ableton `Master`

### Why
The tutorial later mixes by bus. If the routing is improvised halfway through the build, the learner will end up redoing screenshots and balances.

### Screenshot
- `setup-04-bus-routing`

## Step 5: Load The References And Gain-Trim Them
### Action
1. Create four audio tracks for the references.
2. Name them:
   - `REF KETTAMA pressure`
   - `REF IC groove`
   - `REF YUQT bass roll`
   - `REF Virji hook harmony`
3. Select those four reference tracks together.
4. Press `Cmd+G` on Mac or `Ctrl+G` on Windows.
5. Rename the new parent group `References`.
6. Route the `References` group directly to Ableton's real `Master`, not to `Premaster`.
7. Load the four reference tracks onto the four reference lanes.
8. Put a `Utility` on each reference lane.
9. Start by pulling each reference down by about `-10 dB` on its `Utility`.
10. Solo one reference at a time and compare it against your empty session at the same monitor volume.
11. If a reference still feels obviously too loud, pull it down another `2–3 dB`.
12. Leave a note in the track name if one reference needed noticeably more trim than the others.
13. Mute the `References` group after trimming.
14. Leave it muted by default. Unmute it only during A/B checks.

### Why
References only help if they are in the session and usable from the start.

### Rule
- do not wait until the mix stage to load references

### Screenshot Set
- `setup-05a-reference-tracks`
- `setup-05b-reference-gain-trim`

## Step 6: Prepare The Premaster Lane
### Action
1. Click the `Drum Bus` mixer output dropdown labeled `Audio To`.
2. Choose `Premaster`.
3. Repeat the same `Audio To -> Premaster` routing on `Bass Bus`.
4. Repeat the same `Audio To -> Premaster` routing on `Music Bus`.
5. Click the `Premaster` mixer output dropdown.
6. Make sure `Premaster` is routed to Ableton's real `Master`.
7. Do not route `References` to `Premaster`; references should bypass your mix processing.
8. Put a `Utility` on the premaster.
9. Leave headroom; do not place a limiter here yet unless it is clearly bypassed and documented as later-stage only.

### Why
The session should start with headroom discipline, not loudness chasing.

### Rule
- no “mixing into final loudness” this early

### Screenshot
- `setup-06-premaster-headroom`

## Step 7: Add Timeline Markers For The Frozen Section Map
### Action
1. Switch to Arrangement View if you are not already there.
2. Move the playhead to bar `1.1.1`.
3. Right-click in the scrub area above the timeline and choose `Add Locator`.
4. Click the new locator flag once.
5. Press `Cmd+R` on Mac or `Ctrl+R` on Windows.
6. Rename it exactly:
   - `1–16 Intro A`
7. Repeat that process at these exact bar starts:
   - `17.1.1` -> `17–32 Intro B`
   - `33.1.1` -> `33–48 Drop A`
   - `49.1.1` -> `49–64 Drop A Lift`
   - `65.1.1` -> `65–80 Break`
   - `81.1.1` -> `81–96 Re-entry Build`
   - `97.1.1` -> `97–112 Drop B`
   - `113.1.1` -> `113–128 Drop B Lift`
   - `129.1.1` -> `129–144 Outro`
8. After each locator is created and renamed, color it:
   - right-click the locator flag
   - choose a color swatch
   - keep warm colors for drop sections and cooler colors for intro/break sections if that helps you read the song faster
9. Read the locator list back to yourself from top to bottom and make sure there are exactly `9` locators.

### Why
Even before writing parts, the project should already know what song shape it is aiming toward.

### Screenshot
- `setup-07-timeline-markers`

## Step 8: Run The Zero-Music Checkpoint
### Action
With no real music written yet:
1. Press play from bar `1.1.1` for a few empty bars so you can see the session moving.
2. Stop playback and visually confirm the buses and returns are visible in the mixer.
3. Click each reference track once and say its job out loud:
   - `KETTAMA` = pressure
   - `IC` = groove pocket
   - `Y U QT` = bass roll
   - `Virji` = hook / harmony readability
4. Make sure no limiter is active on the premaster.

### Expected Answer
- the session feels organized, not improvised
- the references are ready to use
- there is no limiter-led loudness bias yet

### Screenshot
- `setup-08-zero-music-ready-state`

## Troubleshooting
### Problem: “The project already feels disorganized.”
Fix order:
1. rename tracks and groups
2. restore the lane order
3. clean the routing before adding any music

### Problem: “The references are much louder.”
Fix order:
1. trim them with `Utility`
2. re-check at a stable monitoring level
3. only then start comparing tone or groove

### Problem: “I want to start building sounds first.”
Fix order:
1. finish this setup pass
2. save the clean project state
3. then move into `Part 1`

## What Must Be Captured For Later Lesson Conversion
- project tempo screenshot
- group / routing screenshot
- return-track screenshot
- reference-track screenshot
- premaster lane screenshot
