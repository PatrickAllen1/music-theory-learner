# UKG 140 OG Bounce Driver: Tutorial Part 5 - Vocal Sample, Full Chorus, and Chops

## Purpose
Teach the learner how to turn the chosen `D minor` vocal into the emotional identity of the track.

This part no longer teaches a synth hook or synth answer.

The current track uses two versions of the same vocal source:
- a clean intact chorus version
- a dry chopped-fragment version

The intact chorus is the singable payoff.

The chops are the club edit language around that payoff.

## Outcome
By the end of this part, the learner should have:
- one `Vocal Audition` audio track
- one `Vocal Full Chorus` audio track
- one `Vocal Chops` audio track
- one `Vocal Throw` audio track
- one muted `Vocal Guide` MIDI track
- one clean intact chorus clip named `VOC full chorus clean`
- one set of chopped clips named by function, not by lyric text
- first-pass vocal placements across `Break A`, `Drop A`, `Drop A Lift`, `Break B`, `Re-entry Build`, `Drop B`, and `Drop B Lift`

## Time Estimate
- `90-150 minutes`

Do not rush this part.

The vocal is now the record's identity lane.

## Current Vocal Source Assumption
Use this lesson for the current source choice:
- source type: lossless vocal / acapella
- source key: `D minor`
- project key: `D minor`
- project tempo: `140 BPM`
- vocal role: recognizable chorus plus chopped club edits

Because the current vocal is already in `D minor`, the first-pass transpose value is:
- `0 semitones`

If you later test a vocal in a different key, use this quick transpose guide:
- `D# minor` or `Eb minor` to `D minor`: transpose `-1`
- `C# minor` or `Db minor` to `D minor`: transpose `+1`
- `E minor` to `D minor`: transpose `-2`
- `C minor` to `D minor`: transpose `+2`

## Copyright-Safe Clip Labels
Do not name the public tutorial clips with full copyrighted lyric lines.

Use functional names:
- `VOC full chorus clean`
- `VOC mystery statement`
- `VOC mystery seed`
- `VOC question pre-drop`
- `VOC chop A`
- `VOC chop B`
- `VOC exposed core`
- `VOC vulnerable phrase`
- `VOC reverse tail`
- `VOC throw`

You can write the actual lyric in your private Ableton session if you want, but the tutorial file should stay functional.

## What These Words Mean
### Vocal Audition
`Vocal Audition` is a temporary workbench track.

Use it to test:
- whether the vocal is in time
- whether the key feels right
- whether the phrase fights the bass
- whether the phrase has useful chop points

Do not build the final arrangement on this track.

After a clip is approved, copy it to one of the real vocal tracks.

### Full Chorus
`VOC full chorus clean` means the chorus stays intact.

You are not slicing every word.

The point is that the room can recognize and sing the hook.

It should sound:
- readable
- emotional
- forward
- less aggressive than the chop tracks

It should not sound:
- like a random one-word stab
- like a notification beep
- like a thin acapella pasted on top with no body
- like it is being chopped before the listener understands the song

### Chop
A chop is a short piece cut out of the vocal.

It can be:
- one word
- one short phrase
- the end of a phrase
- a breath
- a tail
- a reversed tail

The chop track is allowed to be more edited, dry, gated, pitched, reversed, or delayed.

### Throw
A throw is a short response after a main phrase.

It usually happens at the end of a phrase.

It is quieter or more delayed than `Vocal Full Chorus`.

It should feel like punctuation, not a second lead vocal.

### Bar Position
Arrangement positions like `49.1.1` mean:
- bar `49`
- beat `1`
- first subdivision of the beat

These are arrangement timeline positions, not piano-roll note names.

## Step 1: Create The Vocal Tracks
### Action
Create four audio tracks and one MIDI guide track.

In Ableton:
1. Press `Cmd+T` on Mac or `Ctrl+T` on Windows to create an audio track.
2. Rename it `Vocal Audition`.
3. Press `Cmd+T` / `Ctrl+T` again.
4. Rename it `Vocal Full Chorus`.
5. Press `Cmd+T` / `Ctrl+T` again.
6. Rename it `Vocal Chops`.
7. Press `Cmd+T` / `Ctrl+T` again.
8. Rename it `Vocal Throw`.
9. Press `Cmd+Shift+T` on Mac or `Ctrl+Shift+T` on Windows to create a MIDI track.
10. Rename it `Vocal Guide`.
11. Mute `Vocal Guide`; it is only a visual ruler.

