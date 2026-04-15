# Music Theory Learner — Phase 2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deepen the learning content, add a daily practice system with progress tracking, and finish all 25 guided builds. Phase 2 turns the scaffold into a real learning tool.

**What Phase 1 delivered:** App shell, 5 track breakdowns, 3 beginner reps + 1 Kettama spinoff, Theory reference (4 scales, 6 chords, 6 rhythms), Ableton cheatsheet (3 entries), Builder UI. Deployed at music-theory-learner.pages.dev.

---

## Phase 2A: Theory Deep Dives

### Task 11: Deep Dive content type + Theory page upgrade

**Goal:** Replace surface-level expandable cards with a proper "Deep Dives" tab on the Theory page. Each deep dive is a long-form article that teaches one concept in depth — with track references, MIDI examples, and a practice exercise at the end.

**Files:**
- Create: `src/content/theory/deep-dives/vi-iii-i-loop.json`
- Create: `src/content/theory/deep-dives/phrygian-tension.json`
- Create: `src/content/theory/deep-dives/bass-implied-harmony.json`
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
  "practice_exercise": {
    "instruction": "Program the VI→III→i loop in F minor (not Bb minor). Work out the three chord names from the F minor scale, then voice them in Serum or a piano roll. The notes are all in the F natural minor scale.",
    "answer_hint": "F minor scale: F G Ab Bb C Db Eb. VI = Dbmaj7 (Db, F, Ab, C). III = Abmaj (Ab, C, Eb). i = Fm (F, Ab, C)."
  },
  "key_takeaway": "One sentence that sticks."
}
```

**Step 1: Write 3 deep dives**

Deep dive 1 — `vi-iii-i-loop.json`: Full analysis of Kettama's VI→III→i. Cover: what each chord is, why all three are diatonic to natural minor, what common tones do, why the progression feels inevitable. Reference the chord voicings from the spinoff build. End with: transpose the loop to F minor as an exercise.

Deep dive 2 — `phrygian-tension.json`: Full analysis of the phrygian b2 (MPH Raw). Cover: what phrygian mode is vs natural minor (only the 2nd is different), why one semitone of distance creates maximum tension, how note length and velocity shape the tension arc, why MPH has no chord progression and doesn't need one. Exercise: write a 4-bar phrygian bass line in A minor (root = A, tension = Bb).

Deep dive 3 — `bass-implied-harmony.json`: Full analysis of BL3SS's approach. Cover: what implied harmony is, how the ear fills in chord tones from a single bass note, why this technique creates space, the specific i→bIII→bVI→iv motion in D minor. Exercise: write a new 4-bar bass-implied progression in G minor (work out the chord names first, then write only the roots).

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

Article renders: title, subtitle block, sections with headings and body text, MIDI example pills (note names displayed as tags), practice exercise box (highlighted block with instruction + expandable answer hint), key takeaway block.

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

### Task 19: Cheatsheet expansion to 15+ entries

**Goal:** Expand from 3 to 15+ cheatsheet entries covering the full Ableton toolkit needed for UK garage production.

**Files:** `src/content/cheatsheet/` — 12 new JSON files, update `index.js`

**New entries to write:**

1. `groove-pool.json` — How to use Ableton's Groove Pool: drag grooves to clips, global groove amount, extracting groove from a reference audio clip. Tags: groove, swing, timing, feel.

2. `automation.json` — Drawing automation: Cmd+click to add breakpoints, automation lanes, unlinking clip envelopes. Tags: automation, movement, dynamics.

3. `operator-sub-bass.json` — Building a sub bass in Operator from scratch: sine oscillator only, pitch envelope for punch, filter off, no FX. Tags: operator, sub bass, synthesis.

4. `wavetable-pad.json` — Building a pad in Wavetable: oscillator selection, unison, filter, amp envelope. Tags: wavetable, pad, synthesis, serum alternative.

5. `serum-basics.json` — Serum quickstart: OSC A/B, filter, envelope, unison. How to navigate the UI. Tags: serum, synthesis, oscillator.

6. `arrangement-view.json` — Arrangement view basics: session to arrangement, loop brace, clip duplication, track freeze. Tags: arrangement, workflow, session view.

7. `return-tracks.json` — Return tracks and sends: how to set up a reverb return, send knob routing, pre/post fader. Tags: sends, reverb, routing, return track.

8. `utility-mono.json` — Utility device for mono bass: Width = 0% for sub bass, Mid/Side balance, DC offset removal. Tags: utility, mono, width, stereo.

9. `audio-effect-rack.json` — Audio Effect Rack: chains, macros, parallel processing, dry/wet per chain. Tags: rack, macros, parallel, chains.

10. `midi-effect-rack.json` — MIDI tricks: Chord MIDI effect for instant voicings, Scale MIDI to lock notes to a key, Arpeggiator basics. Tags: midi, chord, scale, arpeggiator.

11. `clip-envelopes.json` — Clip envelopes: how to draw volume/pitch/filter automation inside a MIDI clip, loop envelopes, LFO-like movement without a plugin. Tags: clip envelope, automation, modulation.

12. `resampling.json` — Resampling in Ableton: route Master to a new audio track, record your own output, process it further, freeze/flatten. Tags: resampling, bounce, flatten, resample.

**Step: Update index.js** — import all 15 entries, re-export.

**Step: Verify search still works with 15 entries**

**Step: Commit**
```bash
git commit -m "feat: expand cheatsheet to 15 entries"
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
| Entry/mid spinoffs | 4 | 0 done → Task 15 adds all 4 |
| Full spinoffs | 3 | 1 done (Kettama) → Task 16 adds 2 |
| Originals | 4 | 0 done → Task 16 adds all 4 |
| Theory deep dives | 6 | 0 done → Tasks 11–12 add all 6 |
| Cheatsheet entries | 15 | 3 done → Task 19 adds 12 |

**Total builds after Phase 2:** 25/25 complete.
**Total theory deep dives:** 6.
**Total cheatsheet entries:** 15.

---

## Task Order (recommended)

1. Task 11 — Theory Deep Dives Part 1 (highest learning value, fast)
2. Task 12 — Theory Deep Dives Part 2
3. Task 17 — Progress tracking (makes the builds feel purposeful)
4. Task 18 — Daily practice (depends on progress tracking)
5. Task 13 — Beginner reps 4–7 (content)
6. Task 14 — Intermediate reps 8–14 (content)
7. Task 15 — Spinoffs 2–4 (content)
8. Task 19 — Cheatsheet expansion (quick wins)
9. Task 20 — Drum rack downloads (requires Python script run)
10. Task 16 — Full spinoffs + originals (most work, highest payoff)
11. Task 21 — CI fix (housekeeping)
