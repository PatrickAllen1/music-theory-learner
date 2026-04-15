# Music Theory Learner — Phase 2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deepen the learning content, add a daily practice system with progress tracking, finish all 25 guided builds, and teach Serum V2 from zero to functional. Phase 2 turns the scaffold into a real learning tool.

**What Phase 1 delivered:** App shell, 5 track breakdowns, 3 beginner reps + 1 Kettama spinoff, Theory reference (4 scales, 6 chords, 6 rhythms), Ableton cheatsheet (3 entries), Builder UI. Deployed at music-theory-learner.pages.dev.

**Serum V2 target:** By end of Phase 2, the user can open Serum V2, navigate the UI confidently, build a sub bass from scratch, build a pad from scratch, build a Reese bass, and understand what every section of the synth does in the context of UK garage sounds. All Serum content is anchored to sounds in the 5 source tracks — no abstract synthesis theory.

---

## Core Learning Philosophy: Content → Repetition

**Reading is not learning. Doing is learning.**

Every piece of content in this app exists to send the user to a rep — a guided build where they experience the concept hands-on, in their DAW, making real sounds. The goal is not comprehension. The goal is repetition: doing the same musical move in 3 different keys, with 3 different sounds, until the pattern lives in the hands.

**The system:**
- **Cheatsheet entries** → each entry has a companion rep where you use that tool in context. You do not understand sidechain compression by reading about 3:1 ratio. You understand it by opening the Kettama spinoff, setting up the sidechain on your pads, and hearing the pump.
- **Theory cards (scales/chords/rhythms)** → each card links to the rep(s) where you practise that concept. Bb minor is not a page to read — it's rep-11 that you play.
- **Deep dives** → each article ends with a practice exercise that maps directly to a Builder rep. The article gives you the "why". The rep is where you do it.
- **Reps** → each rep tags which concepts it teaches (via `teaches[]`), enabling reverse navigation: from the Theory page, you can see which reps use that scale/chord and click straight into one.

**Schema requirement:** Any new content type must have a `practice_rep_id` or `linked_rep_ids[]` field. If no existing rep covers a concept, that gap goes in the rep backlog — never left unlinked.

**The experience:** A user reads the "VI→III→i Loop" deep dive, sees the Bb minor chord voicings, then clicks "Practice this in the Builder" — and lands in rep-11 where they actually programme those three chords. When they're done, they try the same exercise in F minor (rep-12). This is how the content and the reps form one loop, not two separate sections.

---

## Phase 2A: Theory Deep Dives

### Task 11: Deep Dive content type + Theory page upgrade

**Goal:** Replace surface-level expandable cards with a proper "Deep Dives" tab on the Theory page. Each deep dive is a long-form article that teaches one concept in depth — with track references, MIDI examples, and a practice exercise at the end.

**Files:**
- Create: `src/content/theory/deep-dives/vi-iii-i-loop.json`
- Create: `src/content/theory/deep-dives/phrygian-tension.json`
- Create: `src/content/theory/deep-dives/bass-implied-harmony.json`
- Create: `src/content/theory/deep-dives/chord-voicing.json`
- Create: `src/content/theory/deep-dives/index.js`
- Modify: `src/content/theory/index.js`
- Modify: `src/pages/Theory.jsx`

**Deep dive schema:**
```json
{
  "id": "vi-iii-i-loop",
  "title": "The VI→III→i Loop",
  "subtitle": "How Kettama's three chords create an emotional arc",
  "difficulty": "beginner",
  "read_time_mins": 8,
  "track_references": ["kettama-it-gets-better"],
  "sections": [
    {
      "id": "intro",
      "heading": null,
      "body": "Long-form text here..."
    },
    {
      "id": "the-chords",
      "heading": "The Three Chords",
      "body": "..."
    }
  ],
  "midi_examples": [
    {
      "label": "Gbmaj7 voicing",
      "notes": ["Gb3", "Bb3", "Db4", "F4"],
      "context": "The launch chord — major 7th on the flat-6"
    }
  ],
  "listening_cues": [
    {
      "track_id": "kettama-it-gets-better",
      "timestamp": "~0:32",
      "what_to_hear": "The full VI→III→i loop enters for the first time — Gbmaj7 for 2 bars, then Dbmaj and Bbm each for 1 bar. Notice how the Gbmaj7 feels like a moment of brightness in an otherwise dark key.",
      "technique": "VI→III→i progression entering"
    },
    {
      "track_id": "kettama-it-gets-better",
      "timestamp": "~1:10",
      "what_to_hear": "Listen specifically to the common tone between Gbmaj7 and Dbmaj — the note F (or the Db) that stays in place as the chords move. That stationary note is what makes the transition feel smooth rather than abrupt.",
      "technique": "common tone across chord changes"
    }
  ],
  "practice_exercise": {
    "instruction": "Program the VI→III→i loop in F minor (not Bb minor). Work out the three chord names from the F minor scale, then voice them in Serum or a piano roll. The notes are all in the F natural minor scale.",
    "answer_hint": "F minor scale: F G Ab Bb C Db Eb. VI = Dbmaj7 (Db, F, Ab, C). III = Abmaj (Ab, C, Eb). i = Fm (F, Ab, C).",
    "linked_rep_id": "rep-11-VI-III-i-loop-bbmin"
  },
  "key_takeaway": "One sentence that sticks."
}
```

**`listening_cues[]` schema — required on every deep dive:**

Each deep dive must contain a `listening_cues[]` array. Each cue has:
- `track_id` — references one of the 5 source tracks
- `timestamp` — approximate position in the track (prefix with `~` — these are reference points, not exact; mark as approximate to set expectations)
- `what_to_hear` — specific instruction: not "listen to the chord" but "notice the F in the high voice staying stationary as the bass moves under it"
- `technique` — one-line label used to render a small tag on the cue in the UI

**Timestamps for all 6 deep dives — fill these in during implementation by loading the track and finding the moment:**

| Deep Dive | Track | Key moments to timestamp |
|---|---|---|
| vi-iii-i-loop | kettama-it-gets-better | Loop enters, common tone between Gbmaj7→Dbmaj, full drop where the loop carries full energy |
| phrygian-tension | mph-raw | The phrygian b2 note entering, the moment it resolves back to root, longest sustained tension note |
| bass-implied-harmony | bl3ss-deeper | i→bIII moment, bVI arriving (the "lift"), how little else is happening harmonically |
| arrangement-theory | kettama-it-gets-better | Exactly where intro ends, where build starts, 1-beat silence, drop 1 start, breakdown start |
| sound-design-emotion | kettama-it-gets-better | Attack of pad (slow — notice the swell vs immediate hit), compare pad attack vs bass attack |
| transposing-concepts | mph-raw + kettama | The same interval relationship (root → b2) heard in two different keys |

**Note on timestamps:** These are added to the JSON data as approximates. When implementing, the developer opens each track in a media player and finds the actual moments — the schema allows the content to be corrected without changing the UI.
```

**Note on `linked_rep_id`:** Every deep dive's `practice_exercise` must have a `linked_rep_id` pointing to the Builder rep where the user experiences the concept. If no rep exists yet, create one first. The deep dive is the "why" — the rep is the "do".

| Deep Dive | linked_rep_id |
|---|---|
| vi-iii-i-loop | rep-11-VI-III-i-loop-bbmin (also surfaces rep-12 for F minor) |
| phrygian-tension | rep-03-phrygian-bass-emin |
| bass-implied-harmony | rep-13-bass-implied-dmin |
| arrangement-theory | rep-06-mini-track-emin (first track with structure) |
| sound-design-emotion | rep-24-serum-chord-pad (attack/timbre exercise) |
| transposing-concepts | rep-04 + rep-05 (multi-key phrygian) |
```

**Step 1: Write 3 deep dives**

Deep dive 1 — `vi-iii-i-loop.json`: Full analysis of Kettama's VI→III→i. Cover: what each chord is, why all three are diatonic to natural minor, what common tones do, why the progression feels inevitable. Reference the chord voicings from the spinoff build. End with: transpose the loop to F minor as an exercise.

Deep dive 2 — `phrygian-tension.json`: Full analysis of the phrygian b2 (MPH Raw). Cover: what phrygian mode is vs natural minor (only the 2nd is different), why one semitone of distance creates maximum tension, how note length and velocity shape the tension arc, why MPH has no chord progression and doesn't need one. Exercise: write a 4-bar phrygian bass line in A minor (root = A, tension = Bb).

Deep dive 3 — `bass-implied-harmony.json`: Full analysis of BL3SS's approach. Cover: what implied harmony is, how the ear fills in chord tones from a single bass note, why this technique creates space, the specific i→bIII→bVI→iv motion in D minor. Exercise: write a new 4-bar bass-implied progression in G minor (work out the chord names first, then write only the roots).

Deep dive 7 — `chord-voicing.json` *(new — fills the gap between knowing a chord name and making it sound like a garage chord)*:

**Title:** "Chord Voicing — From Name to Sound"
**Subtitle:** "Knowing Gbmaj7 and making it sound like Kettama are completely different skills. This deep dive bridges them."
**Difficulty:** beginner
**Read time:** 10 mins
**Track references:** kettama-it-gets-better

**Sections:**

1. **The problem nobody warns you about**
You've learned that VI→III→i in Bb minor = Gbmaj7 → Dbmaj → Bbm. You open the piano roll. You put the notes in. It sounds nothing like Kettama. What went wrong? The notes are correct. The voicing is not. Voicing is how you distribute chord notes across octaves and between instruments — and it changes the emotional character of a chord completely. A Gbmaj7 voiced in the wrong octave sounds muddy, cluttered, or empty. Voiced correctly it sounds like warmth falling from a height.

2. **Register — where in the keyboard the chord lives**
Register is the most important voicing decision. Playing chord tones in the low register (below C3) creates mud — the overtones of multiple notes at low frequencies clash and blur together. Playing all chord tones in the high register (above C5) sounds thin and bright — no body. The sweet spot for garage pads: voice the main chord body between D3–D5. Keep notes below C3 only for the bass line. Keep notes above C5 only for a single top note or melody voice. The Gbmaj7 in Kettama sits in this register: Gb3 Bb3 Db4 F4 — you can hear the chord clearly without muddiness.

3. **Closed vs open (spread) voicings**
A closed voicing stacks chord tones as close together as possible — Gbmaj7 closed = Gb3 Ab3 Bb3 Db4. A spread (open) voicing distributes them across a wider range — Gb3 Bb3 Db4 F4. Closed voicings in the mid register sound dense and jazzy. Spread voicings sound larger, more cinematic, and translate better in a mix with a separate bass line. For garage pads: spread voicings are almost always correct. The chord tones are distributed across at least 1.5–2 octaves. The bass line takes the root — the pad does not need to double it.

4. **Inversions — which note is on the bottom**
Root position = the root note is the lowest note in the chord voicing (not counting the separate bass line). First inversion = the 3rd is lowest. Second inversion = the 5th is lowest. This is separate from the bass line — the pad can be in any inversion while the bass plays the root. In UK garage pads: root position and first inversion are both common. Root position sounds grounded and stable. First inversion sounds slightly lighter, like the chord is lifting off the ground. Second inversion has a more ambiguous, unresolved quality — useful at the end of a phrase to create motion toward the next chord. Experiment: play Gbmaj7 with Gb at the bottom (root), then Bb at the bottom (1st inversion). Same notes, different emotional weight.

5. **Major 7ths specifically — why garage uses them**
A major 7th chord (Gbmaj7 = Gb Bb Db F) has the major 7th as its top note (F is the major 7th of Gb). This interval — the major 7th between root and top note — creates the distinctive lush, bittersweet quality of garage pads. Without the 7th, it's just a major triad (Gb Bb Db) — fine but less distinctive. The 7th is what makes the chord feel like it's reaching upward. Voice the 7th as the highest note in the pad voicing whenever possible. Gbmaj7 in the Kettama spinoff: Gb3 Bb3 Db4 **F4** — F is the top, the 7th rings out above everything.

6. **Chord rhythm — when notes are held vs released**
Voicing is not just which notes — it's when they start and end. Kettama's pads hold each chord for its full duration (2 bars for Gbmaj7, 1 bar each for Dbmaj and Bbm). The long held chord lets the reverb bloom around the voicing. If you program the same voicing with short, staccato notes it sounds completely different — percussive rather than lush. For garage pads: hold notes for at least 1 bar, sometimes 2. The release is handled by Serum's envelope (long release = notes decay naturally rather than cutting off). The sidechain gives rhythmic pulse without shortening the note. This is how the pad can feel "pumping" while the notes are held.

7. **Doubling notes — and when not to**
Doubling means playing the same note in two octaves simultaneously (e.g., both Gb3 and Gb4 in the same voicing). Doubling the root in octaves adds weight and grounding — but also adds more root to the mix that may compete with the bass. Doubling the 7th (top note) in octaves adds brightness and shimmer. In a garage pad context: doubling is usually unnecessary because the reverb and unison in Serum already create width and fullness. If the pad feels thin despite being voiced correctly, try doubling the top note one octave up (F5 added to the Gbmaj7 voicing) — but use this sparingly.

8. **Voicings for each chord in the source tracks:**

```
Gbmaj7 (Kettama VI chord — Gb major key):
  → Spread voicing: Gb3  Bb3  Db4  F4
  → 7th (F) on top. Db4 in the middle creates fullness.
  → Do not put Gb below C3 — leave that to the bass.

Dbmaj (Kettama III chord):
  → Spread voicing: Db3  F3  Ab3  (or Ab3  Db4  F4)
  → No 7th needed — straight major. Sounds more resolved than Gbmaj7.
  → Keep in D3–F4 register.

Bbm (Kettama i chord — tonic):
  → Spread voicing: Bb3  Db4  F4  (minor triad spread over 1.5 octaves)
  → The 5th (F) on top keeps it light despite being minor.
  → Heavier version: Bb2  F3  Bb3  Db4 — but this is denser, only if you want weight on the tonic.

Em (4-on-floor rep i chord):
  → Bb voicing mapped to E minor:  E3  G3  B3  (or E3  B3  E4)
  → For phrygian bass context: pad doesn't need to play — bass carries everything.

Minor 7th (general):
  → Formula: root  b3  5  b7
  → Spread: root3  b3-3  5-3  b7-4
  → Bbm7 = Bb3  Db4  F4  Ab4
```

9. **How to hear voicings in a reference track**
When listening to a garage track, train yourself to hear the top note of the chord pad — that's usually the most distinctive pitch. The top note of a major 7th chord is the 7th — you can hum it. Find it in the reference, then work downward: what note is a 3rd below? A 5th below? This reverse-engineers the voicing. You don't need perfect pitch — relative intervals are enough. Practice: listen to Kettama at the drop. Hum the highest note of the pad. Now hum the note you hear underneath it. That's a minor 3rd (Db4 under F4). Now hum the note under that. That's a major 3rd (Bb3 under Db4). You've found the voicing from the top down.

10. **The decision tree**
Does the chord sound muddy? → Move the voicing up an octave. Nothing should be below C3 except the bass line.
Does the chord sound thin and empty? → Check the spread — you may have all notes clustered in one octave. Spread them across 1.5–2 octaves.
Does the chord not sound like the reference? → Check the register. Check whether you have the 7th as the top note. Check that you're not doubling the root in the pad (the bass already has it).
Does the chord sound harsh or cold? → You may be using a closed voicing in the mid-low register. Open it up — use a spread voicing between D3 and E4.
Does the chord sound right in isolation but wrong in the mix? → The pad may be competing with the bass in the 100–200Hz range. High-pass the pad at 120–130Hz and let the bass own below that.

**Practice exercise:**
"Open a MIDI track in Ableton with Serum V2 (Init Preset, Basic Shapes wavetable, slow attack, long release). Program these three voicings one at a time:
1. Gbmaj7 closed: Gb3 Ab3 Bb3 Db4 — hold for 4 bars.
2. Gbmaj7 spread: Gb3 Bb3 Db4 F4 — hold for 4 bars.
3. Gbmaj7 spread, 1st inversion: Bb3 Db4 F4 Gb4 — hold for 4 bars.
Add the Kettama spinoff's reverb and sidechain. Listen to all three versions back to back. Write down in one sentence: which version sounds closest to the reference and why."

**Answer hint:** The spread voicing (version 2) with F as the top note is correct. The closed voicing muds up in the lower mids. The 1st inversion version sounds floating and unresolved — the Gb at the top doesn't have the warmth of the 7th, it has the angular quality of the root in a high register.

**`linked_rep_id`:** `rep-11-VI-III-i-loop-bbmin` — this is where you actually programme the three Kettama chords using the voicings from this deep dive.

**`listening_cues`:**
- kettama-it-gets-better ~0:32 — "Find the top note of the pad chord at the drop. That F4 ringing out above everything is the major 7th. Hum it. Now work down: what's a 3rd below? Db4. What's a 3rd below that? Bb3. That's the Gbmaj7 voicing from top to bottom."
- kettama-it-gets-better ~0:48 — "When the chord changes from Gbmaj7 to Dbmaj, notice: the F at the top disappears (or drops a step). That single note change is how you hear a chord change without the bass moving. The voicing shift tells you more than the root movement."

**Key takeaway:** "A chord name tells you the notes. A voicing tells you where to put them. Register (above C3), spread (1.5–2 octaves), and the 7th on top: those three decisions turn a correct chord into a Kettama chord."

---

**Step 2: Update theory index**

`src/content/theory/index.js`:
```js
export { scales, chords, rhythms } from './scales.json' // etc
export { deepDives } from './deep-dives/index.js'
```

**Step 3: Add Deep Dives tab to Theory page**

Add a 4th tab: Scales | Chords | Rhythms | **Deep Dives**

Deep dive cards in the tab list show: title, subtitle, difficulty badge, read time, track references as small pills.

Clicking a card opens a full-page article view (replace the tab content area, not a new route). Show a "← Back to Theory" link at the top.

Article renders: title, subtitle block, sections with headings and body text, MIDI example pills (note names displayed as tags), **listening cue blocks** (track reference + timestamp + "what to hear" description, displayed inline where they appear in the section — styled as a callout box: zinc-900 background, left-border accent in yellow-600, "→ Listen: [track name] ~[timestamp]" header), practice exercise box (highlighted block with instruction + expandable answer hint), "Practice this in the Builder →" CTA button that navigates to the `linked_rep_id`, key takeaway block.

**Step 4: Verify + commit**
```bash
npm run dev
# Navigate to Theory → Deep Dives → click VI→III→i Loop
# Check: sections render, MIDI note pills show, practice box expands answer
git add src/content/theory/deep-dives/ src/content/theory/index.js src/pages/Theory.jsx
git commit -m "feat: theory deep dives — VI→III→i, phrygian tension, bass-implied harmony"
```

---

### Task 12: Theory deep dives — Part 2 (arrangement + sound design)

**Files:**
- Create: `src/content/theory/deep-dives/arrangement-theory.json`
- Create: `src/content/theory/deep-dives/sound-design-emotion.json`
- Create: `src/content/theory/deep-dives/transposing-concepts.json`

**Deep dive 4 — `arrangement-theory.json`:** Why garage tracks are structured intro/build/drop/breakdown/rebuild/drop. What each section does psychologically. Why the 1-beat silence before the drop works. How long each section should be (bar counts and why). Exercise: map the structure of Kettama — It Gets Better by listening — write down bar counts for each section.

**Deep dive 5 — `sound-design-emotion.json`:** How timbre (the character of a sound) affects emotional register. Sine vs saw vs noise. Why Kettama's pads feel lush (slow attack, reverb, detune). Why MPH's bass feels tense (clean sine, phrygian pitch movement). Why the 2-step kick feels lighter than 4-on-floor even at the same tempo. Exercise: take a Serum patch and adjust the attack from 0ms to 500ms — describe how the emotion changes at each setting.

**Deep dive 6 — `transposing-concepts.json`:** How to move any technique to a new key. The semitone map: what +2, +3, +7 etc mean. How to find the i, bIII, bVI, iv in any minor key without memorising. The "count from the root" method. Full worked examples: transpose VI→III→i from Bb minor to E minor to G minor. Exercise: write the phrygian b2 bass line in 3 new keys of your choosing.

**Step 4: Verify + commit**
```bash
git commit -m "feat: theory deep dives — arrangement, sound design, transposing"
```

---

## Phase 2B: Complete Guided Builds Content

### Task 13: Beginner reps 4–7

**Files:** `src/content/guided-builds/reps/rep-04` through `rep-07`, update `index.js`