Route the audio tracks:
1. On `Vocal Audition`, set `Audio To` to `Music Bus`.
2. On `Vocal Full Chorus`, set `Audio To` to `Music Bus`.
3. On `Vocal Chops`, set `Audio To` to `Music Bus`.
4. On `Vocal Throw`, set `Audio To` to `Music Bus`.

Set first-pass faders:
- `Vocal Audition`: `-12 dB`
- `Vocal Full Chorus`: `-10 dB`
- `Vocal Chops`: `-14 dB`
- `Vocal Throw`: `-18 dB`

If you do not know what a fader is:
- it is the vertical volume control at the bottom of the track in Ableton's mixer
- numbers like `-10 dB` are track volume values
- click the number under the track meter and type the value

### Why
Separate vocal tracks let you process the intact chorus differently from the chopped fragments.

The clean chorus needs to be readable.

The chops need to be tighter and more aggressive.

### Checkpoint
You should now see:
- `Vocal Audition`
- `Vocal Full Chorus`
- `Vocal Chops`
- `Vocal Throw`
- `Vocal Guide`

## Step 2: Import The Vocal Onto The Audition Track
### Action
1. Drag the lossless vocal file into Arrangement View.
2. Drop it on `Vocal Audition`.
3. Put the first clip start at `1.1.1`.
4. Double-click the clip to open Clip View.
5. Turn `Warp` on.
6. Set Warp Mode to `Complex` or `Complex Pro`.
7. If `Complex Pro` is available, use it for full phrases.
8. If `Complex Pro` is not available, use `Complex`.
9. Set `Transpose` to `0 st`.

If the clip plays too early or too late:
1. Find the first real vocal attack in the waveform.
2. Right-click that point.
3. Choose `Set 1.1.1 Here` if Ableton offers it.
4. If not, drag the clip start marker so the first vocal attack lines up with the grid.

### Why
The vocal has to be grid-aware before you chop it.

If the vocal is not aligned before chopping, every later chop placement becomes confusing.

### Checkpoint
Loop `1.1.1-5.1.1`.

The vocal should stay in time for at least `4` bars.

It does not need to sound mixed yet.

## Step 3: Build Two Processing Chains
### Action
On `Vocal Full Chorus`, start clean.

Put these devices in this order:
1. `EQ Eight`
2. `Compressor`
3. optional `De-Esser` if you have one

First-pass `EQ Eight` settings:
- high-pass around `120 Hz`
- do not boost anything yet
- if the vocal is muddy, cut around `250-400 Hz` by `1-3 dB`

First-pass `Compressor` settings:
- ratio: `2:1`
- attack: `10-20 ms`
- release: `80-150 ms`
- aim for `2-4 dB` gain reduction only on louder phrases

On `Vocal Chops`, make the chain tighter.

Put these devices in this order:
1. `EQ Eight`
2. `Compressor`
3. optional `Saturator`
4. optional `Gate`

First-pass `Vocal Chops` settings:
- high-pass around `150 Hz`
- cut mud around `250-500 Hz` if needed
- keep the dry chop more forward than the reverb
- add drive only if the chop needs bite

On `Vocal Throw`, make the chain wider and more delayed later.

For now:
- high-pass around `180 Hz`
- fader stays lower than `Vocal Full Chorus`
- sends can be added after the dry placement works

### Why
The full chorus and the chops have different jobs.

One chain cannot do both jobs well.

## Step 4: Cut The Full Chorus Clean Clip
### Action
On `Vocal Audition`, find the complete chorus section you want the room to recognize.

Do not chop it word-by-word.

Make one clean clip:
1. Put the playhead at the start of the chorus.
2. Press `Cmd+E` / `Ctrl+E` to split.
3. Put the playhead just after the end of the chorus tail.
4. Press `Cmd+E` / `Ctrl+E` again.
5. Click the chorus clip.
6. Duplicate or copy it to `Vocal Full Chorus`.
7. Rename the clip `VOC full chorus clean`.