**Rep 04 — `rep-04-phrygian-bass-dmin.json`:** Phrygian b2 bass tension, D minor (root D, tension Eb). Same 8-step structure as rep-03 but different key — forces the concept to generalise. Include a direct comparison step: play rep-03's E minor phrase back to back with the D minor version.

**Rep 05 — `rep-05-phrygian-bass-amin.json`:** Phrygian b2 bass tension, A minor (root A, tension Bb). Third key for the same concept. Final step: combine all three keys (E, D, A) into an 8-bar sequence that modulates between them.

**Rep 06 — `rep-06-mini-track-emin.json`:** Mini-track combining 4-on-floor kick + phrygian bass in E minor. 8 steps: set up drums, set up bass, layer them together, EQ each, rough mix balance, add a simple open hat accent, loop 8 bars and adjust, export a 30-second loop. First time the user combines multiple elements.

**Rep 07 — `rep-07-mini-track-gmin.json`:** Same mini-track concept but G minor, 2-step kick. Source track reference: Sammy Virji. 8 steps. Uses the 2-step kick from rep-02. Final step: compare the mini-track feel (2-step + G minor bass) against rep-06 (4-on-floor + E minor bass).

**Step: Update index.js** — import all 4 new reps, add to builds array.

**Step: Verify + commit**
```bash
git commit -m "feat: beginner reps 4-7 — phrygian bass in D/A minor, mini-tracks"
```

---

### Task 14: Intermediate reps 8–14

**Files:** `src/content/guided-builds/reps/rep-08` through `rep-14`, update `index.js`