If you cannot rename the audio clip directly:
- rename the track region or add a locator note
- the important part is that you can identify it later

### Full-Chorus Timing Target
The first clean chorus should occupy `Drop A`:
- start at `49.1.1`
- end before `65.1.1`

If the chorus has four clear internal lines, use this first-pass anchor map:
- line `1` attack near `49.1.1`
- line `2` attack near `53.1.1`
- line `3` attack near `57.1.1`
- line `4` attack near `61.1.1`

Do not force the line anchors if the natural vocal phrasing is slightly ahead or behind.

The important rule:
- the chorus begins cleanly at `49.1.1`
- the final tail does not spill messily over `65.1.1`

### Why
The first drop should let the song arrive.

This is where the track becomes singable.

## Step 5: Cut The Chop Vocabulary
### Action
Return to `Vocal Audition`.

Cut shorter clips and copy them to `Vocal Chops` or `Vocal Throw`.

Create these functional clips:

| Clip name | Track | Function |
|---|---|---|
| `VOC mystery statement` | `Vocal Chops` | first readable setup phrase |
| `VOC mystery seed` | `Vocal Chops` | shorter unresolved setup fragment |
| `VOC question pre-drop` | `Vocal Chops` | phrase that asks for the drop |
| `VOC chop A` | `Vocal Chops` | first devotional hook fragment |
| `VOC chop B` | `Vocal Chops` | second devotional hook fragment |
| `VOC exposed core` | `Vocal Chops` | most emotionally direct short phrase |
| `VOC vulnerable phrase` | `Vocal Chops` | intimate phrase for `Break B` |
| `VOC reverse tail` | `Vocal Throw` | reversed pull into a drop |
| `VOC throw` | `Vocal Throw` | short phrase-end answer |

How to make each chop:
1. On `Vocal Audition`, find the phrase.
2. Put the playhead just before the phrase attack.
3. Press `Cmd+E` / `Ctrl+E`.
4. Put the playhead just after the phrase ends.
5. Press `Cmd+E` / `Ctrl+E`.
6. Copy the new clip to the correct vocal track.
7. Drag the clip start so the first consonant or vowel attack is clean.
8. Add a tiny fade-in if the clip clicks.
9. Add a tiny fade-out if the clip ends abruptly.

If a phrase ends on a hard consonant:
- do not loop it as the main hook
- use it once
- crossfade it
- reverse it
- or make it a tight throw

### Why
You are building a vocabulary, not randomly dragging phrases around.

The intact chorus is the anthem.

The chops are the editing language.

## Step 6: Place The Break A Vocal Setup
### Action
Go to Arrangement View.

Zoom to `33.1.1-49.1.1`.

This is `Break A`.

Place these clips:
1. Put `VOC mystery statement` on `Vocal Chops` at `40.1.1`.
2. Optional: put `VOC mystery seed` on `Vocal Chops` at `44.1.1`.
3. Put `VOC question pre-drop` on `Vocal Chops` at `48.3.3`.
4. Trim `VOC question pre-drop` so it ends before `49.1.1`.

Do not put the full chorus in `Break A`.

Do not put `VOC chop A` or `VOC chop B` here.

### Why
`Break A` is the setup.

The listener should hear the voice and feel the question, but the chorus should not arrive until the drop.

### Checkpoint
Loop `33.1.1-49.1.1`.

You should hear:
- space
- first vocal identity
- a question or unresolved phrase before the drop

You should not hear:
- the full chorus
- a busy chop loop
- a second drop pretending to be a break

## Step 7: Place The First Intact Chorus In Drop A
### Action
Zoom to `49.1.1-65.1.1`.

Place `VOC full chorus clean` on `Vocal Full Chorus`:
- start: `49.1.1`
- end: before `65.1.1`

If the chorus is shorter than `16` bars:
- do not stretch it until it sounds fake
- leave a controlled gap after the chorus tail
- use drums and bass to carry the end of the section

If the chorus is longer than `16` bars:
- choose the strongest `16`-bar section
- or trim the tail so the next section can enter cleanly at `65.1.1`

Keep these first-pass support rules:
- no extra vocal chop over the first line
- no constant throw track
- no big delay throws until the dry chorus placement works
- bass should support the chorus, not fight it

### Why
This is the first big payoff.

The room needs to understand the song before you deconstruct it.

### Checkpoint
Loop `49.1.1-65.1.1`.

The chorus should feel:
- readable
- singable
- supported by the groove

If it feels buried:
- lower chords first
- lower bass mid second
- raise vocal only after checking those two

If it feels pasted on:
- reduce reverb
- high-pass mud
- make sure the first attack starts exactly where intended

## Step 8: Deconstruct The Chorus In Drop A Lift
### Action
Zoom to `65.1.1-81.1.1`.

This section is where the chops finally appear.

Place:
1. `VOC chop A` at `68.3.4`.
2. `VOC chop B` at `72.3.4`.
3. `VOC exposed core` at `76.3.4`.

Optional:
- add `VOC throw` at `80.4.4` if the transition into `Break B` needs a final answer

Do not run the full chorus again in this section on the first pass.

### Why
The listener just heard the intact chorus.

Now you can chop it because the source idea is already in their head.

This is the difference between:
- clever chop with context
- random vocal edit with no meaning

### Checkpoint
Loop `65.1.1-81.1.1`.

The section should feel more edited than `Drop A`.

It should not feel like a brand-new lyric section.

## Step 9: Place Break B As The Darker Return
### Action
Zoom to `81.1.1-97.1.1`.

Place:
1. `VOC question pre-drop` or `VOC mystery seed` at `88.1.1`.
2. Optional: place `VOC vulnerable phrase` at `92.1.1`.

If `VOC vulnerable phrase` has a hard consonant ending:
- add a short fade-out
- or crossfade the tail
- or use it once and do not loop it

Do not place the full chorus here.

### Why
`Break B` reminds the listener of the doubt before the final answer.

It should feel darker than `Break A`.

## Step 10: Build The Re-entry Pickup
### Action
Zoom to `97.1.1-113.1.1`.

Place:
1. optional `VOC reverse tail` ending at `109.3.4`
2. optional short filtered pickup at `110.3.4`
3. `VOC question pre-drop` at `112.3.3`
4. trim the question so it ends before `113.1.1`

The pickup should not overlap messily with the first word of the next chorus.

### Why
The re-entry pickup should pull the listener into `Drop B`.

It should not become another chorus before the chorus.

## Step 11: Return The Intact Chorus In Drop B
### Action
Zoom to `113.1.1-129.1.1`.

Place `VOC full chorus clean` on `Vocal Full Chorus`:
- start: `113.1.1`
- end: before `129.1.1`

This time the production can be bigger than `Drop A`:
- fuller bass tone
- wider chords
- stronger tops
- light chop texture in gaps

But keep the lead vocal readable.

Allowed support:
- short `VOC throw` in natural gaps
- low-level `VOC chop A` or `VOC chop B` tucked under the chorus tail
- reverse tail into the section start

Not allowed on the first pass:
- chops over every chorus line
- delay throws that cover the next line
- full chorus plus nonstop chop loop at the same level

### Why
This is the final intact-hook payoff.

It should feel like the first chorus returned with more context and more power.

## Step 12: Use Drop B Lift For Peak Chop Energy
### Action
Zoom to `129.1.1-145.1.1`.

Place the strongest chop / throw moments:
- `VOC chop A` at `132.3.4`
- `VOC chop B` at `136.3.4`
- `VOC exposed core` or `VOC throw` at `140.3.4`
- optional final `VOC throw` at `144.3.4`

If you want to stack:
- keep the main dry chop centered
- keep the throw lower
- send the throw to delay instead of turning it up

### Why
The peak is allowed to sound more edited.

But it should still be built from the chorus the listener already knows.

## Step 13: Keep The Outro Clean
### Action
Zoom to `145.1.1-161.1.1`.

First pass:
- no new lyric
- no new chop idea
- only tails or very short throws if needed

If a vocal tail spills into the outro:
- fade it down by `149.1.1`
- keep the DJ-safe groove readable

### Why
The outro should help the track mix out.

It should not introduce a new vocal story.

## First-Pass Arrangement Map
Use this as the placement authority for the current vocal direction:

| Section | Bars | Vocal role | First-pass placement |
|---|---:|---|---|
| `Intro A` | `1-16` | silence | no vocal |
| `Intro B` | `17-32` | silence | no vocal |
| `Break A` | `33-48` | setup | `VOC mystery statement` at `40.1.1`; `VOC question pre-drop` at `48.3.3` |
| `Drop A` | `49-64` | first intact chorus | `VOC full chorus clean` at `49.1.1` |
| `Drop A Lift` | `65-80` | first chop deconstruction | chops at `68.3.4`, `72.3.4`, `76.3.4` |
| `Break B` | `81-96` | darker return | question / vulnerable phrase at `88.1.1` and `92.1.1` |
| `Re-entry Build` | `97-112` | pickup | reverse / question at `109.3.4`, `110.3.4`, `112.3.3` |
| `Drop B` | `113-128` | intact chorus return | `VOC full chorus clean` at `113.1.1` |
| `Drop B Lift` | `129-144` | peak chop edit | chops / throws at `132.3.4`, `136.3.4`, `140.3.4`, `144.3.4` |
| `Outro` | `145-160` | exit | tails only |

## What It Should Sound Like
`Break A` should sound like the vocal has entered the room, but the song has not arrived yet.

`Drop A` should sound like the recognizable chorus finally lands.

`Drop A Lift` should sound like a club edit of the chorus, not a new chorus.

`Break B` should sound more exposed and doubtful.

`Drop B` should sound like the chorus comes back with more production weight.

`Drop B Lift` should sound like the most edited version of the vocal, but still connected to the hook.

## Troubleshooting
### The full chorus sounds pasted on
Check in this order:
1. Is the first attack exactly at `49.1.1` or `113.1.1`?
2. Is the clip warped cleanly?
3. Is the vocal too wet?
4. Are the chords too loud in `300 Hz-2 kHz`?
5. Is the bass mid masking the lower part of the vocal?

### The chops sound random
Fix the story order:
1. `Break A` sets up mystery.
2. `Drop A` gives the intact chorus.
3. `Drop A Lift` chops the chorus after the listener knows it.
4. `Break B` returns to the question.
5. `Drop B` brings the intact chorus back.

If the listener has not heard the intact chorus yet, aggressive chops will feel random.

### The track sounds like a cover, not a flip
Make the sections between intact choruses more edited.

Do not destroy the chorus itself first.

Use:
- dry chops
- reverse tails
- phrase-end throws
- filtered pickups
- tighter drum fills

### The vocal fights the bass
Do this before changing the whole arrangement:
1. High-pass the vocal a little higher.
2. Lower `Bass Mid` by `1-2 dB`.
3. Cut a little `250-400 Hz` from the vocal or chords.
4. Check the vocal with `Sub` muted.
5. Check the vocal with `Bass Mid` muted.

### The vocal fights the chords
Check whether the vocal note implies a different chord.

If it does:
- move that vocal phrase to a different chord bar
- or use it as a throw instead of a sustained lead
- or filter it so the pitch reads less strongly

## Screenshot Requirements
Capture these:
- `part05-01-vocal-tracks-created`
- `part05-02-audition-clip-warped`
- `part05-03-full-chorus-chain`
- `part05-04-chop-chain`
- `part05-05-full-chorus-clip-cut`
- `part05-06-break-a-vocal-placement`
- `part05-07-drop-a-full-chorus-placement`
- `part05-08-drop-a-lift-chop-placement`
- `part05-09-break-b-vocal-placement`
- `part05-10-reentry-vocal-pickup`
- `part05-11-drop-b-full-chorus-return`
- `part05-12-drop-b-lift-chops`

## Completion Check
Before moving to Part 6, confirm:
- `Intro A` has no vocal
- `Intro B` has no vocal
- `Break A` introduces the vocal before `Drop A`
- `Drop A` uses the intact chorus, not chopped fragments as the main event
- `Drop A Lift` uses chops after the chorus has been heard
- `Break B` reopens the emotional question
- `Drop B` returns to the intact chorus
- `Drop B Lift` carries the strongest chop edits
- no vocal clip spills across a section boundary by accident