All intermediate reps are ~10 steps each (more complex than beginner's 8).

**Rep 08 — `rep-08-bVI-lift-emin.json`:** The bVI lift chord (IC technique), E minor. Teach: what bVI is (C major in E minor), how it creates brightness in a dark key, how to voice Cmaj over an Em bass. Steps: set up drums, program Em bass, program Em chord pad, introduce C major chord in bar 3 (the lift), sidechain pads, reverb, contrast Em-only vs Em+Cmaj, export.

**Rep 09 — `rep-09-bVI-lift-amin.json`:** Same bVI lift, A minor (bVI = F major). 10 steps. Include: how F major in A minor creates a different emotional colour than C major in E minor — same interval relationship, different timbre.

**Rep 10 — `rep-10-bVI-lift-dmin.json`:** bVI lift, D minor (bVI = Bb major). Include: note that Bb major is also part of the VI→III→i loop (from Kettama's Bb minor track). Cross-reference between techniques.

**Rep 11 — `rep-11-VI-III-i-loop-bbmin.json`:** Full VI→III→i chord loop, Bb minor (Kettama's key). 10 steps using Serum. Teaches: voicing all 3 chords correctly, the chord rhythm (Gbmaj7 × 2 bars, Dbmaj + Bbm × 1 bar each), bass line following roots, sidechain, arrangement hint (which chord to start the drop on).

**Rep 12 — `rep-12-VI-III-i-loop-fmin.json`:** VI→III→i in F minor (Dbmaj7→Abmaj→Fm). 10 steps. Include: deriving the chord names from the F minor scale (not memorising), so the user learns the method not just the Bb minor version.

**Rep 13 — `rep-13-bass-implied-dmin.json`:** Bass-implied harmony, D minor (BL3SS technique). 10 steps: sub bass only carrying i→bIII→bVI→iv (Dm→F→Bb→Gm roots), no chord pad. Include: how to make bass-only sound harmonically full (note length, velocity, sub bass timbre). Final step: add a very minimal pad at -18dB and hear how little you actually need.

**Rep 14 — `rep-14-bass-implied-gmin.json`:** Bass-implied harmony, G minor. 10 steps. Different chord movement — the user chooses the progression (i→bVII→bVI→v is a good suggestion). Include: a step that explains why choosing a different progression in the same technique produces a completely different emotional result.

**Step: Update index.js**

**Step: Verify + commit**
```bash
git commit -m "feat: intermediate reps 8-14 — bVI lift x3, VI-III-i x2, bass-implied x2"
```

---

### Task 15: Spinoffs 2–4 (entry and mid levels)

**Files:** `src/content/guided-builds/spinoffs/spinoff-01` through `spinoff-04`, update `index.js`

**Spinoff 01 — `spinoff-01-mph-dmin-entry.json`:** MPH Raw style, D minor, 128 BPM (entry level). Changes from source: key D minor instead of E minor, BPM 128 instead of 132. Same phrygian approach. 10 steps. Production brief: "We dropped the key a step to D minor and slowed to 128 BPM. Same phrygian tension, but the lower pitch and slower tempo makes it feel heavier and more hypnotic."

**Spinoff 02 — `spinoff-02-ic-amin-entry.json`:** IC Slow Burner style, A minor, 2-step kick (entry level). Changes: key A minor, kick swapped from 4-on-floor to 2-step. 10 steps. Production brief: "The 2-step kick completely changes the emotional register — same chord loop (Em→Bm→C transposed to Am→Em→F) but lighter, more human-feeling rhythm."

**Spinoff 03 — `spinoff-03-ic-dmin-mid.json`:** IC style, D minor, mid level. Changes: new key, introduce a Reese-style bass in the breakdown section. 12 steps. Production brief: "We've added a Reese bass — a detuned saw oscillator — that only appears in the breakdown. The harmonic complexity of the Reese against the quiet chord pads creates a brief moment of darkness before the drop."

**Spinoff 04 — `spinoff-04-kettama-fmin-mid.json`:** Kettama style, F minor, BL3SS bass technique (mid level). Changes: new key, bass-implied harmony instead of full chord pads (bass carries the VI→III→i roots, pads at lower volume). 12 steps. Production brief: "We stripped the chords back and let the bass imply the harmony. The same VI→III→i motion is there but it feels more stripped, more late-night. The pads exist but they're texture, not the main event."

**Step: Update index.js**

**Step: Verify + commit**
```bash
git commit -m "feat: spinoffs 1-4 — MPH/IC entry levels, IC Reese mid, Kettama F minor mid"
```

---

### Task 16: Full spinoffs 5–7 + Originals 1–4

**Files:** `spinoff-05` through `spinoff-07`, `original-01` through `original-04`, update `index.js`

**Spinoff 05 — `spinoff-05-ic-full.json`:** IC DNA, full transform. New key (B minor), new drum pattern (mix 4-on-floor bars with 2-step bars), new bass texture (layered sub + mid bass), new structure (longer intro, no breakdown — goes straight drop→outro). 15 steps. Full production brief explaining every decision.

**Spinoff 06 — `spinoff-06-sammy-full.json`:** Sammy Virji DNA, full transform. New key (C minor), borrowed major chords (i chord as major = Cm turned to C major for the Picardy effect), ascending riff on a different instrument (try Rhodes instead of strings). 15 steps.

**Spinoff 07 — `spinoff-07-bl3ss-full.json`:** BL3SS DNA, full transform. New key (A minor), vocal chop element (find a vocal loop on Splice and chop it to a Drum Rack), different time feel (add a subtle 3/4 bar every 8 bars to disrupt the pattern). 15 steps.

**Original 01 — `original-01-slow-fade.json`:** "Slow Fade". D minor, 132 BPM, beginner. Concept: dark, minimal, phrygian bass only, no chords. Late-night feeling. 10 steps. Techniques borrowed: MPH phrygian bass, BL3SS bass-implied approach.

**Original 02 — `original-02-glass-road.json`:** "Glass Road". F minor, 134 BPM, intermediate. Concept: i→bVI→bIII progression (different from Kettama's VI→III→i), long reverb tails, synth strings. 12 steps.

**Original 03 — `original-03-midnight-circuit.json`:** "Midnight Circuit". G minor, 138 BPM, intermediate. Concept: evolving structure — the chord progression changes in the second drop (bVI→iv in drop 1, bVI→bVII in drop 2). 14 steps.

**Original 04 — `original-04-static-amber.json`:** "Static Amber". A minor, 136 BPM, advanced. Concept: full crossbred track — 2-step kick, bass-implied harmony, borrowed major chord on the drop, Reese bass in breakdown, phrygian riff in the outro. All 5 source track techniques in one. 18 steps.

**Step: Update index.js**

**Step: Verify + commit**
```bash
git commit -m "feat: full spinoffs 5-7 and originals 1-4 — all 25 builds complete"
```

---

## Phase 2C: Features

### Task 17: Progress tracking (localStorage)

**Goal:** Users can mark steps as complete and see their progress across builds. Persists between sessions. No backend — all localStorage.

**Files:**
- Create: `src/hooks/useProgress.js`
- Modify: `src/components/BuildStep.jsx`
- Modify: `src/components/BuildSelector.jsx`
- Modify: `src/pages/Builder.jsx`

**Step 1: Write useProgress hook**

`src/hooks/useProgress.js`:
```js
import { useState, useEffect } from 'react'

const KEY = 'mtl-progress'

function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || {} }
  catch { return {} }
}

export function useProgress() {
  const [progress, setProgress] = useState(load)

  const markStep = (buildId, stepId) => {
    setProgress(prev => {
      const next = {
        ...prev,
        [buildId]: { ...prev[buildId], [stepId]: true }
      }
      localStorage.setItem(KEY, JSON.stringify(next))
      return next
    })
  }

  const unmarkStep = (buildId, stepId) => {
    setProgress(prev => {
      const next = { ...prev, [buildId]: { ...prev[buildId] } }
      delete next[buildId][stepId]
      localStorage.setItem(KEY, JSON.stringify(next))
      return next
    })
  }

  const stepsComplete = (buildId) =>
    Object.keys(progress[buildId] || {}).length

  const isBuildComplete = (build) =>
    stepsComplete(build.id) >= build.steps.length

  return { progress, markStep, unmarkStep, stepsComplete, isBuildComplete }
}
```

**Step 2: Add "Mark complete" checkbox to BuildStep**

Add a checkbox below the nav buttons in BuildStep. When checked: calls `markStep(buildId, step.id)`. Show a checkmark + "Step complete" text when marked.

**Step 3: Show progress on BuildSelector cards**

On each build card: show a progress bar (completed steps / total steps) and a count `3/8 steps`. If all steps complete, show a green "Complete" badge instead.

**Step 4: Pass progress hook down through Builder**

Builder instantiates `useProgress()` and passes `markStep`, `stepsComplete`, `isBuildComplete` down to BuildSelector and BuildStep as props.

**Step 5: Verify + commit**
```bash
git commit -m "feat: progress tracking — mark steps complete, persists in localStorage"
```

---

### Task 18: Daily practice system

**Goal:** A "Practice" widget on the Builder page that suggests today's rep and tracks streaks. Uses localStorage. Lightweight — no new route, just a section above the build selector.

**Files:**
- Create: `src/hooks/usePracticeStreak.js`
- Create: `src/components/DailyPractice.jsx`
- Modify: `src/pages/Builder.jsx`

**Step 1: Write usePracticeStreak hook**

Tracks: last practice date, current streak (consecutive days). When a build is opened on a new day, updates the streak. Stores `{ lastDate: 'YYYY-MM-DD', streak: N, completedToday: [] }`.

**Step 2: Write DailyPractice component**

Shows above the BuildSelector when no build is selected.

Layout:
- Top row: "Today's practice" heading + streak counter (🔥 5 days or just "5 day streak")
- Suggested rep card — picks the next incomplete beginner or intermediate rep. If all complete, suggest a spinoff.
- One-line description of what the rep covers
- "Start →" button that calls `onSelect(suggestedBuild)`

Logic for suggestion: find the first rep where `stepsComplete(id) < build.steps.length` — the next incomplete build. Cycle through reps in order.

**Step 3: Wire into Builder.jsx**

Show `<DailyPractice>` above `<BuildSelector>` only when `!build` (selector view). Pass `onSelect` and progress data.

**Step 4: Verify + commit**
```bash
git commit -m "feat: daily practice system — today's rep suggestion, streak tracking"
```

---

### Task 19: Cheatsheet expansion — grounded in the actual remakes

**Goal:** Expand from 3 to 30+ entries. Every entry is tied to a real device or technique used in at least one of the 5 source remakes. Sourced from a Python scan of all 5 .als files — only devices that actually appear get entries.

**Device usage from .als scan (most → least common):**
- 5/5 tracks: Simpler, GlueCompressor, Reverb, Chorus (internal), PreDelay, DiffuseDelay
- 4/5 tracks: Limiter, Saturator, SimplerLfo, SimplerFilter
- 3/5 tracks: AutoFilter, Compressor, FilterType
- 2/5 tracks: Delay/Echo, Overdrive, Flanger
- 1/5 tracks (Kettama only): Operator, Gate, GrainDelay, FilterDelay, Amp, SimplerShaper

**Files:** 27 new JSON files in `src/content/cheatsheet/`, updated `index.js`

**Schema update for all cheatsheet entries:** Add a `practice_rep_id` field and a `practice_hint` string. These enable the Cheatsheet page to show a "Try it in a build →" button that opens the Builder at that rep. If no existing rep covers the tool, the entry gets a `practice_hint` (plain text instructions to use the tool in any session) until a dedicated rep is added.

| Entry | practice_rep_id | notes |
|---|---|---|
| sidechain / glue-compressor | spinoff-kettama-bbmin-full (steps 14-15) | sidechain is already in the Kettama spinoff |
| reverb | spinoff-kettama-bbmin-full (step 16) | reverb return send is in Kettama spinoff |
| simpler | rep-01 through rep-07 (any drum step) | all drum reps use Simpler |
| saturator | rep-08-bVI-lift (EQ+Saturator step) | intermediate reps use Saturator on pads |
| compressor | rep-13-bass-implied-dmin | sidechain comp is step 7 |
| auto-filter | rep-11-VI-III-i-loop (build section) | filter sweep in build |
| operator / FM | Task 30 rep (Serum track, defer to phase 3) | no existing rep — add practice_hint for now |
| all workflow entries (groove pool, automation, etc.) | practice_hint only | add dedicated "workflow reps" in Phase 3 |

---

**TIER 1 — Used in every remake (5/5 tracks). Must have entries:**

1. `simpler.json` — **Simpler** is the most-used device across all 5 tracks. Every drum sound lives in a Simpler inside the Drum Rack. Used for: sample playback, melodic samples (piano, strings), chopped loops. Steps: load a sample, set sample start/end, adjust loop, set amp envelope, understand Classic vs 1-Shot vs Slicing mode. When: any time you want to load a single audio sample and play it from MIDI. V Classic = full sampler with looping. 1-Shot = plays once on note-on (drums). Slicing = chops a loop to individual pads. Tags: simpler, sample, playback, drum, melodic.

2. `glue-compressor.json` — **Glue Compressor** is on drum buses in every remake. Different from the standard Compressor — modelled on an SSL bus compressor. Used for: bus glue on drum groups, making a drum kit feel like one instrument rather than separate samples. Steps: add to DRUMS group, set ratio 4:1, attack 3ms (slow to let transients through), release Auto, threshold until gain reduction shows 2–4dB, makeup gain. Soft Clip button on = gentle limiting at the output. When: on group channels (drums, bass+sub, pads) as the last device. When NOT: on individual elements — Glue Compressor is a bus tool. Tags: glue compressor, bus, drums, SSL, glue.

3. `reverb.json` — **Reverb** used in all 5 tracks, always on return tracks (not inserts). Steps: create a return track, drag Reverb onto it, set Dry/Wet 100%, choose a room size (Large Hall = 3.5s for pads, Small Room = 0.3s for drums), high-pass the return track at 200Hz with EQ Eight before the Reverb. Pre-Delay: 15ms for pads (attack stays clear before bloom), 30ms for snare (snap audible before room). When: anything that needs depth/space. When NOT: sub bass, kick (usually). Tags: reverb, space, hall, send, return, depth.

4. `chorus.json` — **Chorus** (and Ensemble mode) used in Simpler and as a standalone effect. Creates width by layering slightly detuned copies of a signal. Steps: add Chorus-Ensemble to a pad or synth track. Ensemble mode (3 voices) is richer than Classic mode (2 voices). Rate controls how fast the detuning oscillates. Depth controls how wide the detune swings. Amount/Mix controls the blend. For pads: Rate 0.4Hz, Depth 30–50%, Mix 30–50%. For light width on anything: Ensemble mode, Amount 20%, Classic mode. When: pads that feel narrow or static, any synth that needs width without reverb. When NOT: sub bass (phase cancellation in mono), kick. Tags: chorus, ensemble, width, stereo, detuning.

---

**TIER 2 — Used in 4/5 tracks:**

5. `limiter.json` — **Limiter** is on the master output in 4 of 5 remakes. Hard prevents signal from clipping above 0dBFS. Steps: add Limiter as the very last device on the Master channel. Set Ceiling to -0.3dBFS. Set Lookahead to 3ms (lets it react before peaks arrive). Watch the Gain Reduction meter — should catch peaks only, not constantly clamping. If clamping all the time: something upstream is too loud. Soft Clip ON = gentle saturation at the ceiling rather than hard brick-wall. When: always on the Master, last in chain, as the final safety net. When NOT: never as a creative effect on individual tracks — use Saturator for that. Tags: limiter, master, clipping, ceiling, output.

6. `saturator.json` — **Saturator** used in 4/5 remakes (MPH, IC, Sammy, BL3SS). Adds harmonic distortion for warmth and translation. Already planned in Task 27 effects deep dive — write detailed cheatsheet entry here. Steps: sub bass use (Drive 15%, Soft Clip, Dry/Wet 40%), pad use (Drive 10%, Soft Clip, Dry/Wet 25%), bus use (Drive 5%, Analog Clip). Waveshaper mode shows the distortion curve — Soft Clip curves gently, Hard Clip squares off sharply. When: sub bass that disappears on small speakers, pads that sound too digital. Tags: saturator, distortion, warmth, harmonics, soft clip.

7. `simpler-lfo.json` — **Simpler's internal LFO** is active in 4/5 remakes — it's the modulation source inside each Simpler in the Drum Rack. Used to add pitch wobble, filter movement, or amplitude tremolo to individual drum sounds. Steps: in Simpler, go to the LFO section, set Dest to Pitch for tape-stop effects, Filter for filter sweep, Amp for tremolo. Rate controls speed. Amount controls depth. Retrigger: on = LFO resets on each note (consistent per hit). When: making drum sounds feel less static — a subtle pitch LFO on a hat at very low depth makes it feel organic. Tags: simpler, lfo, modulation, pitch, filter, vibrato.

8. `simpler-filter.json` — **Simpler's internal Filter** is active in 4/5 remakes. Each Simpler has a built-in filter in the Classic tab. Used to shape the tone of a sample without adding a separate EQ or AutoFilter. Steps: in Simpler > Classic tab, enable Filter, choose LP/HP/BP type. Freq knob sets cutoff. Res knob sets resonance. Can be modulated by the Simpler's envelope or LFO. When: quick tone shaping on an individual drum sound (e.g. cut the high end of a snare to make it sit back, or HP a pad sample to remove rumble). Tags: simpler, filter, tone, cutoff, resonance.

---

**TIER 3 — Used in 3/5 tracks:**

9. `auto-filter.json` — **AutoFilter** used in MPH, Kettama, and IC. A filter with built-in LFO and envelope follower — can animate over time, unlike a static EQ. Steps: add AutoFilter to a track. Choose filter type (LP for lowpass sweep into drop, HP for removing lows). Set Cutoff at starting frequency. To sweep: automate the Cutoff in Arrangement view. For envelope follower: input Sidechain from a track and AutoFilter opens/closes with that signal's amplitude. LFO mode: sync to tempo, Rate = 1/4 or 1/8, creates a rhythmic filter pulse. When: filter sweeps in builds (automate LP cutoff from 200Hz to open over 8 bars), rhythmic filter effects on pads, creative filtering. Tags: auto filter, filter sweep, lfo, envelope follower, cutoff, build.

10. `compressor.json` — **Compressor** (standard, not Glue) used in MPH, Kettama, BL3SS. General-purpose dynamics control. Separate entry from GlueCompressor because their use cases are different. Steps: add Compressor to a track. Threshold controls when it starts. Ratio controls how much. Attack/Release shape the response. Knee: Hard knee = instant response at threshold, Soft knee = gradual transition. For sidechain: expand sidechain section, enable, set Audio From to kick. For vocal/bass smoothing: slow attack (20ms), auto release, ratio 3:1–4:1. When: sidechain pumping (sub bass, pads), dynamic control of a bass that plays at varying volumes, levelling individual elements. Tags: compressor, dynamics, threshold, ratio, attack, release, sidechain.

---

**TIER 4 — Used in 2/5 tracks:**

11. `echo.json` — **Echo/Delay** in MPH and Kettama. Ableton's Echo device (newer than the legacy Simple Delay) has more features. Steps: add Echo to a return track. Sync L/R to tempo: 1/8 synced = eighth-note delay, dotted 1/8 = the most common garage delay feel. Feedback controls how many repeats. Reverb inside Echo: adds reverb to the delay tails (the repeats decay into space). Filter section: HP/LP on the delay tails only (so the dry signal is unaffected). When: pad echoes that lock to the groove, subtle rhythmic texture on a synth, ping-pong delay for a stereo widening effect. Tags: echo, delay, feedback, tempo sync, ping pong, rhythm.

12. `overdrive.json` — **Overdrive** used in BL3SS and Kettama. Softer distortion than the Operator's built-in drive — more tube-like warmth than harsh clip. Steps: add Overdrive to a bass or synth track. Drive: 20–40% for warmth, 60–80% for grit. Tone knob: rolls off high frequencies of the distortion (higher = brighter, lower = darker). Dynamic: envelope-following drive — the harder you play, the more drive. When: bass that needs aggression (Reese bass), pads that need edge without full distortion. When NOT: sub bass (distortion adds harmonics but here they should be controlled — use Saturator instead for more precise harmonic control). Tags: overdrive, distortion, drive, grit, bass, warmth.

13. `flanger.json` — **Flanger** used in MPH. Creates a whooshing, comb-filtering effect by delaying and mixing the signal with itself. Steps: add Flanger to a pad or synth. Rate: how fast the effect sweeps (0.1–2Hz for slow sweep, sync to tempo for rhythmic). Feedback: how pronounced the metallic comb-filter effect is. Dry/Wet: 20–40% for subtle movement, higher for obvious flange. Hi-Pass/Lo-Pass controls: filter the effect so it only affects certain frequencies. When: breakdown sections where you want a synth to feel like it's moving or dissolving, transitional sweeps on pads, psychedelic movement on an arp. When NOT: as a constant effect throughout a track — flanger is most effective sparingly. Tags: flanger, modulation, sweep, comb, movement.

---

**TIER 5 — Kettama-specific (but highly useful):**

14. `operator.json` — **Operator** (FM synthesis) used in Kettama — the most powerful built-in Ableton synth. FM synthesis uses oscillators to modulate each other, creating complex harmonic timbres. Steps: Operator has 4 operators (A, B, C, D) arranged in an algorithm. Algorithm selector: determines which operators modulate which. Start with algorithm 1 (D→C→B→A, all in series). Operator A = carrier (the audible output). B, C, D = modulators (affect the timbre of A). To build a bass: Operator A frequency ratio 1.00, envelope fast decay. Operator B ratio 1.00, Amount (mod depth) at 20–40% (adds harmonics). For an organ bass: try algorithm 5 (A+C = parallel carriers), both at ratio 1.00. Tags: operator, FM synthesis, carrier, modulator, ratio, algorithm.

15. `gate.json` — **Gate** used in Kettama. A gate silences the signal when it drops below a threshold — the opposite of a compressor. Used to: chop sustained sounds rhythmically by sidechaining from a MIDI trigger, remove noise from a reverb tail, create gated reverb (1980s drum effect). Steps: add Gate to a pad track. Threshold: level below which the gate closes. Attack: how quickly the gate opens. Hold: minimum time the gate stays open. Release: how quickly it closes. For rhythmic gating: enable sidechain, set Audio From to a rhythmic MIDI trigger track. The gate opens only when that trigger fires — creating a rhythmic chop effect. Tags: gate, dynamics, noise gate, rhythmic, gating, sidechain.

16. `grain-delay.json` — **Grain Delay** used in Kettama. Granular processing — chops audio into tiny grains and plays them back with random pitch/position shifts. Creates textures from any audio source. Steps: add Grain Delay to a pad or atmospheric track. Spray: how random the grain position is (low = coherent, high = pitch clouds). Frequency: number of grains per second. Pitch: amount of random pitch variation. Delay time: base delay before grains play. When: breakdown textures (high spray = pad dissolves into clouds), transition effects, making a sample sound otherworldly. Not a traditional delay — it's a texture device. Tags: grain delay, granular, texture, spray, clouds, atmosphere.

17. `filter-delay.json` — **Filter Delay** used in Kettama. Three independent delays, each with a separate filter — sends different frequency ranges to different delay times. Creates complex, frequency-dependent echo patterns. Steps: each of the 3 delay bands has: HP and LP filter to isolate a frequency range, delay time (sync or ms), feedback. Example: band 1 (sub, LP 200Hz) = long delay, band 2 (mids) = medium delay, band 3 (highs, HP 2kHz) = short delay. The three frequency ranges echo at different rates, creating a movement that feels organic. When: complex textural pad effects, transition smears. Tags: filter delay, frequency, bands, complex delay, texture.

18. `amp.json` — **Amp** (amp simulation) used in Kettama. Simulates a guitar/bass amplifier — adds tube harmonics, cabinet colouration, and amp character. Steps: add Amp to a bass or synth track. Choose Amp Type: Clean = gentle saturation, Ext Bass = enhanced low-end response, Heavy = aggressive gain. Drive: overall input gain into the amp. Bass/Middle/Treble: amp tone controls (different from EQ — these interact like a real amp). Dry/Wet: blend original with amp-processed signal. When: bass that needs warmth or grit with more character than Saturator, synth that needs to feel "played through an amp." Tags: amp, amplifier, tube, drive, warmth, bass.

---

**TIER 6 — Workflow and routing (not from the scan but essential):**

19. `groove-pool.json` — Groove Pool workflow: drag grooves to MIDI clips, global groove amount knob, extracting groove from a reference audio clip. Tags: groove, swing, timing, feel.

20. `automation.json` — Arrangement automation: Cmd+click to add breakpoints, automation lanes, unlinking clip envelopes, drawing filter sweeps. Tags: automation, movement, filter sweep, dynamics.

21. `return-tracks.json` — Return tracks and send routing: creating a reverb return, send knob routing, pre vs post fader. Tags: sends, reverb, routing, return track.

22. `utility-mono.json` — Utility device: Width to 0% for mono sub bass, Mid/Side balance, Gain for makeup. Tags: utility, mono, width, stereo.

23. `instrument-rack.json` — Instrument Rack for layering synths: add two Serum instances to one MIDI track, balance volumes, high-pass one and low-pass the other for frequency layering. Tags: instrument rack, layering, macro, synthesis.

24. `audio-effect-rack.json` — Audio Effect Rack: parallel processing chains, Dry/Wet per chain, Macro knobs. Tags: rack, macros, parallel, chains.

25. `midi-effects.json` — MIDI Effects: Chord (add intervals automatically), Scale (lock notes to a key), Arpeggiator basics. Tags: midi, chord, scale, arpeggiator.

26. `clip-envelopes.json` — Clip envelopes: per-clip automation of volume/pitch/device params, linked vs unlinked mode. Tags: clip envelope, automation, modulation.

27. `arrangement-view.json` — Arrangement view workflow: session to arrangement, loop brace, duplicate section, track freeze/flatten. Tags: arrangement, workflow, freeze, flatten.

28. `resampling.json` — Resampling: route Master to audio track, record own output, then process further. Tags: resampling, bounce, flatten.

29. `track-grouping.json` — Track Groups: select tracks, Cmd+G to group, use as bus. Colour coding, naming. Drum group → Glue Compressor on the group. Tags: groups, bus, routing, organisation.

30. `operator-sub-bass.json` — Operator sub bass from scratch: Sine carrier, no modulators, pitch envelope for punch. Tags: operator, sub bass, fm synthesis.

---

**Step: Update index.js** — import all 30 entries, export.

**Step: Verify search works across all entries**

**Step: Commit**
```bash
git commit -m "feat: expand cheatsheet to 30 entries — grounded in remake device scan"
```

---

### Task 20: Drum rack .adg downloads

**Goal:** Add a "Download Kit" button to each TrackDetail page that downloads the drum rack extracted from the source .als file as a `.adg`.

**Files:**
- Create: `scripts/extract-drum-racks.py` — Python script to extract DrumGroupDevice from each .als and save as .adg
- Create: `public/drum-kits/mph-raw-drums.adg` (and 4 others)
- Modify: `src/pages/TrackDetail.jsx`

**Step 1: Write extraction script**

`scripts/extract-drum-racks.py`:
```python
import gzip, xml.etree.ElementTree as ET, os

tracks = [
  ("MPH - Raw", "/path/to/MPH - Raw.als", "mph-raw-drums"),
  ("KETTAMA - It Gets Better", "...", "kettama-drums"),
  # etc
]

for name, als_path, out_name in tracks:
    with gzip.open(als_path) as f:
        tree = ET.parse(f)
    root = tree.getroot()
    for drum in root.iter('DrumGroupDevice'):
        adg_root = ET.Element('Ableton', {
            'MajorVersion': '5', 'MinorVersion': '10.0_377',
            'SchemaChangeCount': '3', 'Creator': 'Ableton Live 10.1.4', 'Revision': ''
        })
        adg_root.append(drum)
        xml_bytes = b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(adg_root, encoding='unicode').encode('utf-8')
        out = f"../public/drum-kits/{out_name}.adg"
        with gzip.open(out, 'wb') as f_out:
            f_out.write(xml_bytes)
        print(f"Written: {out}")
        break
```

**Step 2: Run the script, verify .adg files in public/drum-kits/**

**Step 3: Add download button to TrackDetail**

Below the Tracks section, add:
```jsx
{track.has_drum_rack && (
  <section className="mb-8">
    <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
      Download Kit
    </h2>
    <a
      href={`/drum-kits/${track.id}-drums.adg`}
      download
      className="inline-flex items-center gap-2 px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded font-mono text-sm text-zinc-300 transition-colors"
    >
      ↓ {track.title} Drum Rack (.adg)
    </a>
    <p className="text-xs text-zinc-600 mt-2">
      Drag directly into an Ableton session. Samples must be in the original project folder.
    </p>
  </section>
)}
```

**Step 4: Add `has_drum_rack: true` to track JSON files that have drum racks**

**Step 5: Verify download works — browser should prompt to save .adg file**

**Step 6: Commit**
```bash
git commit -m "feat: drum rack .adg downloads on track detail pages"
```

---

## Phase 2D: Deploy & CI Fix

### Task 21: Fix Cloudflare Pages CI (auto-deploy on push)

**Goal:** Every `git push` to main should auto-deploy without manual wrangler commands.

**Option A — wrangler.toml approach:**

Add to `wrangler.toml`:
```toml
[assets]
directory = "./dist"
```

Change deploy command in Cloudflare Pages settings to:
```
npx wrangler deploy --assets=./dist
```

**Option B — Remove deploy command entirely:**

If Cloudflare allows leaving the deploy command blank (try again — earlier it said required but this may be configurable in Settings vs initial setup), leave it blank. Cloudflare Pages with GitHub integration is supposed to handle upload automatically.

**Option C — GitHub Actions:**

Add `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Cloudflare Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - run: npm run build
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: pages deploy dist --project-name music-theory-learner
```

Add `CLOUDFLARE_API_TOKEN` as a GitHub repository secret (not Cloudflare env variable). This is the most reliable approach.

**Recommended: Option C.** GitHub Actions gives full control and the token management is cleaner.

---

## Content Backlog Summary

| Category | Count | Status |
|---|---|---|
| Beginner reps | 7 | 3 done → Task 13 adds 4 |
| Intermediate reps | 7 | 0 done → Task 14 adds all 7 |
| Serum-specific reps | 4 | 0 done → Tasks 23–25 add all 4 |
| Entry/mid spinoffs | 4 | 0 done → Task 15 adds all 4 |
| Full spinoffs | 3 | 1 done (Kettama) → Task 16 adds 2 |
| Originals | 4 | 0 done → Task 16 adds all 4 |
| Theory deep dives | 10 | 0 done → Tasks 11–12 add 7 core theory dives; Tasks 26–28 add arrangement/effects dives |
| Cheatsheet entries | 30 | 3 done → Task 19 adds 27 (grounded in .als device scan) |
| Serum cheatsheet entries | 3 | 0 done → Task 22 adds 3 (oscillators, filter, envelopes) |
| Effects cheatsheet entries | 4 | 0 done → Tasks 26–27 add reverb-send, compression-basics, delay-tempo-sync, saturation |
| Gain staging cheatsheet | 1 | 0 done → Task 27 adds 1 |

**Total builds after Phase 2:** 29 (25 music builds + 4 Serum-specific reps).
**Total theory deep dives:** 10 (7 theory/sound-design + 3 arrangement deep dives from Task 28).
**Total cheatsheet entries:** 41 (30 device entries + 3 Serum + 4 effects + 1 gain staging + 3 existing).
**Note:** Deep dive count does not include the 3 effects deep dives from Task 26 and signal-flow/saturation/EQ from Task 27 — those are 6 additional deep dives making the total 13 if counted separately. All live in the Deep Dives tab.

---

## Phase 2E: Serum V2 Learning Track

**User context:** Has Serum V1 and V2. Uses V2. Has never built a sound from scratch — only used presets. Goal: confident patch building for UK garage by end of Phase 2. All V2 UI terminology used throughout.

### Task 22: Serum V2 — UI orientation deep dive + cheatsheet

**Goal:** The user understands every section of Serum V2's interface before touching a parameter. Anchored to sounds they've already heard in the source tracks.

**Files:**
- Create: `src/content/theory/deep-dives/serum-v2-ui.json`
- Create: `src/content/cheatsheet/serum-v2-oscillators.json`
- Create: `src/content/cheatsheet/serum-v2-filter.json`
- Create: `src/content/cheatsheet/serum-v2-envelopes.json`

**Deep dive — `serum-v2-ui.json`:**

Sections:
1. **The four panels** — OSC (make sound), FILTER (shape it), ENV/LFO (move it over time), FX (finish it). Everything in Serum lives in one of these four areas.
2. **OSC A and OSC B** — Each oscillator has: a wavetable (the raw shape of the sound), WT POS (which point in the wavetable), OCT/SEMI/FINE (tuning), UNISON (how many copies, and how detuned). V2 difference from V1: the wavetable display is larger and interactive — you can drag the WT POS knob while watching the waveform change in real time.
3. **The wavetable** — A wavetable is a collection of single-cycle waveforms. WT POS moves through them. Basic Shapes goes from sine (smooth, pure) → triangle → sawtooth (bright, buzzy) → square (hollow). The position you pick determines the starting character of the sound.
4. **UNISON** — Sets how many copies of OSC A play simultaneously, slightly detuned from each other. 1 voice = mono, focused. 4 voices at 12 cents = wide, warm pad. 8 voices at 20 cents = huge wall-of-sound. Detune creates the chorus effect — copies beating against each other. In V2 the unison modes include HYPR (stacks and fattens in a specific way) and STACK.
5. **SUB oscillator** — A separate pure sine wave one octave below OSC A. Only adds fundamental frequency — no harmonics. Great for reinforcing the very bottom of a sub bass without adding brightness.
6. **NOISE oscillator** — Adds a noise layer (white, pink, etc.) to the patch. Used sparingly for breath and texture on pads.
7. **FILTER** — The filter removes frequencies. Low Pass (LP) = cuts highs, lets lows through. High Pass (HP) = cuts lows. The cutoff knob is the frequency at which cutting starts. Resonance adds a peak at the cutoff — too much = squeaky. For pads: LP at 60–70% cutoff. For bass: LP fully open or off. V2 filter types: MG Low (Moog-style, smooth), Dirty (adds grit), the new PRO filters (more aggressive). Use MG Low for pads.
8. **ENV 1 (Amplitude envelope)** — Controls the volume shape over time. Attack = how long it takes to reach full volume from silence. Decay = how quickly it falls after the peak. Sustain = level it holds while the key is held. Release = how long it takes to go silent after the key is released. Pad: slow attack (200–400ms), high sustain, long release. Bass: zero attack, high sustain, short release. Stab: zero attack, short decay, zero sustain, short release.
9. **ENV 2 and LFOs** — Additional modulators. Drag ENV 2 or an LFO onto any knob to create movement. LFO on filter cutoff = filter sweep. ENV 2 on pitch = pitch envelope (punchy bass attack). Rate and shape determine how fast and what shape the movement takes.
10. **FX tab** — Processing after the oscillators. In V2: DISTORT, HYPR (ensemble chorus), DIMENSION (subtle stereo width), CHORUS, FLANGER, PHASER, COMPRESSOR, DELAY, REVERB, EQ, FILTER (second filter). For pads: CHORUS + REVERB. For bass: nothing, or just COMPRESSOR. Order matters — signal flows left to right.
11. **MATRIX tab** — V2's modulation matrix. Shows every modulator → destination connection. Useful for seeing what's connected to what when a patch gets complex.
12. **V2 vs V1 key differences** — Larger wavetable display. More FX slots. HYPR mode in UNISON and FX. New filter types. Better UI scaling. Matrix view more readable. The fundamental architecture is identical — if you learn V2 you understand V1.

MIDI examples: show example MIDI notes for each sound type discussed (pad chord, sub bass note, stab note).

Practice exercise: "Open Serum V2. Go to Init Preset. On OSC A, slowly drag WT POS from 0 to 100% while holding a single note. Describe in one sentence what you hear changing at the beginning, middle, and end of the sweep."

Key takeaway: "Serum is four things: make a sound (OSC), shape its brightness (FILTER), control how it moves over time (ENV/LFO), and finish it (FX). Every sound you'll ever build is those four steps in that order."

**Cheatsheet — `serum-v2-oscillators.json`:** Quick reference for wavetable navigation, WT POS, unison settings for common UK garage sounds. Steps: set up pad OSC, set up sub bass OSC, set up stab OSC. Tags: serum, oscillator, wavetable, unison.

**Cheatsheet — `serum-v2-filter.json`:** Filter types and when to use each. Steps: add LP filter for pad, set cutoff + resonance, hear the difference between MG Low and Dirty. Tags: serum, filter, low pass, cutoff, resonance.

**Cheatsheet — `serum-v2-envelopes.json`:** ENV 1 shapes for common sounds. Steps: set pad envelope, set bass envelope, set stab envelope, drag ENV 2 onto filter cutoff. Tags: serum, envelope, attack, release, modulation.

**Step: Commit**
```bash
git commit -m "feat: Serum V2 UI deep dive + oscillator/filter/envelope cheatsheets"
```

---

### Task 23: Serum V2 — Build a sub bass (garage-specific)

**Goal:** A dedicated guided build rep that walks through building a clean, punchy sub bass in Serum V2 from Init Preset. No presets. Every step explained.

**File:** `src/content/guided-builds/reps/rep-serum-sub-bass.json`

**Build details:**
- ID: `rep-serum-sub-bass`
- Title: "Sub Bass in Serum V2"
- Build type: rep
- Difficulty: beginner
- BPM: 136
- Key: E minor
- Estimated time: 20 mins
- Source: MPH Raw (sub bass reference)

**Steps (~10):**

1. Open Serum V2. Load Init Preset (right-click preset name → Init Preset). You start with a basic saw wave — you'll replace everything.
2. OSC A: click the wavetable name, select Basic Shapes. Drag WT POS all the way left — pure sine wave. This is your entire sub bass tone. No OSC B, no noise, no sub OSC needed yet.
3. UNISON: set to 1 voice. Subs must be mono — multiple detuned voices create phase cancellation in the low end that destroys the sub on mono systems.
4. FILTER: disable it entirely (click the FILTER power button off). A filter on a sub bass adds unnecessary processing. The sub should be as pure as possible.
5. ENV 1: Attack 0ms. Decay 0. Sustain 100%. Release 150ms. The sub should respond instantly and release cleanly. Slow attack on a sub = the note feels late; it misses the kick transient.
6. Sub OSC: enable it. Set to Sine. Set level to -6dB below OSC A. The Sub OSC adds the fundamental one octave below — you feel it more than hear it. Compare with and without.
7. FX tab: turn everything OFF. No chorus, no reverb, no distortion. Any FX on a sub introduces phase and harmonics that cloud the low end.
8. Program a simple bass line: Gb1 → Db1 → Bb1 (the Kettama root movement, transposed to start on Gb). Hold each note for ~2 beats. Listen to how the pitch movement implies chord changes.
9. Add a Utility device in Ableton after Serum: set Width to 0% (mono). Check in a DAW meter that the sub is centered. A wide sub will disappear in mono.
10. Compare your sub against the sub in a reference track (Kettama or IC Slow Burner) at the same volume. Is yours as clean? As punchy? Adjust ENV 1 release if it sounds muddy between notes.

**Step: Commit**
```bash
git commit -m "feat: rep — sub bass in Serum V2 from scratch"
```

---

### Task 24: Serum V2 — Build a chord pad (garage-specific)

**Goal:** Walk through building the lush Kettama-style pad in Serum V2 from Init Preset. Teaches the full oscillator → filter → envelope → FX chain.

**File:** `src/content/guided-builds/reps/rep-serum-chord-pad.json`

**Build details:**
- ID: `rep-serum-chord-pad`
- Title: "Chord Pad in Serum V2"
- Difficulty: beginner
- BPM: 140, Key: Bb minor
- Source: Kettama — It Gets Better

**Steps (~12):**

1. Init Preset in Serum V2.
2. OSC A: Basic Shapes, WT POS ~25% (soft, slightly rounded — not pure sine, not full saw). This is the tonal foundation.
3. OSC B: enable. Same wavetable and WT position as OSC A. Tune fine to +7 cents (FINE knob, drag up 7). Lower its volume by 3dB. This creates the beating/chorus effect between A and B — two oscillators slightly out of tune with each other.
4. UNISON on OSC A: 4 voices, detune 12 cents, blend 50%. Now you have OSC A with 4 detuned copies + OSC B slightly above them — 5 slightly different versions of the same waveform. This width is the warmth.
5. FILTER: enable, select MG Low 24. Cutoff ~60% (about 10 o'clock). Resonance 8%. The filter rounds off the bright upper harmonics, making the sound warm rather than harsh.
6. ENV 1: Attack 300ms (slow — the pad fades in). Decay 0. Sustain 100%. Release 1500ms (long — chords overlap slightly as they change).
7. LFO 1: shape Sine, Rate 0.25 Hz (one cycle every 4 seconds). Drag LFO 1 onto the Filter Cutoff knob — a mod dot appears. Set the modulation amount to 5%. The filter now breathes very gently in and out. This is the living quality.
8. FX tab: Enable CHORUS (click the power dot). Rate 0.40, Depth 25%, Mix 40%. Enable REVERB: Size 0.75, Decay 0.65, Pre-delay 15ms, Mix 30%. Enable EQ: high-pass at 120Hz (pads don't need anything below that — the sub bass handles it).
9. V2 note: In V2 the HYPR mode in FX is a more complex ensemble effect. Try it at 30% mix as an alternative to standard CHORUS — it adds a more organic, slightly vintage width.
10. Program a Gbmaj7 chord: Gb3, Bb3, Db4, F4. Hold for 4 bars and listen. Does it feel dreamy and warm? The F4 on top is the major 7th — the note that makes it shimmer.
11. Add a Saturator in Ableton after Serum: Drive 12%, Soft Clip mode, Dry/Wet 30%. This adds analogue warmth — the sound feels less digital.
12. Compare against the Kettama reference: solo your pad against the original. Notice the similarities and differences. Adjust the FILTER cutoff or REVERB mix until yours feels similarly deep.

**Step: Commit**
```bash
git commit -m "feat: rep — chord pad in Serum V2 from scratch"
```

---

### Task 25: Serum V2 — Reese bass, chord stabs, and layering

**Goal:** Teach the three remaining Serum sounds used in the source tracks: Reese bass (detuned saws), chord stabs (Sammy Virji style), and how to layer two Serum patches together.

**Files:**
- `src/content/guided-builds/reps/rep-serum-reese-bass.json`
- `src/content/guided-builds/reps/rep-serum-stab.json`
- `src/content/theory/deep-dives/serum-layering.json`

**Reese bass build (~8 steps):**
1. Init Preset.
2. OSC A: Basic Shapes, WT POS all the way right (sawtooth). This is the core of a Reese — raw, harmonically rich.
3. OSC B: enable. Same saw wavetable. Tune FINE to -14 cents (slightly flat). The beating between A and B is the Reese sound.
4. UNISON on both: 2 voices, detune 8 cents. Keep it controlled — too much unison makes the Reese lose its focus.
5. FILTER: MG Low 24. Cutoff ~40% (darker than the pad). Resonance 15% (a bit of peak adds the growl).
6. ENV 2: drag onto Filter Cutoff. Attack 0, Decay 200ms, Sustain 0%, amount +20%. Now the filter opens briefly when each note plays then closes — the "wah" envelope. This is what gives the Reese its movement.
7. ENV 1: Attack 10ms (slightly soft), Sustain 100%, Release 300ms.
8. Program G1 → D1 → B1 (a minor root movement). Listen for the growl and movement. Adjust ENV 2 Decay between 100ms and 400ms to hear how it changes the character.

**Chord stab build (~8 steps):** Based on Sammy Virji's major chord stabs (G#maj → Emaj → Bmaj). Init Preset → OSC A sawtooth → FILTER HP at 300Hz (cuts the low end — stabs live in the mid) → ENV 1 Attack 0, Decay 400ms, Sustain 0% (stab shape: hits and fades) → FX Distort lightly → program G#3+C4+D#4 (G# major chord voicing).

**Layering deep dive — `serum-layering.json`:** Why you layer two Serum instances (one for the body of a sound, one for the attack/texture). How to use Ableton's Instrument Rack to layer two Serum patches on one MIDI track. How to balance them with volume and frequency — high-pass one, low-pass the other. Example: layer the sub bass (pure sine) with a mid-bass texture patch (light saw with HP at 200Hz) for a bass with both weight and character.

**Step: Commit**
```bash
git commit -m "feat: reps — Reese bass, chord stabs, layering deep dive in Serum V2"
```

---

## Updated Task Order (with Serum track)

1. Task 11 — Theory Deep Dives Part 1
2. **Task 22 — Serum V2 UI orientation** ← do this early so all future builds make sense
3. **Task 23 — Serum sub bass** ← first practical Serum skill
4. **Task 24 — Serum chord pad** ← second practical Serum skill
5. Task 12 — Theory Deep Dives Part 2
6. Task 17 — Progress tracking
7. Task 18 — Daily practice
8. Task 13 — Beginner reps 4–7
9. **Task 25 — Serum Reese + stabs + layering**
10. Task 14 — Intermediate reps 8–14
11. Task 15 — Spinoffs 2–4
12. Task 19 — Cheatsheet expansion
13. Task 20 — Drum rack downloads
14. Task 16 — Full spinoffs + originals
15. Task 21 — CI fix

**Serum V2 competency progression:**
- After Task 22: understand what every section of the UI does
- After Task 23: can build a sub bass from scratch
- After Task 24: can build a chord pad from scratch
- After Task 25: can build a Reese bass, a stab, and layer two patches
- By Task 14+: all intermediate reps use Serum — they reinforce the skills in musical context

**Total Serum content in Phase 2:**
- 1 UI deep dive (Task 22)
- 4 Serum-specific reps (Tasks 23–25: sub bass, chord pad, Reese, stab)
- 1 layering deep dive (Task 25)
- 3 Serum cheatsheet entries (oscillators, filter, envelopes)
- Serum steps embedded in all spinoffs and intermediate reps

---

## Phase 2F: Effects — When, Why, and How

**Design principle:** Every effects section is taught as a decision, not a tutorial. The question is always "why would you reach for this tool?" not "what are all the parameters?". Like padel — you don't learn what a flat smash is in isolation, you learn when the court position and ball height make it the right shot. Same here: you learn what situation calls for reverb vs delay vs compression vs saturation.

### Task 26: Effects deep dives — Reverb, Delay, Compression

**Files:**
- Create: `src/content/theory/deep-dives/effects-reverb-delay.json`
- Create: `src/content/theory/deep-dives/effects-compression.json`
- Create: `src/content/cheatsheet/reverb-send.json`
- Create: `src/content/cheatsheet/compression-basics.json`
- Create: `src/content/cheatsheet/delay-tempo-sync.json`

---

**Deep dive — `effects-reverb-delay.json`:**

Title: "Reverb and Delay — Space vs Time"
Subtitle: "Two tools that create depth. Knowing which one to reach for changes everything."

Sections:

1. **What they actually do**
Reverb simulates a physical space — it adds a sense of the sound existing in a room, hall, or cave. The bigger the space, the longer the decay. Delay is an echo — a copy of the sound that plays back after a set time, then again, then again (each repeat slightly quieter). Both add depth. They feel completely different.

2. **When to use reverb**
Reverb is the right tool when: you want an element to feel like it exists in a space rather than floating in a void. Chord pads (large hall, 3–4s decay), snare/clap (small room, 0.4s — just enough to stop it sounding like a gunshot in a cupboard), atmospheric textures (very long plate). The rule: the more present you want something, the shorter the reverb. The more distant, the longer.

When NOT to use reverb: sub bass (reverb smears the low end and creates mud — reverb on sub bass is one of the most common beginner mistakes), kick drum (usually dry or with just a tiny room reverb), anything that needs to be tight and rhythmically locked (too much reverb blurs the timing).

3. **Send vs insert reverb — this matters a lot**
Insert = reverb directly on the track. The reverb processes only that track. Every element has its own separate reverb space. Sounds disconnected. Send = reverb on a return track. Multiple elements feed into the same reverb. Everything shares one room. Sounds like a cohesive environment. For UK garage: one large reverb send (3.5s hall) for pads and atmosphere, one smaller send (0.4–0.8s room) for drums. Never use insert reverb on your main elements — always sends.

4. **Pre-delay — the underused parameter**
Pre-delay is a gap before the reverb tail starts. Without pre-delay, the reverb smears the attack of the sound (it starts reverbing immediately). With 15–25ms pre-delay, the dry signal attacks cleanly, then the reverb follows. Kettama's pad has pre-delay — you hear the chord hit before the reverb bloom. This gives clarity while still having depth. On drums, pre-delay (30–50ms on a snare reverb send) lets the snap of the snare be heard before the room fills in.

5. **When to use delay**
Delay is the right tool when: you want rhythmic interest, movement, or echo. Tempo-synced delay (1/8, 1/4, 1/16 note) creates repeats that lock to the groove. A pad with a dotted 1/8 delay creates a rhythmic pulse without adding new notes. A snare with 1/8 delay creates a ghost echo that feels like a second drummer playing off the beat. Unlike reverb, delay has a defined rhythmic structure — you can predict where the repeats will land.

When NOT to use delay: on sub bass (same problem as reverb — low-frequency smear), when you want something to sit still (delay inherently implies movement), in a dense mix where the repeats will fight with other elements.

6. **High-passing the reverb/delay sends**
This is non-negotiable. Always add an EQ Eight to your reverb and delay return tracks. High-pass at 200–300Hz. This removes low-frequency reverb/delay (which is just mud). You want the space and shimmer — not the bass bloom. This single move will immediately clean up a muddy mix.

7. **The decision tree**
Does the element need to feel like it's in a physical space? → Reverb.
Does the element need rhythmic echoes that move with the groove? → Delay.
Does it need both space AND movement? → Both sends, at different levels.
Is it a sub bass or kick? → Neither, or the absolute minimum.
Does the mix feel muddy with the reverb on? → High-pass the send at 200Hz and/or reduce the send level.
Does the mix feel dry and disconnected despite the reverb? → Everything is using insert reverb — switch to a shared send.

MIDI examples: show Ableton routing diagrams as text (pad → reverb send routing).

Practice exercise: "Open your kettama-study project. Solo the chord pads. Toggle the reverb send on and off. Then sweep the reverb send high-pass filter from 0Hz to 400Hz while the track loops. Describe what you hear at: 0Hz (no HP), 200Hz, 400Hz."

Key takeaway: "Reverb puts things in a room. Delay makes things echo in time. Use sends, not inserts. Always high-pass the send. Sub bass gets neither."

---

**Deep dive — `effects-compression.json`:**

Title: "Compression — Control, Glue, and Pump"
Subtitle: "The most misunderstood effect in production. It's not just 'making things louder'."

Sections:

1. **What compression actually does**
A compressor automatically turns down loud moments. When a signal exceeds the threshold, the compressor reduces its volume by the ratio you set. After compression, you can turn the whole thing back up (with makeup gain) — the result is a more consistent, controlled sound. That's it. But the how, when, and how much completely changes the character of the result.

2. **The four parameters and what they actually mean in context**
Threshold: the level at which the compressor starts working. Lower threshold = more compression (more moments get compressed). Attack: how quickly the compressor responds when the signal exceeds threshold. Fast attack = compressor catches the transient and softens it. Slow attack = compressor misses the transient and lets it through (adds punch). Release: how quickly the compressor stops working after the signal drops below threshold. Too fast = pumping/breathing. Too slow = the compressor never fully lets go (kills dynamics). Ratio: how much it turns down. 2:1 is gentle. 4:1 is noticeable. 10:1+ is limiting.

3. **Slow attack = more punch (this is counterintuitive)**
On a kick or snare: a slow attack (30–50ms) means the compressor doesn't react to the initial transient. The snap/click of the hit gets through uncompressed — you hear it clearly. Then the compressor kicks in and controls the body of the sound. Result: punchy hit with a controlled tail. Fast attack = compressor catches the transient and rounds it off = soft, pillowy hit. In UK garage: kicks and snares usually want slow attack, fast release. Pads want slow attack and slow release (almost no compression — let the envelope from Serum handle the shape).

4. **Sidechain compression (you already know this one)**
The kick triggers the compressor on the pad and sub bass. The compressor doesn't respond to the pad's own volume — it responds to the kick. Already covered in the Kettama build in detail. Key reminder: ratio 6:1 and fast attack (0.5ms) for the sub, ratio 3:1 and 2ms attack for the pads.

5. **Glue compression on a bus**
Put a light compressor (ratio 2:1, slow attack 30ms, medium release 100ms, threshold just barely touching) on a group of tracks — like the DRUMS group. The compressor very gently ties them together: when the kick hits hard, it slightly ducks the hats and clap. This is "glue" — subtle, not obvious, but the drums start to feel like one instrument instead of individual samples stacked together.

6. **Limiting — the last step**
A limiter is a compressor with a very high ratio (10:1 to ∞:1) and a fast attack. Its job is to prevent the signal from ever exceeding 0dBFS (and clipping). Put a limiter as the very last plugin on your master channel. Ceiling: -0.3dBFS. Use it to catch peaks, not to make things loud. If your limiter is reducing gain by more than 2–3dB constantly, something earlier in the chain is too loud.

7. **The decision tree**
Does the kick feel weak or undefined? → Try slow attack on the kick compressor to let the transient through.
Does the track feel like a collection of separate elements rather than a cohesive mix? → Add a bus compressor on your main groups (2:1, slow attack, glue settings).
Does the sub bass fight the kick? → Sidechain compression (already in your arsenal).
Does the pad feel too dynamic (sometimes too loud, sometimes too quiet)? → Light compression on the pad (4:1, slow attack, medium release) to even it out.
Is the master channel clipping? → Limiter with ceiling -0.3dBFS.
Are you reaching for a compressor because "it should go on everything"? → Stop. Don't compress what doesn't need it.

Practice exercise: "On your kick track, add a Compressor. Set ratio 4:1. Try attack at 1ms vs 50ms. What happens to the punch of the kick at each setting? Now try the same with the release: 50ms vs 200ms. What happens to the tail?"

Key takeaway: "Compression is volume control over time. Slow attack = more punch. Fast attack = more control. Sidechain = the pump. Glue = the glue. On everything = wrong."

---

**Cheatsheet — `reverb-send.json`:** Steps for setting up a reverb send in Ableton: create return track, add Reverb, set dry/wet 100%, route pad send to A, HP the return at 200Hz. Tags: reverb, send, return track, depth.

**Cheatsheet — `compression-basics.json`:** Steps for compressing a kick: slow attack, fast release, threshold, makeup gain. And sidechain setup quick reference. Tags: compression, kick, punch, sidechain, dynamics.

**Cheatsheet — `delay-tempo-sync.json`:** Steps for adding a tempo-synced delay to a pad: set sync mode, choose 1/8 or dotted 1/8, feedback 30%, filter the repeats with HP. Tags: delay, tempo sync, echo, rhythm.

**Step: Verify + commit**
```bash
git commit -m "feat: effects deep dives — reverb/delay and compression with decision trees"
```

---

### Task 27: Effects deep dives — Saturation, EQ strategy, Signal flow

**Files:**
- Create: `src/content/theory/deep-dives/effects-saturation.json`
- Create: `src/content/theory/deep-dives/effects-eq-strategy.json`
- Create: `src/content/theory/deep-dives/signal-flow.json`
- Create: `src/content/cheatsheet/saturation.json`

---

**Deep dive — `effects-saturation.json`:**

Title: "Saturation and Distortion — Warmth, Grit, and Character"
Subtitle: "Why every digital sound benefits from a little analogue dirt."

Sections:

1. **What saturation does that nothing else does**
Digital audio is perfectly clean. Too clean. Real analogue hardware — tape machines, tube amplifiers, transformer-based gear — introduces harmonic distortion: additional frequencies that weren't in the original signal. These added harmonics make sounds feel warmer, more present, more alive. Saturation in a DAW simulates this. It's not "making things louder" or "making things distorted" — at low settings it's nearly inaudible but completely changes the feel.

2. **Harmonics — what's actually being added**
When you saturate a 100Hz sine wave, you get: 200Hz (second harmonic), 300Hz (third), 400Hz (fourth), etc. Even harmonics (2nd, 4th) — generated by tape and tube — sound warm and musical. Odd harmonics (3rd, 5th) — generated by transistors and digital clipping — sound harsher. This is why "tape saturation" sounds warm and "digital clip" sounds harsh. Ableton's Saturator with "Soft Clip" mode generates more even harmonics. "Hard Clip" generates more odd harmonics. Use Soft Clip for warmth, Hard Clip for grit.

3. **On a sub bass — the most important use**
A pure sine wave sub bass has no harmonics above the fundamental. On a small speaker (phone, earbuds, laptop), speakers physically can't reproduce 60Hz — so the sub disappears. Saturation adds harmonics at 120Hz, 180Hz, 240Hz — frequencies that small speakers CAN reproduce. The listener hears those harmonics and their brain fills in the missing fundamental. Result: a sub bass that translates to small speakers. Drive: 10–15%. Dry/wet: 30–50%. This is not about making the sub dirty — it's about making it audible everywhere.

4. **On chord pads**
Light saturation (Drive 10%, Soft Clip, Dry/Wet 25–35%) adds the quality of a synth having been recorded through real hardware. It glues the Serum pad to the rest of the mix — digital pads often feel like they're floating above the track rather than inside it. Saturation is the glue. This is why the Kettama spinoff build includes a Saturator after Serum.

5. **On the drum bus**
A Saturator on the DRUMS group at very low drive (5–8%) adds subtle tape character to the whole kit. The kick gets slightly more weight, the hats get slightly more air. Compare the kit before and after — you can barely hear the difference, but with it off the drums feel more plastic.

6. **When NOT to saturate**
Sub bass that's already in a full mix (saturation multiplies the effect of existing harmonics — can make a sub bass that was balanced become too present in the 200–400Hz range). Anything that's supposed to be clean and clinical (certain electronic stabs where the digital precision is intentional). When you've already got chorus on a pad — chorus and saturation both add harmonic complexity, stacking them can make things muddy.

7. **The decision tree**
Does the sub bass disappear on small speakers/earbuds? → Light saturation on the sub (harmonics = translation).
Does the pad feel digital and disconnected from the mix? → Light saturation after Serum (Soft Clip, 25% mix).
Does the whole track feel cold and clinical? → Bus saturation on the master at very low drive (3–5%).
Do you want grit and aggression (Reese bass, distorted stab)? → Higher drive (20–40%), Hard Clip or Waveshaper mode.
Is the sound getting muddy after saturation? → High-pass the saturated signal above whatever frequency is building up.

Practice exercise: "Load your sub bass patch. Add Saturator (Soft Clip, Drive 15%, Dry/Wet 40%). Play a single note. Switch between headphones and your phone speaker. Does the sub translate better with saturation on vs off on the phone?"

Key takeaway: "Saturation adds harmonics. Even harmonics = warmth. Odd harmonics = grit. Sub bass needs it to translate to small speakers. Everything else uses it for character."

---

**Deep dive — `effects-eq-strategy.json`:**

Title: "EQ as a Mixing Tool — Cutting Space, Not Just Boosting"
Subtitle: "Why cutting is always better than boosting, and how every element needs its own frequency home."

Sections:

1. **The frequency map of a UK garage track**
Sub bass: 40–100Hz (felt, not heard on small speakers). Bass body: 100–200Hz. Low-mids (where mud lives): 200–500Hz. Mids (pads, chords): 500Hz–2kHz. Presence (hats, pad attack, vocal clarity): 2–5kHz. Air (hat shimmer, reverb tails): 5–16kHz. Everything above 16kHz: inaudible to most adults, often just noise. UK garage is a low-end driven genre — the sub bass and kick own 40–150Hz. Everything else gets out of the way below that.

2. **High-passing everything that doesn't need low end**
This is the single most impactful EQ move in any mix. Every non-bass element — pads, hats, atmosphere, reverb sends, clap — has content below 100–300Hz that's not useful. It's just competing with the sub and kick, adding mud. Solution: high-pass filter. Pads: HP at 120–150Hz. Hats/claps: HP at 200–400Hz. Reverb sends: HP at 200Hz. Atmosphere drone: HP at 200Hz. After doing this to every non-bass element, the sub and kick suddenly have more room and feel bigger without changing the sub at all.

3. **Cutting before boosting**
If something sounds dull, the instinct is to boost the highs. But often the better move is to cut the muddiness that's masking the highs. Cut 250–400Hz on a dull pad by 3–4dB before reaching for a high shelf boost. Cuts make space; boosts emphasise. A track full of boosts is a loud, fighting mix. A track full of surgical cuts with rare, purposeful boosts is a balanced mix.

4. **The mud frequency: 200–400Hz**
This range is where most mixing problems live. Too much 200–400Hz = boxy, muffled, indistinct. Sources of mud: kick body, bass harmonics, pad lower mids, reverb tails on the send. The fix: identify what's generating the mud (solo each element), cut 3–5dB with a medium-wide Q at the offending frequency. A 3dB cut at 300Hz on every pad element will often immediately open up a muddy mix.

5. **EQ order in the effects chain**
EQ before compression: shapes the tone first, then controls dynamics. The compressor responds to the EQ'd signal. EQ after compression: can undo any tonal changes the compressor introduced. Common approach: HP filter before the compressor (remove low end so the compressor doesn't react to sub rumble), then a second EQ after for tonal shaping. In practice: on drums, always HP before the compressor. On pads, one EQ is usually enough.

6. **The decision tree**
Does the mix sound muddy and indistinct? → High-pass every non-bass element at 120–300Hz.
Does the kick sound boxy? → Cut 250Hz on the kick.
Does the sub bass feel lost in the mix? → High-pass everything non-bass harder, and check that the sub is truly mono.
Does a pad sound dull? → Try cutting 300Hz before reaching for a high shelf boost.
Does a hi-hat sound harsh? → Cut 5–8kHz with a narrow Q. Don't reach for a low-pass that will kill the shimmer.
Should you boost anything? → Only if something specific is missing. Boost with wide Q, cut with narrow Q.

Practice exercise: "On your kettama project, open EQ Eight on the chord pad track. Enable the frequency spectrum view. High-pass at 130Hz. Now add a bell cut at 300Hz, Q=2, amount -3dB. Toggle the entire EQ on/off. What changes in the mix?"

Key takeaway: "Every element needs a frequency home. High-pass everything that doesn't own the low end. Cut mud at 200–400Hz. Cutting is mixing; boosting is colouring."

---

**Deep dive — `signal-flow.json`:**

Title: "Signal Flow — Why Order Matters"
Subtitle: "A sound travels through your chain left to right. Putting things in the wrong order changes the result fundamentally."

Sections:

1. **What signal flow means**
Every plugin processes the signal and passes it to the next. The output of plugin 1 becomes the input of plugin 2. The order is non-trivial — compression before EQ sounds different from EQ before compression. Distortion before reverb sounds completely different from reverb before distortion. Understanding signal flow means you can predict what a chain will sound like before you hear it.

2. **The standard Ableton pad chain (and why)**
Serum → EQ Eight (HP 130Hz) → Saturator (10% soft clip) → Compressor (light, slow attack) → [send to reverb return] → [send to delay return].
Why this order: EQ first removes frequencies Serum generated that you don't want before anything else processes them. Saturator comes before compression — if compression came first, it would control the dynamics before saturation adds harmonics to them (saturation sounds different on a compressed vs uncompressed signal). Compression last (on the dry signal) catches any peaks. Reverb and delay always come after — you want to process the dry sound, then add the wet ambience.

3. **The standard Ableton sub bass chain**
Serum → EQ Eight (HP 40Hz, optional LP 200Hz) → Saturator (15%, Soft Clip, 40% mix) → Compressor (sidechain from kick) → Utility (Width = 0%, mono).
Why this order: HP removes rumble below 40Hz (even a sub bass has sub-sub garbage below its fundamental). Saturator before sidechain compression means the compressor responds to the saturated (harmonically enriched) signal — the sidechain duck feels more natural. Utility at the very end ensures mono after all processing.

4. **Distortion before vs after filter**
Distortion after filter: the filter shapes the tone first, then distortion adds harmonics to whatever frequencies got through. Result: controlled character — the distortion adds grit to a specific tonal range. Distortion before filter: distortion runs on the full frequency range, then the filter cuts some of it. Result: more raw, less controlled — the filter cleans up the distortion. For a Reese bass: distortion → filter gives controlled growl. Filter → distortion gives wilder, more aggressive sound.

5. **Common signal flow mistakes**
Reverb on the dry track then EQ to cut the reverb frequencies → wrong. You're EQ-ing the dry + wet summed signal. Better: EQ on the reverb send's return track only. Compression after reverb → you're compressing the reverb tail, which pumps with every note. Usually wrong (unless intentional). Put compression before the send. Saturator after sidechain compression → the saturation's harmonics don't get the sidechain treatment. If you want the sidechain to affect the whole signal including saturation harmonics, put saturation before the compressor.

6. **The mental model: ask "what is each plugin responding to?"**
If plugin 2 is compression: it responds to the level of whatever comes before it. If you have EQ before compression, the compressor hears the EQ'd signal. If you have saturation before compression, the compressor hears the saturated signal. Always ask: do I want this plugin to respond to the pre-processed or post-processed signal?

Practice exercise: "Take a pad track in your project. Try two chains: (A) Saturator → EQ Eight → Compressor. (B) EQ Eight → Compressor → Saturator. Listen to both. The saturation is doing different things in each. Describe what's different."

Key takeaway: "Order is not arbitrary. Each plugin responds to what came before it. EQ → Compress → Saturate is the standard pad chain. Sends come after the dry chain."

**Cheatsheet — `saturation.json`:** When to reach for Saturator in Ableton: sub bass for translation, pads for warmth, bus for glue. Steps for each use case. Tags: saturation, distortion, warmth, harmonics, translation.

---

**Deep dive — `gain-staging.json`** *(new — fills the gap between knowing effects and using them correctly):*

Title: "Gain Staging — Setting Levels Before You Touch a Plugin"
Subtitle: "The invisible discipline that separates a mix that translates everywhere from one that fights itself."

**Files to add:**
- `src/content/theory/deep-dives/gain-staging.json`
- `src/content/cheatsheet/gain-staging.json`

Sections:

1. **What gain staging is and why it matters**
Gain staging is the discipline of setting the correct signal level at every stage in your signal chain before adding any processing. Each plugin in your chain has a "sweet spot" — a level range it was designed to receive. Feed it too hot (too loud) and it either clips or behaves aggressively in ways you didn't ask for. Feed it too quiet and noise floor becomes audible, or the plugin's processing (especially compressors and saturators) doesn't engage properly. Gain staging is not about making things loud — it's about making things clean and controlled so that every plugin down the chain receives a predictable, manageable signal. Most beginner mixes sound squashed, muddy, or distorted not because the mixing is wrong but because the levels coming into each plugin are wrong. Fix the levels first; the mix falls into place.

2. **The target: -18dBFS average, peaks no higher than -6dBFS**
These numbers represent the digital equivalent of the "0VU" level on an analogue console — the sweet spot where most analogue-modelled plugins were designed to receive signal. At -18dBFS average (measured with a VU meter or by watching your RMS level): the signal has headroom before clipping, the compressor has room to react, the saturator adds warmth without distortion you didn't ask for. Peaks hitting -6dBFS means you have 6dB of headroom before 0dBFS — enough to absorb transients without any single peak clipping. By contrast, a signal averaging -6dBFS with peaks hitting 0dBFS will clip every plugin in its chain, and the mix bus will be fighting to contain levels the whole time.

3. **How to check gain at each stage in Ableton**
Ableton's meters show peak levels by default (the momentary highest value). For gain staging you want to see the average level (roughly what the meter holds most of the time). Method A — the "pre-fader listen" technique: right-click a track's meter and it shows dB values. Solo the track. Watch the sustained (non-peak) meter reading while audio plays. It should average -18 to -12dBFS for individual tracks. Method B — use a gain device: add Ableton's Utility device before your first plugin. Adjust the Gain knob until the signal averages -18dBFS going into the chain. Method C — zoom the arrangement view and look at the audio waveforms: if every waveform is maxing out the track height, the level is too hot before it even hits a plugin. Reduce the clip gain (right-click the clip → Clip Gain).

4. **Gain staging a full chain — the workflow**
Start at the source and work downstream:

Step 1 — Set the synthesiser/sample level. In Serum: the Master volume knob. Target: the pad leaving Serum at around -12 to -6dBFS peak (not 0, not -24). This gives the chain something to work with.

Step 2 — Check into the first plugin (usually EQ). Solo the track, let it play, watch the input meter on the EQ Eight. If the signal is hitting above -6dBFS peak regularly: reduce the input. EQ Eight has no input gain knob, so use a Utility device before it with gain trimmed down.

Step 3 — After EQ, check into Saturator. The Saturator should receive -12 to -6dBFS peak. Saturator's Drive knob amplifies the input — if the signal arrives too hot, even low Drive settings will overdrive. At correct input levels, Drive 10–15% gives warmth without aggression.

Step 4 — After Saturator (which may have raised the level slightly due to makeup gain), check into the compressor. The compressor responds to level — its threshold is set in dBFS. If the input arrives much hotter than expected, the compressor's threshold setting becomes inaccurate (you set -18dBFS threshold expecting a signal that peaks at -12, then you feed it a signal peaking at -3 and suddenly the compressor is working much harder than intended).

Step 5 — After the compressor, use makeup gain to restore lost level. The post-comp signal should leave at roughly the same level it arrived at before compression. Check: before comp = -12dBFS average, after comp + makeup = -12dBFS average. The compressor shaped the dynamics; the gain structure is preserved.

Step 6 — Check the group/bus level. After all tracks in a group feed into the group channel, the group fader should be keeping the summed level in check. Groups often need to be pulled down 3–6dB from unity (0dB) if they contain many tracks. Watch the group channel meter — it should average -12 to -6dBFS before hitting the master.

Step 7 — Master channel level before the limiter: -6dBFS or lower on peaks. The limiter is a safety net, not a gain tool. If the master is averaging -3dBFS before the limiter, the limiter is working too hard and everything will sound crushed.

5. **Gain staging vs fader mixing — the difference**
Many beginners adjust the loudness of elements with the channel fader only. The fader sets the output volume — it doesn't change the level going into plugins on that track. If a pad track has its fader at -6dB but Serum is outputting at 0dBFS, every plugin on that pad chain is still receiving a 0dBFS signal and is working too hard. The fader reduction only happens after the plugins. Fix: trim at the source (Serum's Master knob or clip gain), not at the fader. Trim the input; use the fader for relative balance between elements.

6. **Why clipping before compression sounds bad**
A signal that clips (goes above 0dBFS, or distorts in an uncontrolled way) before reaching a compressor means the compressor is now compressing a distorted signal. The compression dynamics are being applied to clipping artifacts rather than to the original sound. The result: harsh, fatiguing, distorted compression that no amount of makeup gain or ratio adjustment will fix. The fix is always upstream — reduce the level before the plugin, not at the plugin.

7. **The gain staging checklist — run before starting every session:**
- [ ] Solo kick. Does it peak above -6dBFS? If yes: reduce clip gain or reduce in drum rack.
- [ ] Solo sub bass. Does it average below -12dBFS? It should — sub bass is powerful but should leave headroom for the pad and drums to stack above it.
- [ ] Check the DRUMS group meter. Should peak around -6dBFS before the Glue Compressor.
- [ ] Check the master before the Limiter. Should average -12dBFS or lower. Peaks at -6dBFS or lower.
- [ ] Is the Limiter gain reduction meter constantly showing -3dB or more? If yes: something upstream is too loud — pull down the group faders or instrument levels, not just the limiter ceiling.
- [ ] Play the full mix. If anything feels instantly too loud or too compressed, solo it and check its level before its first plugin.

8. **The decision tree**
Does the mix sound overcompressed even though your compressor settings seem reasonable? → Check the level going into the compressor — it's probably arriving too hot.
Does the Saturator sound harsh at low drive settings? → The signal arriving at the Saturator is already too loud. Add a Utility before it and trim down.
Does the limiter constantly clamp on the master? → The bus is too loud before the limiter — reduce group faders or individual instrument levels upstream.
Does the sub bass feel louder than everything else in the mix even though the fader is at -6dB? → The Serum master output on the sub bass patch is too high. Reduce it in Serum, then re-balance the fader.
Does EQ boosting seem to make things worse rather than better? → You're boosting an already hot signal. Stage the gain first, then apply boosts.
Does the mix feel surprisingly quiet even at high fader levels? → Your individual signals may be too quiet entering the chain, so makeup gain is working through each plugin trying to compensate. Trim at the source.

Practice exercise: "Open your Kettama study project. Without changing anything, solo the chord pad track. Watch the EQ Eight's input meter as the track plays. Write down the average dB reading and the peak dB reading. Now look at the Saturator's input — if Ableton shows it: write it down. Is the pad entering the chain at a clean level? If it's hitting above -6dBFS peak: use a Utility device before the EQ Eight to trim it to -12dBFS average, then re-listen to the pad. What changed in the sound of the Saturator and the compressor after trimming the input?"

Key takeaway: "Gain staging is not about loudness — it's about giving every plugin a signal it can work with. Target -18dBFS average, -6dBFS peaks going into each plugin. Fix levels upstream, not at the fader."

**`linked_rep_id`:** `rep-11-VI-III-i-loop-bbmin` — run the gain staging checklist on this rep's project as the practice exercise.

**Cheatsheet — `gain-staging.json`:** Quick checklist for gain staging a session. Steps: check Serum output level, add Utility to trim, check each plugin input, check group meters, check master before limiter. Tags: gain staging, levels, headroom, clipping, metering.

---

**Step: Verify + commit**
```bash
git commit -m "feat: effects deep dives — saturation, EQ strategy, signal flow, gain staging"
```

---

## Phase 2G: Arrangement Theory

### Task 28: Arrangement deep dives — Structure, Energy, and Transitions

**Design principle:** Arrangement is about managing the listener's attention over time. Every section has a psychological job. Every transition is a tool. These deep dives teach arrangement as decision-making, not just "here's what sections go in a track."

**Files:**
- Create: `src/content/theory/deep-dives/arrangement-structure.json`
- Create: `src/content/theory/deep-dives/arrangement-transitions.json`
- Create: `src/content/theory/deep-dives/arrangement-energy-curve.json`
- Create: `src/content/cheatsheet/arrangement-sections.json`

---

**Deep dive — `arrangement-structure.json`:**

Title: "Track Structure — What Every Section Is Actually Doing"
Subtitle: "Each section has a psychological job. If you don't know the job, you can't do it right."

Sections:

1. **The psychological contract**
When a listener presses play, they enter an implicit contract with you: you will take them somewhere. They don't know where, but they expect movement, tension, release, and return. Every section of your track is either building toward the drop, being the drop, or recovering from it. If a section doesn't have a clear job, it's filler and the listener loses interest. The question to ask about every section you write: "what is this section doing to the listener?"

2. **Intro (bars 1–16 typically)**
Job: establish tempo and groove. Give the DJ something to mix into. Let the listener orient themselves. What it contains: drums only, or drums + bass, or just atmosphere. What it does NOT contain: all elements, the chords, anything that belongs in the drop. Why: if you reveal everything immediately, there's nowhere to go. The intro is the on-ramp. It has to feel incomplete — that incompleteness is what creates the pull toward the drop. Common UK garage intro length: 8–16 bars. 16 bars if you want clear DJ mix room.

3. **Build (bars 17–32 typically)**
Job: create tension. Raise the listener's expectation. Build energy toward the drop. Tools: filter sweep (low-pass opening up toward the drop), layer in elements one by one (bass enters bar 17, hi-hats layer in bar 21, chord stab teased bar 29), rising noise/synth sweep, increase reverb send level (creates a sense of expanding space). What makes a good build: it should feel like it's about to explode. If the build doesn't create physical anticipation, the drop won't feel like a release. A build that does nothing is worse than no build.

4. **The drop moment**
Job: release all the tension the build created. The single most important moment in the track. Tools: 1-beat silence before the drop (removes all sound for one beat — silence amplifies what follows), full element reveal at bar 1 of the drop, sidechain pump immediately apparent. Why the 1-beat silence works: it's a complete sonic reset. The brain experiences a brief moment of "where did the music go?" — then it hits. The contrast of silence against full energy makes the drop feel larger than it actually is. This is the flat smash equivalent: you use it at the exact moment the opponent (listener) expects the ball to keep coming.

5. **Drop 1 (bars 33–64 typically)**
Job: deliver on the build's promise. Make people dance, feel, move. All elements present: drums, sub bass, chord pads, atmosphere, sidechain pumping. Length: 16–32 bars. The drop should feel like it could go on forever but also that something is going to change. Don't change anything during the drop — let it breathe. The listeners are experiencing the full picture you built toward.

6. **Breakdown (bars 65–80 typically)**
Job: create intimacy. Remove elements to expose the harmony. Let the listener breathe. Give the next drop something to build contrast against. What to remove: kick, sub bass, hats (sometimes). What stays: chord pads, atmosphere, reverb (increase reverb send level here — the space expands when the dense elements leave). What happens psychologically: the listener suddenly hears the chord progression clearly for perhaps the first time. The bass-implied harmony is exposed. This is where people go "oh, I hear what this track is actually about." Increase reverb in the breakdown — more wet = more emotional.

7. **Rebuild (bars 81–88 typically)**
Job: reintroduce elements to rebuild tension before drop 2. Method: 2-bar increments — hat bar 81, kick bar 83, bass bar 85, everything bar 87. Each entry restores one component of the energy. The listener knows the drop is coming (they've heard drop 1) — the anticipation is even stronger because now they know exactly how good it's going to feel.

8. **Drop 2 (bars 89–120 typically)**
Job: deliver drop with accumulated weight. Often identical to drop 1, but feels bigger because of the context around it. Optional: add a subtle new element (a stab, a counter-melody, a new hat pattern) — not to change the drop, just to reward attentive listeners with something new. Length: typically longer than drop 1 (32 bars vs 16) because this is the peak of the track.

9. **Outro (bars 121–128)**
Job: give the DJ something to mix out of. Reduce tension. Strip elements back one by one (reverse of the rebuild). End on just atmosphere or a fade. Don't just stop — the outro is as important as the intro for the DJ context.

10. **Decision tree**
Does the build feel like it goes nowhere? → You're not creating tension. Add a filter sweep or layer elements incrementally. The build needs an arc.
Does the drop feel like it didn't land? → Check: is there a 1-beat silence before it? Is the build long enough? Did you reveal drop elements too early in the build?
Does the track feel too long? → Typical issue is the drop is too long or the rebuild is too slow. Cut bars, not sections.
Does the breakdown feel flat? → You didn't increase the reverb. Remove more elements — breakdowns work by contrast with the drop, so the more you strip back, the bigger the next drop feels.
Does drop 2 feel anticlimactic vs drop 1? → It shouldn't — but if it does, you need a longer rebuild, or a surprise element at the start of drop 2.

Practice exercise: "Load Kettama — It Gets Better. Listen to the whole track. Write down bar numbers for: where the intro ends, where the build starts and ends, where drop 1 starts, where the breakdown starts, where drop 2 starts, where the outro starts. Compare your map to the structure in the track library entry."

Key takeaway: "Every section has a job. Intro = orient. Build = tension. Drop = release. Breakdown = expose. Rebuild = re-tension. Drop 2 = peak. Outro = exit. If you don't know what a section is doing, it's doing nothing."

---

**Deep dive — `arrangement-transitions.json`:`**

Title: "Transitions — The Moments Between Sections"
Subtitle: "How you get from A to B is as important as A and B."

Sections:

1. **Why transitions matter**
A jarring transition breaks immersion. A smooth transition feels inevitable. A great transition creates a moment — the listener feels something specifically because of the way two sections connected. Transitions are the punctuation of arrangement. They tell the listener: something just ended, something is beginning.

2. **The 1-beat silence**
Already covered in the structure deep dive but deserves its own treatment here. The silence is a transition technique, not just a drop trick. It can be used: before the drop (most common), between the breakdown and rebuild, at the very end of an intro. Technically: mute every track for exactly one beat (at 140 BPM, one beat = 429ms). In Ableton: draw an automation clip that mutes the master track, or use a Macro in a Rack that controls volume of all elements simultaneously.

3. **Filter sweep into the drop**
A rising low-pass filter on a white noise or synth element that sweeps from ~200Hz to fully open over the last 4–8 bars of the build. This creates a sense of energy accumulating and releasing. In Ableton: add a white noise audio track, add Auto Filter, automate the cutoff from closed to open across bars 29–32. The reverse (high-pass sweep: filter starts fully open then gradually closes) works for outro transitions or going into a breakdown.

4. **Drum fill into section change**
In the last bar before a new section, modify the drum pattern: add extra hat hits (a 16th-note roll in the last beat), remove the kick entirely (creating a "space" that the drop fills), or use a specific snare pattern (4 snare hits in the last beat = classic "drum fill"). This signals to the listener: something is about to change. Without a drum fill, section changes can feel abrupt.

5. **Reverb throw**
At the very end of a section, automate the reverb send to maximum for 1–2 beats, then cut everything to silence. The last sound you hear is disappearing into a cavernous reverb. This is the "reverb throw" — a transition technique that makes section endings feel cinematic rather than sudden. Works especially well going into a breakdown or the final drop.

6. **Energy through layering**
Instead of a filter sweep, build energy by layering elements in: bar 1 of the build = bass only, bar 5 = bass + closed hats, bar 9 = bass + hats + clap, bar 13 = all drums + bass, bar 15 = all drums + bass + pad stab (teased), bar 17 = full drop. Each new entry is a micro-transition that maintains tension across 16 bars.

7. **The "tension and release" rule for transitions**
Every transition creates either tension or release. Going into a build = tension. Going into a drop = release. Going into a breakdown = release (from the drop's intensity). Going into drop 2 = tension again. Your transitions should always be in service of the tension/release arc. A smooth, swelling transition into a drop = good tension. A jarring cut into a drop = can work if intentional, but usually breaks immersion.

Practice exercise: "In your kettama-study project, find the moment before drop 1. Add a 1-beat silence (mute all tracks for beat 4 of the last bar before the drop). Loop bars 30–35 to hear the silence. Now add a white noise sweep that climbs from 200Hz to open over bars 29–32. Does the drop feel bigger?"

Key takeaway: "Transitions are tools: silence, filter sweep, reverb throw, drum fill, layering. Each has a specific effect. Use them intentionally, not randomly."

---

**Deep dive — `arrangement-energy-curve.json`:**

Title: "The Energy Curve — Mapping Intensity Over Time"
Subtitle: "A finished track has a shape. Understanding that shape lets you design it on purpose."

Sections:

1. **What the energy curve is**
If you drew a graph of your track's intensity over time (X = time, Y = energy level 0–10), you'd see a curve. Intro: 3/10. Build climbing to 7/10. Drop: 9/10. Breakdown: 4/10. Rebuild climbing to 8/10. Drop 2: 10/10. Outro descending to 2/10. This is the energy curve. A track without a designed energy curve has a flat line at 5/10 — it goes nowhere and does nothing to the listener's nervous system.

2. **What creates energy level (specific elements)**
Low energy: sparse drums, no sub bass, long reverb, minimal elements, slow tempo feel. High energy: 4-on-floor kick, pumping sidechain, full frequency range, sub bass hitting hard, tight reverb, all elements present. Transition: elements entering or leaving, filter sweeping, reverb building or cutting. The specific UK garage energy dial: kick density (2-step vs 4-on-floor), sidechain presence (pump vs breathe), sub bass level, hat density.

3. **Designing against the typical curve**
The curve above is conventional. You can subvert it intentionally: put the most intense moment at bar 48 instead of bar 89 (subverts expectation). Start at 7/10 instead of 3/10 (drops you straight in). Never fully release (maintain tension throughout — a different emotional effect). These are advanced choices. Know the convention first, then break it on purpose.

4. **The practical exercise: map before you build**
Before opening Ableton, write the energy curve on paper: "Bars 1–8: drums only at 3/10. Bars 9–16: bass enters, 5/10. Bars 17–24: filter sweep climbing, 6–7/10. Bar 24 beat 4: silence. Bar 25: full drop, 9/10..." etc. Building against a map is always faster than discovering the structure while you're building it.

5. **Common energy curve mistakes**
The flat drop: everything enters at the drop but nothing changes for 32 bars — 9/10 all the way through, which exhausts the listener. Fix: introduce subtle variations at 8-bar intervals within the drop (a new hat accent at bar 8, a brief filter movement at bar 16, etc.). The too-slow build: the build is 32 bars of nothing happening. Fix: layer elements every 4 bars minimum. The anticlimactic breakdown: breakdown is at 4/10 but drop 1 was only at 7/10 — there's not enough contrast. Fix: drop 1 must be your highest energy before drop 2. The early reveal: you play the chord pads in the intro. Now the drop has nothing new. Fix: save your highest-impact elements for the drop.

Practice exercise: "Draw the energy curve of your kettama-study project as it currently exists. Mark each section with a 0–10 energy rating. Then draw the ideal curve — where would you change sections to improve the arc?"

Key takeaway: "Your track has a shape. Design that shape on paper before building it. The energy curve is your map."

---

**Cheatsheet — `arrangement-sections.json`:** Quick reference for section jobs, typical bar counts, what to include/exclude in each. Tags: arrangement, structure, intro, drop, breakdown.

**Step: Verify + commit**
```bash
git commit -m "feat: arrangement deep dives — structure, transitions, energy curve"
```

---

## Phase 2H: Connect Content to Reps

### Task 29: "Practice this" — wire content to reps across the whole app

**Goal:** Every piece of content (cheatsheet entry, theory card, deep dive) has a visible, clickable path to the rep where you experience that concept. Content is reference. The Builder is where you learn. This task makes that connection explicit in the UI.

**This is the glue task — run it after Tasks 11-19 are content-complete.**

**Files:**
- Modify: `src/content/theory/scales.json`, `chords.json`, `rhythms.json` — add `linked_rep_ids[]`
- Modify: `src/pages/Theory.jsx` — show "Practice" pill on each card
- Modify: `src/pages/Ableton.jsx` — show "Try it in a build →" button on each cheatsheet entry
- Modify: `src/pages/Theory.jsx` deep dive article view — show "Practice this now" button after the exercise block
- Modify: `src/components/BuildStep.jsx` — show theory concept tags on steps that teach a named concept (from `teaches[]`)

---

**Step 1: Update theory card JSON — add `linked_rep_ids[]`**

Add to each existing theory card (scales, chords, rhythms) a `linked_rep_ids` array naming which Builder reps use that concept. Examples:

```json
// In scales entry for "Bb Minor (Natural)"
"linked_rep_ids": ["rep-11-VI-III-i-loop-bbmin", "spinoff-kettama-bbmin-full"]

// In chords entry for "Minor 7 (m7)"
"linked_rep_ids": ["rep-11-VI-III-i-loop-bbmin", "rep-12-VI-III-i-loop-fmin"]

// In rhythms entry for "4-on-floor"
"linked_rep_ids": ["rep-01-four-on-floor-emin", "rep-06-mini-track-emin"]
```

**Step 2: Theory page — "Practice" pill on cards**

On each scale/chord/rhythm card, below the existing content, add a row of small pill buttons:
```
→ Practice in: [Four on Floor E min] [Mini-track E min]
```
Each pill navigates to `/?tab=builder&build=rep-01-four-on-floor-emin` (or sets state in Builder directly via React Router state). Clicking it opens the Builder pre-loaded to that build.

**Step 3: Deep dive article — "Practice this now" link**

After the `practice_exercise` block in every deep dive article, render a prominent CTA:
```
[Practice this in the Builder →]
```
Clicking it navigates to the Builder and opens the `linked_rep_id` build.

**Step 4: Cheatsheet entry — "Try it in a build" link**

On each cheatsheet entry card (in the Ableton page), add a small "Try it →" link at the bottom that opens the Builder at the `practice_rep_id`. If the entry only has a `practice_hint`, show the hint text as an inline tip instead.

**Step 5: BuildStep — concept tags**

Add a `teaches[]` array to the guided build step schema. When a step has `teaches`, render small grey tags below the "Why this works" section:
```
Concepts: sidechain compression  phrygian tension  VI→III→i
```
These are not links — they're labels. They help the user see what they're learning while doing it.

**Step 6: TrackDetail — from dead end to entry point**

The TrackDetail pages (Library → click a track) are currently one-way reference: the user reads the breakdown and has nowhere to go. After Phase 2 adds deep dives and reps that all reference these tracks, every TrackDetail page becomes the natural landing point for content discovery. This step wires that up.

**Step 6a: Update track JSON schema — add `related_content` block**

Each track JSON (in `src/content/tracks/`) gets a new `related_content` field:

```json
"related_content": {
  "deep_dive_ids": ["vi-iii-i-loop", "chord-voicing", "arrangement-structure"],
  "rep_ids": ["rep-11-VI-III-i-loop-bbmin", "rep-12-VI-III-i-loop-fmin"],
  "spinoff_ids": ["spinoff-kettama-bbmin-full", "spinoff-04-kettama-fmin-mid"]
}
```

Fill these in for all 5 tracks:

| Track | deep_dive_ids | rep_ids | spinoff_ids |
|---|---|---|---|
| kettama-it-gets-better | vi-iii-i-loop, chord-voicing, arrangement-structure, sound-design-emotion | rep-11, rep-12, rep-serum-chord-pad | spinoff-kettama-bbmin-full, spinoff-04-kettama-fmin-mid |
| mph-raw | phrygian-tension, transposing-concepts | rep-03, rep-04, rep-05, rep-serum-sub-bass | spinoff-01-mph-dmin-entry |
| ic-slow-burner | vi-iii-i-loop, chord-voicing, effects-compression | rep-08, rep-09 (bVI lift), rep-serum-chord-pad | spinoff-02-ic-amin-entry, spinoff-03-ic-dmin-mid, spinoff-05-ic-full |
| sammy-virji | arrangement-transitions, effects-reverb-delay | rep-02, rep-07, rep-14 | spinoff-06-sammy-full |
| bl3ss-deeper | bass-implied-harmony, transposing-concepts, effects-eq-strategy | rep-13, rep-14 | spinoff-07-bl3ss-full |

**Step 6b: Update TrackDetail.jsx to show related content sections**

After the existing track breakdown content (chord progression, arrangement, production notes), add three new sections:

**Related Deep Dives** — shows a card row (horizontal scroll on mobile) for each `related_content.deep_dive_ids` entry. Each card shows: deep dive title, subtitle, difficulty badge, read time. Clicking navigates to the Theory page and opens that deep dive article directly (use React Router state or URL param: `/theory?deepdive=vi-iii-i-loop`).

**Practice this sound** — shows a row of Builder rep cards for each `related_content.rep_ids`. Each card shows: rep title, BPM, key, difficulty, estimated time. Clicking opens the Builder with that rep pre-loaded.

**Spinoffs of this track** — shows a row of spinoff cards for each `related_content.spinoff_ids`. Each card shows: spinoff title, spinoff_level badge, key, estimated time. A spinoff card looks slightly different from a rep card — use a purple accent border (border-purple-900) to distinguish it. Clicking opens the Builder with that spinoff.

**Visual design:** These three sections are separated from the main breakdown by a `border-t border-zinc-800 mt-8 pt-8`. Header for each section: `text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3`. Each card in the row is the same compact card style used in BuildSelector but scaled down (no BPM row, just title + time + difficulty badge). The rows are horizontally scrollable on mobile (`flex gap-3 overflow-x-auto pb-2`).

**Step 6c: Add "View in Library →" link to spinoff headers in the Builder**

Currently when you're in the Kettama spinoff, there's no link back to the Kettama track breakdown. Add a small link below the spinoff title in the Builder's build header:

```jsx
{build.source_track_id && (
  <Link
    to={`/library/${build.source_track_id}`}
    className="text-xs font-mono text-zinc-600 hover:text-zinc-400"
  >
    ← Source: {build.source_track_id}
  </Link>
)}
```

This closes the loop: TrackDetail → spinoff in Builder → back to TrackDetail.

**Step 7: Verify + commit**
```bash
npm run dev
# Check: Library → Kettama → Related Deep Dives section shows vi-iii-i-loop, chord-voicing cards
# Check: clicking a deep dive card opens Theory page at that article
# Check: Library → Kettama → Practice this sound → clicking rep-11 opens Builder at that rep
# Check: Library → Kettama → Spinoffs section shows Kettama spinoff card with purple border
# Check: Builder → Kettama spinoff header → "← Source: kettama-it-gets-better" link visible and navigates correctly
git add src/content/tracks/ src/pages/TrackDetail.jsx src/components/BuildStep.jsx src/pages/Builder.jsx src/pages/Theory.jsx src/pages/Ableton.jsx
git commit -m "feat: connect content to reps — practice buttons, track cross-links, TrackDetail entry points"
```

---

## Updated Task Order (complete Phase 2)

1. Task 11 — Theory Deep Dives Part 1 (VI→III→i, phrygian, bass-implied)
2. **Task 22 — Serum V2 UI orientation**
3. **Task 23 — Serum sub bass rep**
4. **Task 24 — Serum chord pad rep**
5. Task 12 — Theory Deep Dives Part 2 (arrangement theory intro, sound design, transposing)
6. **Task 26 — Effects: reverb, delay, compression**
7. **Task 27 — Effects: saturation, EQ strategy, signal flow**
8. **Task 28 — Arrangement: structure, transitions, energy curve**
9. Task 17 — Progress tracking
10. Task 18 — Daily practice
11. Task 13 — Beginner reps 4–7
12. **Task 25 — Serum Reese + stabs + layering**
13. Task 14 — Intermediate reps 8–14
14. Task 15 — Spinoffs 2–4
15. Task 19 — Cheatsheet expansion (30 entries with practice_rep_id)
16. Task 20 — Drum rack downloads
17. Task 16 — Full spinoffs + originals
18. **Task 29 — Connect content to reps (practice buttons everywhere)**
19. Task 21 — CI fix

---

## Complete Phase 2 Learning Outcomes

By the end of Phase 2, the user can:

**Theory:**
- Derive any chord in a minor key from the scale (no memorisation)
- Explain why VI→III→i feels inevitable (common tones)
- Hear phrygian tension and identify it by ear
- Transpose any concept (phrygian bass, chord loop) to any key without help
- Voice a maj7, minor, and major chord correctly in a piano roll (correct register, spread, 7th on top)
- Reverse-engineer a chord voicing from a reference track by ear — find the top note and work downward

**Serum V2:**
- Navigate the full UI with confidence
- Build a sub bass from Init Preset
- Build a chord pad from Init Preset
- Build a Reese bass from Init Preset
- Build a stab patch
- Layer two Serum instances in an Instrument Rack

**Effects (when/why):**
- Reverb: knows when to use large hall vs small room, always uses sends, always HP the return
- Delay: knows when delay serves better than reverb, can set up tempo-synced delay
- Compression: knows attack speed affects punch, can set up sidechain, can apply bus glue
- Saturation: knows why sub bass needs it for small speaker translation, uses it for pad warmth
- EQ: high-passes everything that doesn't own the low end, cuts mud at 200–400Hz
- Gain staging: sets levels correctly before plugins, targets -18dBFS average into each stage, doesn't confuse fader position with signal level, can run the gain staging checklist from memory

**Arrangement:**
- Can describe the psychological job of each section
- Uses transitions intentionally (silence, filter sweep, reverb throw, drum fill)
- Draws an energy curve before building
- Can map the structure of any reference track by ear

**Builds:**
- 25/25 guided builds available
- 3 beginner reps completed (reps available for all 7)
- Full Kettama spinoff guide with Serum patch detail

**The loop (how content and reps connect):**
- Reads a theory card → clicks "Practice in [rep name]" → does it in Ableton
- Opens a cheatsheet entry → clicks "Try it →" → lands in the rep where that tool is used
- Finishes a deep dive article → clicks "Practice this now" → opens the linked rep
- Does a rep → sees `teaches[]` concept tags → knows which theory cards to read for context
- Experiences every concept through at least 3 repetitions in different keys before Phase 2 ends

---

# Phase 3: Production Craft — Arrangement, Sampling, and Depth

> **Goal:** Turn a producer who can make a loop into one who can make a track. Phase 3 teaches the craft layer that Phase 2 assumed — how to build sections, how to source samples, how to programme drums with feel, and genre-specific techniques for UK garage, bassline, and house.

---

## Phase 3A: Arrangement Section Reps

Each rep in this section is a single section of a track, isolated and taught in depth. The user builds only that section — no full track context. The goal is mastery of each structural moment before combining them.

### Task 30: Intro construction rep

**File:** `src/content/guided-builds/reps/rep-15-intro-construction.json`

**ID:** `rep-15-intro-construction`  
**Title:** "Building a Tension Intro"  
**Difficulty:** beginner  
**BPM:** 132  
**Key:** E minor  
**estimated_time_mins:** 25

**What it teaches:** How to build a 16-bar intro that creates genuine tension and makes the drop feel earned. Techniques: drums-only opening (not dead silence, not full groove — something in between), element stacking over 8-bar phrases, the moment each element enters and what it psychologically signals, how volume and filtering signal "almost there."

**Steps (~8):**
1. Concept: the intro has one job — make the listener want the drop. 16 bars at 132 BPM = 29 seconds. That is a long time to hold attention with almost nothing. Write down what you'll add and when before programming.
2. Bars 1–4: Kick only. No clap, no hat. Just the kick landing on every beat at velocity 90. Nothing else. Loop it. Does it feel like something is coming? It should.
3. Bars 5–8: Add hat. Sparse — 4 per bar, off-beats, velocity 55. The hat narrows the space without filling it.
4. Bars 9–12: Add clap on beat 3 only (one per bar). The clap arriving signals "the groove is assembling."
5. Bars 13–15: Add sub bass at -8dB (quieter than drop level). The listener hears the bass frequency but doesn't get the full weight of it yet. If using a filter sweep: automate a low-pass on the bass from 40Hz to fully open over these 4 bars.
6. Bar 16 beat 4: 1-beat silence. Everything cuts. Then the drop hits bar 17 beat 1.
7. Variation: experiment with a white noise riser from Splice entering at bar 14 and building to bar 16. Search Splice: 'riser noise sweep 132 BPM'. Does the riser add tension or feel clichéd? Your call.
8. Compare your intro against 3 reference tracks (Kettama at 0:00, IC Slow Burner at 0:00, MPH Raw at 0:00). What does each do in their intro? Which techniques do they share? Which does yours most resemble?

**linked_rep_ids:** `rep-06-mini-track-emin` (first track with structure), `spinoff-05-ic-full` (the 16-bar long intro)

---

### Task 31: Build-up mechanics rep

**File:** `src/content/guided-builds/reps/rep-16-buildup-mechanics.json`

**ID:** `rep-16-buildup-mechanics`  
**Title:** "The Build-Up — 8 Bars to the Drop"  
**Difficulty:** intermediate  
**BPM:** 138  
**Key:** G minor  
**estimated_time_mins:** 30

**What it teaches:** The 8-bar build-up — the section that creates maximum tension before the drop. Techniques: filter automation (LP sweep up over 8 bars), white noise riser, velocity crescendo on hats, removing the kick for 4 bars then reintroducing it, the 1-beat or 2-beat silence technique. Every technique is isolated and then combined.

**Steps (~10):**
1. Start with a complete 4-bar loop (drums + bass + pad). This is what the build is leading to — the drop. Before building the build-up, know exactly what the drop sounds like.
2. The filter sweep: add AutoFilter to the PAD track. Set LP cutoff to 200Hz (nearly closed). In Arrangement view, automate the LP cutoff from 200Hz to fully open over 8 bars. Listen. The pad "opens up" over 8 bars — this is the most common build-up technique in electronic music.
3. The kick removal: in bars 1–4 of the build-up, remove the kick. Add it back at bar 5. The absence of the kick for 4 bars makes its return feel like a punch. Program this as automation (kick track volume from 0 to full at bar 5).
4. Hat velocity crescendo: in the build-up MIDI clip for hats, programme velocities that increase every 2 bars: bars 1–2 at 55, bars 3–4 at 70, bars 5–6 at 85, bars 7–8 at 100. The hats seem to "rush" toward the drop.
5. The riser: search Splice 'riser sweep 8 bar'. Find one that lasts 8 bars. Import to an audio track. Line it up so it ends exactly on the drop's beat 1. Set volume -6dB so it supports rather than dominates.
6. The clap roll: in bar 8 of the build-up, programme a clap or snare roll (4th bar of kicks being absent): 16th note claps in bar 8, velocity increasing from 70 to 110 across the bar. This is the last tension peak before the drop.
7. The 1-beat silence: beat 4 of bar 8 — cut everything. Silence for 1 beat. Drop hits beat 1 of bar 9.
8. Now combine all techniques: filter sweep + hat crescendo + riser + clap roll + 1-beat silence. Loop the build-up into the drop 4 times. Does the drop feel earned? Adjust what's too much.
9. Comparison: which techniques are essential? Mute each one individually. Which removal kills the tension most? Usually it's the filter sweep or the silence — the others support but these are structural.
10. Export the build-up + drop (16 bars). Save the build-up MIDI clip and automation as a template you can drag into any project.

**Key insight:** A build-up is not about adding more elements — it's about managing anticipation. The techniques above all create the same thing: the feeling of something approaching. Any one of them alone can build tension. All of them together can overwhelm. Find the right combination for your track's density.

---

### Task 32: Drop entry mechanics rep

**File:** `src/content/guided-builds/reps/rep-17-drop-entry.json`

**ID:** `rep-17-drop-entry`  
**Title:** "Drop Entry — Making the Moment Land"  
**Difficulty:** intermediate  
**BPM:** 140  
**Key:** Bb minor  
**estimated_time_mins:** 25

**What it teaches:** The drop is a single moment, but how it's engineered determines whether it hits or fizzles. This rep isolates the 4 bars before and 4 bars after the drop and teaches: the 1-beat silence, velocity peaks on drop beat 1, how the bass and kick landing together creates impact, reverb pre-delay as a sharpening tool, and how the build-up's last element should contrast maximally with the drop's first element.

**Steps (~8):**
1. Start with your build-up ending (from rep-16 if available, or any 4-bar tension section). Know what the last thing the listener hears before silence is.
2. The silence duration: try 1 beat (standard), 2 beats (more dramatic), half a beat (barely noticeable), no silence (full flow). Listen to each version 10 times. Record which felt most impactful at which point in your listening. The correct duration depends on the listener's anticipation level going in.
3. Beat 1 velocity spike: on the drop's beat 1, set kick velocity to maximum (127). Set bass note velocity to 95. Set pad velocity to 90. These are all higher than their normal values. The contrast from silence to these three elements hitting simultaneously at high velocity is the "hit."
4. Pad reverb pre-delay: set the reverb return's pre-delay to 20ms. This means the reverb tail starts 20ms after the note — leaving the initial attack of the pad completely dry and clear. On the drop beat 1, the pad hits hard before the room blooms around it. Try pre-delay 0ms vs 20ms vs 40ms — hear how the attack sharpness changes.
5. Kick and bass alignment: play just kick and bass through the drop entry. The kick transient and the bass fundamental must hit on exactly the same millisecond. Even a few ms of offset weakens the impact. Zoom in in the Arrangement view and verify alignment.
6. The EQ hi-cut removal: a common technique — during the build-up, an EQ on the master cuts above 8kHz (muffles the sound). At the drop beat 1, the EQ cut disappears and the full frequency range returns. This creates a "lid coming off" sensation. Try it: automate an EQ Eight on the master, Hi-shelf cut -6dB through the build-up, automation returns to 0dB at drop beat 1.
7. First 4 bars of the drop: do they sustain the impact? The drop hit creates maximum energy — the next 4 bars need to maintain it. If the drop feels like a moment and then deflates, the arrangement after the drop needs work. Check: are all elements (pads, bass, drums) at their correct levels from bar 1 of the drop? The sidechain pump should be audible from the first kick.
8. Export 8 bars: 4 bars of build-up + 4 bars of drop. This is your drop entry template. Label it by BPM and key.

---

### Task 33: Breakdown writing rep

**File:** `src/content/guided-builds/reps/rep-18-breakdown-writing.json`

**ID:** `rep-18-breakdown-writing`  
**Title:** "The Breakdown — Holding Interest Without Rhythm"  
**Difficulty:** intermediate  
**BPM:** 136  
**Key:** F minor  
**estimated_time_mins:** 30

**What it teaches:** The breakdown is the section most producers get wrong — they strip the drums and hope the pads carry it, but the pads alone rarely hold attention. This rep teaches: what to strip vs what to keep, how to use reverb tails as content, how to add new elements ONLY in the breakdown (vocal fragment, filtered melody, texture), and how the breakdown's harmonic exposure should reveal something the drop implied but didn't show.

**Steps (~10):**
1. Start with a full drop loop. The breakdown strips from this. Before programming: decide what the breakdown is emotionally. Is it a dark valley (darker than the drop)? A moment of light (more harmonic exposure)? A breath (nothing dramatic — just space before the next drop)? Each is valid. Your choice shapes the decisions below.
2. Strip the kick: the kick is the first to go in every breakdown. Remove it. Loop 8 bars with everything else. How does the energy feel?
3. Strip the sub bass: remove it too. The low end becomes purely reverb tail from the last bass notes. Does the track feel like it's floating? Good.
4. Decide: what stays? Usually: pads, reverb return, atmosphere. Sometimes: a simplified bass line (ghost bass). Never: the full kit.
5. Reverb as content: in the breakdown, increase the reverb send from -10dB to -6dB (louder). The reverb tail from each pad chord becomes an audible element, not just depth. The chords blur together more. This is intentional — the breakdown is the most harmonic, least rhythmic section.
6. The new element: add one thing that ONLY appears in the breakdown. Options: a vocal fragment from Splice ('vocal sample garage one-shot whisper'), a filtered piano note, a distant melodic ping. Volume at -12dB. This gives the breakdown its own identity — it's not just a stripped drop, it has something new.
7. The re-entry cue: the rebuild must signal clearly that the drop is returning. Options: bass entering 2 bars before the drop at -6dB, a reverse cymbal, the kick entering alone for 1 bar. The listener should feel anticipation returning before the drop does.
8. The 16-bar rule: most breakdowns are 16 bars. Less feels too brief to register. More feels like the track stalled. At 136 BPM, 16 bars = 28 seconds. Test yours: loop the breakdown 3 times. On the third loop, does it feel too long? If so, cut to 12 bars.
9. Export breakdown only (16 bars). Export rebuild + drop 2 entry (8 bars). Listen back to back — does the rebuild feel like a return?
10. Reference comparison: find the breakdown in Kettama — It Gets Better (approximately 1:15 area). What does it do? What does it keep? What does it add? Does it match your decisions in this rep?

---

### Task 34: Outro construction rep

**File:** `src/content/guided-builds/reps/rep-19-outro-construction.json`

**ID:** `rep-19-outro-construction`  
**Title:** "The Outro — Winding Down Without Stopping"  
**Difficulty:** beginner  
**BPM:** 132  
**Key:** D minor  
**estimated_time_mins:** 20

**What it teaches:** The outro has to do two things: signal the track is ending, and give a DJ somewhere clean to mix out of. This rep teaches: element stripping order (what leaves first and why), how to strip without feeling abrupt, how to create a long clean tail that works in a DJ mix, and the difference between an abrupt cut and a musical fade.

**Steps (~7):**
1. Start with a full drop loop. Decide: DJ-friendly outro (long, looping — for DJs to mix over) or track outro (musical ending). This rep teaches the DJ-friendly version since that's the primary use case for UK garage production.
2. Bar 1 of outro: remove pads. Let the kick, bass, and hats continue alone. The listener hears the harmonic content disappear — this signals the outro has started.
3. Bar 5 of outro: remove the hat. Kick and bass only. The groove is stripped to its skeleton.
4. Bar 9 of outro: remove the bass. Kick only. The kick alone is a very clear DJ cue — "mix here."
5. Bar 13 of outro: volume automation on the kick, fading from 0dB to -inf over 4 bars. The kick fades out slowly. This gives a DJ the most mixing flexibility — they can bring in the next track at any point in this fade.
6. Atmosphere track: if present, keep it running through the entire outro and fade it out gradually over 8 bars (slower than the kick fade). The atmosphere leaving last gives the outro a sense of the track dissolving into space.
7. Export outro (16 bars). At 132 BPM = 29 seconds. Listen: does it feel like a natural ending? Does it give a DJ clear structural markers for when to mix in?

**Key insight:** The outro is for the DJ. Build it with a DJ's needs in mind: clear intro (drums only = easy to phrase match), long tail (time to mix), gradual strip (flexibility). A good outro is as invisible as good reverb — it just works.

---

## Phase 3B: Sample Sourcing Reps

These reps teach Splice as a skill — not just where to search but how to listen, evaluate, and decide. Sample sourcing is a production technique that most tutorials ignore. The difference between a track that sounds like a demo and one that sounds like a release is almost always sample selection.

### Task 35: Kick selection and auditioning rep

**File:** `src/content/guided-builds/reps/rep-20-kick-selection.json`

**ID:** `rep-20-kick-selection`  
**Title:** "Finding the Right Kick"  
**Difficulty:** beginner  
**BPM:** 136  
**Key:** E minor  
**estimated_time_mins:** 30

**What it teaches:** Kick selection is not guesswork. This rep teaches: the anatomy of a kick (attack click, body punch, tail rumble — which elements you need for your genre/BPM), how to A/B test candidates systematically, what to listen for specifically (not "does it sound good" but "does the 60–80Hz punch sit in the right register for my key"), and how BPM affects which kick tail length works.

**Steps (~8):**
1. Before opening Splice: understand the three parts of a kick. (1) Click/attack — the transient, usually 2–5kHz, what you hear as the initial "tick." (2) Body/punch — the low-mid weight, usually 60–90Hz, what you feel as the hit. (3) Tail/rumble — the sub frequency decay, usually 30–60Hz, how long the kick lasts. At 136 BPM you have 441ms between kicks. A kick tail longer than ~350ms will overlap with the next kick.
2. Open Splice. Search 'uk garage kick'. Filter: One-Shots, Drums, Kick. Listen to the first 20 results. Do not download yet — just listen. Notice which ones have distinct click, body, and tail. Notice which feel too short (no body), too long (tail clips the next kick), too bright (too much click, not enough punch), too dark (all thump, no click).
3. Download your top 5 candidates. Load all 5 into a Drum Rack on separate pads.
4. Create a 2-bar MIDI clip. Program kick on every beat (4-on-floor at 136 BPM). Play each kick candidate through this pattern for 30 seconds. Use Cmd+click to switch pads while the clip loops. Which one sounds like it belongs in a UK garage track at 136 BPM?
5. Now test in context: add a simple 4-note bass line (just the Kettama root movement transposed to E minor: E1, B0, G#1 — hold each note 2 beats). Which kick candidate sits best against the bass without fighting in the low end?
6. A/B test your top 2 candidates against a reference: load Kettama — It Gets Better in an audio track at the same volume. Switch between your candidates and the reference. Which is closest in feel? Not closest in tone — closest in how it makes the groove feel.
7. EQ the winner: add EQ Eight to the kick chain inside the Drum Rack. Boost 70Hz (+2dB, Q 1.5) for punch. Cut 280Hz (-3dB, Q 2) to remove boxiness. High-pass at 35Hz to remove sub-sub rumble. Compare before and after.
8. Save the kick with its EQ into a custom Drum Rack preset. Name it 'kick-ug-136-[date]'. You now have a production-ready kick you can reuse.

**Key insight:** A kick that sounds right in isolation often sounds wrong in context. Always test against bass. Always test against a reference track. The kick is the most important element in the mix — don't settle for the first one that sounds okay.

---

### Task 36: Full drum kit sourcing rep

**File:** `src/content/guided-builds/reps/rep-21-drum-kit-sourcing.json`

**ID:** `rep-21-drum-kit-sourcing`  
**Title:** "Building a Complete Drum Kit from Splice"  
**Difficulty:** beginner  
**BPM:** 138  
**Key:** G minor  
**estimated_time_mins:** 45

**What it teaches:** How to source every drum element for a complete UK garage kit — kick, clap, snare, closed hat, open hat, and a percussion element — so they sound like they belong together. The challenge: individual samples sound good in isolation but clash in a mix. This rep teaches the concept of a "kit family" — choosing samples that occupy different frequency ranges and have compatible tonal characters.

**Steps (~9):**
1. The kit brief: at 138 BPM G minor, you need: (1) kick (heavy, 60–80Hz body), (2) clap (crisp, 2–5kHz crack, dry), (3) closed hat (tight, 6–12kHz, short tail), (4) open hat (shimmer, brief — used sparingly on off-beats), (5) percussion hit (something unexpected — a rim, a clave, a wood block). One of each. Not more.
2. Source each element with a specific Splice search term and selection criterion:
   - Kick: 'uk garage kick punchy' → select based on body punch at 70Hz
   - Clap: 'crisp clap dry' → select based on crack transient, no reverb tail
   - Closed hat: 'tight closed hat crisp' → select based on short decay and clean tone
   - Open hat: 'open hat shimmer brief' → select based on brightness and how quickly it fades
   - Percussion: 'clave hit dry' or 'rim shot dry' or 'shaker one shot' → select anything percussive that feels right
3. Load all 5 into a Drum Rack. Standard pad layout: kick C1, clap D1, closed hat F#1, open hat A#1, percussion E1.
4. Programme a test groove: 4-on-floor kick, clap beats 2+4, closed hats 8 per bar, open hat on the and-of-4 in bar 2, percussion on beat 3 of bar 2 only. Loop 4 bars.
5. The frequency check: solo each element. Do they occupy clearly different frequency ranges? Kick = sub/low. Clap = high-mid. Hat = high. Percussion = mid. If two elements compete in the same range, one of them needs to be replaced or EQ'd.
6. The character check: do they feel like they belong to the same musical world? A very dark, organic kick with a very clean, digital hat can work, but requires deliberate EQ to bridge the gap. Test: loop the groove. Do the elements feel like they were made for each other?
7. EQ each element for its role: kick (boost 70Hz, cut 280Hz), clap (HP 200Hz, presence boost 3kHz), closed hat (HP 3kHz, gentle LP at 14kHz), open hat (HP 3kHz), percussion (HP 300Hz, gentle cut at 1kHz if honky).
8. Add GlueCompressor to the DRUMS group: Ratio 4:1, Attack 3ms, Release Auto, threshold for 2–3dB GR. Listen to the kit with and without. The GlueCompressor makes them feel like one instrument.
9. Export a 2-bar drum loop as WAV. This is your kit. Save the Drum Rack preset with all EQ settings. Build a library of kits — one per BPM/genre session — so you have ready-to-use starting points for future sessions.

---

### Task 37: Sample key detection and atmosphere sourcing rep

**File:** `src/content/guided-builds/reps/rep-22-atmosphere-sourcing.json`

**ID:** `rep-22-atmosphere-sourcing`  
**Title:** "Finding Atmospheres That Fit Your Key"  
**Difficulty:** intermediate  
**BPM:** 132  
**Key:** E minor  
**estimated_time_mins:** 25

**What it teaches:** Atmosphere/drone samples that clash with your key make a mix feel wrong without the listener knowing why. This rep teaches: how to test key compatibility of an audio loop, how to use Ableton's pitch detection tools, how to search Splice effectively for key-specific atmospheres, and what "compatible but not identical" tonality means (you don't need a sample in exactly E minor — any mode or tonal centre that shares most notes works).

**Steps (~7):**
1. The problem: you find a dark atmospheric drone on Splice that sounds perfect. You drop it into your E minor track. Something feels slightly off — the track sounds vaguely out of tune but you can't identify why. The drone is in F# minor (1 tone up from E). It clashes on certain notes. This rep teaches you to catch this before it ruins the mix.
2. When searching Splice for atmospheres: use the key filter if available. Filter for 'Key: E' or 'Key: A' or 'Key: Cm' — any sample labelled in E, A, or C minor works in a track built on the natural minor scale (they share many notes). Avoid samples labelled in major keys unless you intend the dissonance.
3. Key compatibility without exact key match: E natural minor shares notes with G major, C major, A minor, D minor, and B minor (they're all modes of the same scale). A drone in any of these keys will be harmonically compatible with your E minor track. This gives you a much wider pool of usable samples.
4. The hum test: drag any drone into an audio track. Loop it. Hum along with the drone — let your voice find a pitch that feels comfortable over it. Then play your E minor bass line. Does your hummed pitch appear in the E minor scale? If yes, the drone is compatible. If your hum sounds like it clashes with the scale, the drone is not compatible.
5. Ableton key detection: set the track tempo to match your project. If Warp is enabled on the audio clip, click the '?' next to the root note display and Ableton may suggest a key. This is not always accurate for atmospheric drones but is useful for loop-based samples.
6. Find 3 atmospheres for an E minor track using the hum test and key filter. Select the one that adds depth without adding a competing melody. Set volume -20dB.
7. The transposition option: if a drone sounds right harmonically but is pitched slightly wrong, you can transpose it in Ableton by semitones (right-click clip → Transpose). Transposing up or down 1–2 semitones often brings a nearly-compatible sample into correct alignment.

---

### Task 38: Vocal sample sourcing and placement rep

**File:** `src/content/guided-builds/reps/rep-23-vocal-sampling.json`

**ID:** `rep-23-vocal-sampling`  
**Title:** "Vocal Samples — Finding and Placing One-Shots"  
**Difficulty:** intermediate  
**BPM:** 136  
**Key:** A minor  
**estimated_time_mins:** 30

**What it teaches:** The vocal element is the most emotionally immediate layer in a garage/house track — even a single syllable can give the track personality and human warmth. This rep teaches: searching for usable vocal one-shots and chops, how to decide where in the arrangement a vocal element appears (not everywhere — placement is restraint), how to process a vocal sample for garage use (pitch, reverb, EQ), and how to avoid the "sample pack" feeling (sounding like every other track using the same free vocal).

**Steps (~8):**
1. The vocal brief for A minor at 136 BPM: you want something with human warmth and slightly soulful character — not a dance shout, not a melodic phrase, but a textural syllable or short phrase (1–4 syllables). The vocal should feel like a ghost in the track, not a lead.
2. Splice search terms: 'vocal one shot garage', 'vocal chop house', 'female vocal sample soulful', 'vocal hit dry'. Filter: One-Shots, Vocals. Listen to 30 candidates. Download your top 5. This takes time — vocal sourcing is a session activity, not a quick search.
3. Pitch the vocal to your key: drag each candidate into an audio track. Enable Warp. Set Warp mode to Complex Pro. Right-click and transpose to A (or to a note that sits in A natural minor). Some vocals pitch cleanly; others get artifacts — reject those.
4. Placement test: create a 16-bar loop. Place the vocal ONE TIME — on beat 1 of bar 5, or the and-of-2 of bar 3, or beat 3 of bar 7. Not every bar. Not every 2 bars. Once. Does the single appearance feel more impactful than if it were repeated every 2 bars?
5. The restraint rule: a vocal element that appears too frequently becomes a loop, not an event. Garage vocal chops work because they're unexpected. Predictable = invisible. Surprising = impactful. Test: put the vocal on every 4 bars vs every 8 bars vs once per 16-bar section. The less frequent version will feel more memorable.
6. Processing: add Reverb send at -16dB (the vocal sits in the same space as the pads, not upfront). Add a gentle pitch correction if available (Ableton doesn't have Auto-Tune but you can micro-tune with clip transpose). EQ Eight: HP 150Hz (remove low mud), gentle presence boost +2dB at 2–3kHz.
7. The wet/dry decision: try the vocal fully dry (no reverb) vs with the same reverb as the pads. Dry = present and percussive (works for a chop element). With reverb = floats in the same space as the pads (works for an atmospheric element). Both are valid; they create different characters.
8. Export a 16-bar clip with the vocal included. Listen on earbuds. Does the vocal feel like it belongs in the track, or does it feel like an addition? If it feels added-on, lower its volume by 3dB and re-evaluate.

---

## Phase 3C: Drum Programming Depth Reps

### Task 39: Hat pattern programming rep

**File:** `src/content/guided-builds/reps/rep-24-hat-programming.json`

**ID:** `rep-24-hat-programming`  
**Title:** "Hat Patterns — Swing, Velocity, and Feel"  
**Difficulty:** beginner  
**BPM:** 134  
**Key:** none (drums only)  
**estimated_time_mins:** 25

**What it teaches:** The hat pattern is the most expressive drum element — it carries the swing, the groove, and the human feel more than any other element. This rep teaches: the three core hat rhythms used in UK garage (straight 8th-note, swing 8th, and the rolling triplet-feel pattern), how velocity variation creates the feel of a live drummer, how to use Ableton's Groove Pool for swing, and how the hat pattern changes the perceived tempo of a track without changing the BPM.

**Steps (~8):**
1. Pattern A — straight 8ths: 8 hats per bar, equally spaced, velocity 70 throughout. This is the most common and most mechanical pattern. Sounds precise and cold. Loop it for 30 seconds.
2. Pattern B — velocity variation: same 8 hats, but velocity cycle: 80, 55, 90, 55, 80, 55, 100, 55. Alternating strong-weak-strong-weak creates the illusion of up-beats and down-beats. Loop 30 seconds. Compare to Pattern A. Same rhythm, different feel.
3. Pattern C — swing via Groove Pool: copy Pattern A. Drag 'Swing 8-05' from the Groove Pool onto the hat MIDI clip. Amount 65%. The off-beat hats are now slightly late — behind the beat. This is the rolling, pushing quality of UK garage hats. Loop 30 seconds. Compare to both previous patterns.
4. Pattern D — the UK garage rolling hat: every 2 bars, add an extra 16th-note hat just before beat 1 of bar 2 (a pickup note). Velocity 90. This creates a brief double-hat "flicker" that gives the groove a forward rush at the bar boundary. A subtle but characteristic technique.
5. Pattern E — open hat placement: in a 2-bar pattern, add a single open hat (A#1) on the and-of-4 of bar 2 only. Velocity 80. One open hat per 2 bars. This is the "breath" of the groove — a single moment where the hat opens and shimmers.
6. Combine: build the full hat pattern — Pattern C (swing 8ths) as the base, Pattern D (pickup note) added at bar boundaries, Pattern E (one open hat) once per 2 bars. This is a complete UK garage hat pattern.
7. The tempo illusion: compare your combined hat pattern against a straight hat pattern at the same BPM. The swing version feels slightly slower and more laid-back. The straight version feels faster and more mechanical. Both are at 134 BPM. The hat pattern changes the perceived tempo.
8. Export the hat pattern only (no kick, no clap) as a 2-bar loop. This is your groove reference. When a future project feels rhythmically stiff, apply this hat pattern and compare.

---

### Task 40: Clap and snare layering rep

**File:** `src/content/guided-builds/reps/rep-25-clap-layering.json`

**ID:** `rep-25-clap-layering`  
**Title:** "Clap Layering — Building the Perfect Snare Sound"  
**Difficulty:** beginner  
**BPM:** 140  
**Key:** none (drums only)  
**estimated_time_mins:** 20

**What it teaches:** No single clap or snare sample sounds like a finished production clap. Professional drum sounds are always two or more layers combined — each adding something the other lacks. This rep teaches: the two-layer clap (crack + body), the snare body under a clap for weight, how to tune layers relative to each other, and the EQ logic for each layer in the combined sound.

**Steps (~7):**
1. Layer 1 — the crack: find a very dry, sharp clap with a high transient frequency (3–5kHz crack, almost no tail). This is the attack of the sound — the click that makes it feel immediate. Volume: 0dB (reference level).
2. Layer 2 — the body: find a snare or clap with more low-mid presence (200–800Hz "crack body") and a slightly longer tail. This gives the sound warmth and weight. It should sound different to layer 1 — softer, less clicking, more "thwap." Volume: start at -3dB.
3. Stack them on separate pads in the Drum Rack. Trigger both simultaneously from the same MIDI note using a Drum Rack chain or by mapping both to C2. Listen to both layers together vs each alone. They should create a combined sound that neither has individually.
4. Timing offset: try nudging layer 2 by +5ms (it hits just after layer 1). The crack arrives first, the body arrives 5ms later. This is how real snares work — the shell crack precedes the body. Compare 0ms offset vs 5ms offset. The 5ms offset often sounds more natural.
5. EQ for layering: Layer 1 (crack): HP at 800Hz — pure high frequency crack only. Layer 2 (body): LP at 4kHz — low-mid body only. Now the two layers don't compete. Each occupies a different frequency range. Together they cover the full snare spectrum.
6. Pitch tuning: if the layers sound dissonant together, try tuning Layer 2 up or down 1–2 semitones until they feel harmonically compatible. Snare drums have a tonal centre — tuning them to your track key is an advanced technique that makes the whole kit feel musically integrated.
7. Compare the combined layer against a single-sample clap. Your layered version should feel fuller, more present, and more three-dimensional. Export both as one-shot references.

---

## Phase 3D: Genre-Specific Technique Reps

### Task 41: Bassline/acid bass rep

**File:** `src/content/guided-builds/reps/rep-26-acid-bassline.json`

**ID:** `rep-26-acid-bassline`  
**Title:** "Acid Bassline — The TB-303 Style in Serum"  
**Difficulty:** intermediate  
**BPM:** 130  
**Key:** A minor  
**estimated_time_mins:** 35

**What it teaches:** The bassline genre (Yorkshire-influenced UK bassline/garage) is defined by the 303-style acid bass: a mono synth line with rapid filter automation, resonance peaks, and rhythmic accent notes. This rep teaches how to build an acid-style bass in Serum V2, write a characteristic bassline pattern (8th notes with accents and slides), and use filter automation to create the filter sweep that defines the genre.

**Steps (~10):**
1. Concept: acid bass originates from the Roland TB-303 bass synthesiser. Its defining characteristics: mono, sawtooth wave, resonant low-pass filter, automated filter cutoff that opens and closes rhythmically, and short note slides between some notes. In Serum V2 you can approximate this.
2. Serum setup: Init Preset. OSC A: Basic Shapes, WT POS all the way right (sawtooth). UNISON: 1 voice (mono — acid bass is always mono). OSC B: disabled. Filter: MG Low 24, Cutoff 25% (nearly closed), Resonance 40% (high — this is the peak that makes it "squelch"). ENV 1: Attack 0, Sustain 100%, Release 80ms.
3. The envelope on the filter: ENV 2 → Filter Cutoff, Amount +60%, Attack 0ms, Decay 100ms, Sustain 0%. Now every note gets a brief filter open-then-close. The amount of decay (100ms) controls how long the squelch lasts. This is the primary sound of an acid bass.
4. Write a bassline pattern: create an 8-bar MIDI clip. The pattern is not root-note-per-chord like the other reps — it's a rhythmic melodic line that moves between notes rapidly. Try: A2 (1/8th note), A2, E2, G2, A2, C3, B2, A2 (all 8th notes, varying velocities 80-100). This creates a stepped, rhythmic melody rather than held roots.
5. Accents: in a 303 bassline, some notes are accented (louder, with more filter open) and some are normal. Set accent notes to velocity 110 (the high velocity triggers the filter envelope harder = more squelch). Non-accent notes at velocity 70 (the filter barely opens). Loop and listen — the accents should jump out with a pronounced squelch.
6. Slides: a 303 slide means the pitch glides from one note to the next rather than jumping. In Serum V2, enable the glide (portamento) function: set the PORTA knob (portamento time) to about 80ms. Now any MIDI notes that overlap slightly in the piano roll will slide between pitches. Add a 5ms overlap between 2-3 adjacent notes in your bassline. The slides add the characteristic "wah-wah" pitch movement of acid.
7. The full filter automation: in Arrangement view, automate the Serum filter cutoff over 8 bars — start at 25% (nearly closed), sweep to 75% over bars 1–4, then back down to 25% over bars 5–8. This large-scale filter sweep layers over the per-note envelope. The combination of per-note squelch + bar-level sweep = complete acid bass movement.
8. Add drums: minimal 4-on-floor kick at 130 BPM, clap on beats 2+4. The drums should feel harder and more insistent than the garage reps — bassline/acid house drums are more aggressive. Search Splice: 'bassline kick hard' or 'acid house kick'. Use a kick with more upper-mid energy than the garage kicks.
9. Compare your acid bassline against a reference: search YouTube for 'UK bassline house' or 'DJ Q bassline' or 'Niche Records bassline'. Listen for the filter movement, the accents, the slides. Does yours feel in the same territory?
10. Export the 8-bar acid bassline + drums: 'rep-26-acid-bassline-v1.wav'. Save session. The acid bass is the defining element of Yorkshire bassline — understanding it opens a whole genre.

---

### Task 42: House piano stab rep

**File:** `src/content/guided-builds/reps/rep-27-piano-stab.json`

**ID:** `rep-27-piano-stab`  
**Title:** "House Piano Stab — Off-Beat Chord Energy"  
**Difficulty:** beginner  
**BPM:** 126  
**Key:** F minor  
**estimated_time_mins:** 25

**What it teaches:** The piano stab is the defining element of classic house music — a short, sharp chord hit on the off-beat that creates forward momentum and gospel-influenced energy. This rep teaches: the piano stab rhythm (off-beats of 2 and 4, or the and-of-2 and and-of-4), how to voice the chord for a piano stab (closed voicing, midrange, no reverb tail), and how the stab interacts with the kick and bass rhythmically.

**Steps (~8):**
1. Concept: the house piano stab is not a pad. It's a short, percussive chord hit — velocity 100, note length 1/8th note (not held). It creates energy by hitting on the off-beat while the kick is on the beat. The rhythmic tension between kick (on-beat) and stab (off-beat) is the engine of house music.
2. Serum V2 piano setup: Init Preset. OSC A: load 'Acoustic-Piano' wavetable if available, or Basic Shapes at 40% WT POS (toward a slightly rounded tone). UNISON: 2 voices, detune 4 cents (subtle — piano should be focused, not wide). FILTER: MG Low 24, Cutoff 80% (open — piano should be bright). ENV 1: Attack 0ms, Decay 400ms, Sustain 20%, Release 150ms. This envelope creates a quick pluck that decays — a piano-like shape.
3. The stab voicing in F minor: closed voicing, midrange. For Fm: F3, Ab3, C4 (tight, no wide spread). For Dbmaj: Db3, F3, Ab3. For Abmaj: Ab3, C4, Eb4. The piano stab chord should span less than an octave — it needs to be tight and punchy.
4. The stab rhythm: in a 2-bar MIDI clip, place the stab on these positions: bar 1 beat 2 and-of (position 1.2.3), bar 1 beat 4 and-of (position 1.4.3). Bar 2 same positions. This is the classic and-of-2, and-of-4 rhythm. At 126 BPM these off-beats feel like the track is leaning forward.
5. Note length: the stab should be 1/8th note long (short!). Not held. The chord hits and immediately releases. This is critical — a long stab becomes a pad. The shortness is what makes it "stab."
6. No reverb: add a very small amount of reverb room effect (Decay 0.2s) — just enough to not sound completely dry. Piano stabs should feel immediate and present, not spacious. Too much reverb makes them wash together and lose their percussive character.
7. EQ: HP 200Hz (remove the piano's low end — the bass handles that), gentle presence boost +2dB at 2kHz (adds the attack click that makes stabs feel incisive).
8. Loop with kick at 126 BPM (4-on-floor): kick on every beat, piano stab on off-beats. This is the core relationship. Does the stab feel like it's pushing the kick? Does the track feel like it's leaning forward? At 126 BPM this should feel like classic Chicago/UK piano house.

---

### Task 43: Two-step groove programming rep

**File:** `src/content/guided-builds/reps/rep-28-two-step-groove.json`

**ID:** `rep-28-two-step-groove`  
**Title:** "2-Step Groove — Variations and Fills"  
**Difficulty:** intermediate  
**BPM:** 136  
**Key:** none (drums only)  
**estimated_time_mins:** 25

**What it teaches:** The 2-step is not a single pattern — it's a family of patterns. The basic 2-step (rep-01) was one variation. This rep teaches 4 more 2-step variations and how to programme fills and transitions between them. The ability to vary the 2-step pattern across different sections gives a track rhythmic life without changing the BPM.

**Steps (~8):**
1. Recall the basic 2-step (rep-01): kick on beat 1 and the and-of-2. This is the foundation. Loop it for 8 bars until it's fully in your body.
2. Variation 2 — the "double kick" 2-step: add a second kick on beat 3 (kick at 1, and-of-2, and beat 3). The third kick creates a brief moment of density. Compare against the basic 2-step. Does beat 3 feel heavy or like a roll?
3. Variation 3 — the "skip" 2-step: kick on beat 1 and beat 3 only (no off-beat). This sounds like half-time — the absence of the and-of-2 kick is felt as negative space. This pattern is excellent for breakdowns and intros.
4. Variation 4 — the "anticipated" 2-step: kick on the and-of-4 of the previous bar and beat 1 of the current bar. The kick anticipates beat 1 by arriving half a beat early. Creates a rushing, forward-leaning feel. This is used in more aggressive UK garage and speed garage.
5. Variation 5 — the "ghost" 2-step: standard 2-step kicks but add a ghost kick hit at very low velocity (30) on beat 2. The ghost hit is barely audible — it adds subliminal rhythmic weight without creating an obvious pattern change. This is a producer's technique — listeners feel it, can't identify it.
6. Fills: between pattern variations, add a 1-bar fill on the 4th or 8th bar. Simple fill: double kick on beat 4 of the fill bar (two kicks in quick succession — positions 1.4 and 1.4.3). This signals a pattern change is coming.
7. Build a 16-bar sequence using different variations: bars 1–4 basic 2-step, bars 5–8 variation 2 (double kick), bars 9–12 basic 2-step, bar 12 fill, bars 13–16 variation 4 (anticipated). This is a 16-bar drum sequence with movement and variety.
8. Export the 16-bar sequence. Listen back and ask: does the variation feel intentional or random? Does each variation serve a clear purpose (intro feel, build tension, release, accent)? The rule: vary the pattern with intent, not decoration.

---

## Phase 3E: Mix Depth Reps

### Task 44: Reference track mixing rep

**File:** `src/content/guided-builds/reps/rep-29-reference-mixing.json`

**ID:** `rep-29-reference-mixing`  
**Title:** "Mixing Against a Reference — Closing the Gap"  
**Difficulty:** intermediate  
**BPM:** any  
**Key:** any  
**estimated_time_mins:** 45

**What it teaches:** Reference mixing is one of the most powerful and most underused production techniques. This rep teaches a systematic approach: how to import a reference track, volume-match it to your own track (the most common mistake is not matching volume before comparing), and then identify specific differences in kick punch, low-end weight, high-frequency air, and overall width. The goal is not to sound identical — it's to understand the gap.

**Steps (~8):**
1. Import your reference track (Kettama, IC, MPH, Sammy Virji, or BL3SS — whichever matches your track's genre and tempo) into a new audio track in your Ableton session. Disable it in the mix — it should not play with your track, only instead of it.
2. Volume matching: this is critical. Before any comparison, both tracks must play at the same loudness level (not the same fader level — the same perceived loudness). Use Ableton's volume meter or a loudness meter plugin (if available) to find the average loudness of both tracks and set faders so they match within 0.5dB. If you compare a quiet track to a loud reference, every decision about "why does the reference sound better" is wrong.
3. The comparison loop: find the most energetic 30-second section of your reference (usually the drop). Create a loop in Ableton that plays 8 bars of your track, then 8 bars of the reference (using clip launching or automation). Listen to this loop 10 times. On each listen, focus on one element only: kick, bass, pads, hats, overall width. Note what's different.
4. Kick analysis: is the reference kick punchier? More body? Shorter tail? Use EQ Eight to boost/cut on your kick to close the gap. The most common issue: reference kicks have more 60–80Hz punch (add a bell boost there) and less 200–300Hz boxiness (cut there).
5. Low-end analysis: does the reference bass feel heavier or lighter? Does the sub feel more present on small speakers (usually a Saturator difference)? Compare bass levels — the reference may have the bass louder relative to the kick than you do.
6. High frequency air: reference tracks often have more "air" (10–16kHz presence on pads and hats). Add a gentle high shelf +1.5dB at 12kHz on the PAD track. Compare. This is often what makes a reference sound "released" vs "demo."
7. Stereo width: reference tracks often feel wider. Check your mid/side balance — are your pads using the Chorus or stereo width tools properly? The kick and bass should be narrow (mono). The pads and atmosphere should be wide. If your track sounds narrower than the reference, increase the Chorus depth or the Utility width on the pads.
8. The gap document: write down 3 specific differences between your track and the reference. Not "it sounds better overall" but "the kick has more punch at 70Hz," "the pads feel wider," "the high end has more air." These 3 items are your next session's focus. Repeat this process after each session until the gap is small.

---

### Task 45: Headroom and gain staging rep

**File:** `src/content/guided-builds/reps/rep-30-gain-staging.json`

**ID:** `rep-30-gain-staging`  
**Title:** "Gain Staging — Managing Headroom Across Your Mix"  
**Difficulty:** intermediate  
**BPM:** any  
**Key:** any  
**estimated_time_mins:** 30

**What it teaches:** Gain staging is the invisible architecture of a mix. Without it, channels clip, compressors behave unpredictably, and the mix peaks without feeling loud. This rep walks through a complete gain staging pass on a 5-track session (kick, bass, pad, hat, atmosphere) and teaches: what headroom is and why it matters, the target level for each element type, how to check that no individual track is clipping before the master, and how to use the master Limiter properly as a safety net (not as a gain tool).

**Steps (~7):**
1. What is gain staging: every device in your signal chain adds or reduces level. If level gets too high at any point in the chain — inside a plugin, on a channel fader, or at the master — you get distortion (not the good kind) or unpredictable plugin behaviour. Gain staging means keeping every signal in a healthy range throughout the entire chain.
2. Set all track faders to 0dB. Listen to the mix. Check the master channel meter — is it hitting above 0dBFS? If yes, gain staging is needed. Target: master peaks should be -3 to -6dBFS before the Limiter.
3. Gain staging order — work upstream to downstream. Start with the loudest element (usually the kick): check its level INSIDE the Drum Rack, before the GlueCompressor. It should peak at around -12dBFS pre-processing. If it's peaking at 0dBFS before any processing, reduce the Drum Rack volume or add a gain reduction at the source.
4. The -18dBFS target: most professional audio engineers target -18dBFS average (not peak) for individual tracks going into processing. This gives ample headroom for plugins to work correctly. At -18dBFS average, peaks may hit -8 to -10dBFS. Use Ableton's gain meter to check.
5. Set each track's pre-fader gain so it averages around -18dBFS: kick should peak around -10dBFS pre-fader, bass around -12dBFS, pads around -16dBFS, hats around -20dBFS. These are rough targets — the exact values depend on your session. The goal is no channel consistently hitting 0dBFS.
6. The master chain: after gain staging individual tracks, the master should sum to around -6 to -3dBFS peaks before the Limiter. If it's still too hot, reduce all track faders by 3dB simultaneously (Shift+click and drag multiple faders) rather than adjusting each individually.
7. Limiter as a safety net: the master Limiter (Ceiling -0.3dB) should only catch occasional peaks — its gain reduction meter should flash briefly, not stay lit. If the Limiter is constantly engaged (gain reduction 3dB+ all the time), the mix is too loud upstream. Go back and reduce levels before the master. The Limiter is a safety net, not a volume knob.

---

## Phase 3F: Phase 3 Content Summary

| Category | Task | Rep IDs | What It Teaches |
|---|---|---|---|
| Arrangement sections | 30–34 | rep-15 to rep-19 | Intro, build-up, drop entry, breakdown, outro |
| Sample sourcing | 35–38 | rep-20 to rep-23 | Kick selection, drum kit building, atmosphere key-matching, vocal sampling |
| Drum programming | 39–40 | rep-24 to rep-25 | Hat patterns with swing, clap/snare layering |
| Genre techniques | 41–43 | rep-26 to rep-28 | Acid bassline, house piano stab, 2-step variations |
| Mix depth | 44–45 | rep-29 to rep-30 | Reference mixing, gain staging |

**Total new reps in Phase 3:** 16 (rep-15 through rep-30)

**What Phase 3 adds to the learning system:** Phase 1 taught loops. Phase 2 taught harmony, sound design, and full builds. Phase 3 teaches craft — the invisible skills that separate a demo from a release. Arrangement logic, sample selection instincts, groove programming depth, genre fluency, and mix awareness. A producer who completes Phases 1–3 has the tools to make finished, genre-appropriate UK garage, bassline, and house tracks.

**Sequencing recommendation:** Complete all Phase 2 reps before starting Phase 3. The arrangement section reps (Tasks 30–34) assume the user can build a complete loop (taught in Phase 2). The sample sourcing reps (Tasks 35–38) assume basic Splice familiarity. The genre technique reps (Tasks 41–43) assume comfort with Serum V2 from Phase 2.
