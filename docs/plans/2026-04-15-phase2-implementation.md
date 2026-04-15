# Music Theory Learner — Phase 2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deepen the learning content, add a daily practice system with progress tracking, finish all 25 guided builds, and teach Serum V2 from zero to functional. Phase 2 turns the scaffold into a real learning tool.

**What Phase 1 delivered:** App shell, 5 track breakdowns, 3 beginner reps + 1 Kettama spinoff, Theory reference (4 scales, 6 chords, 6 rhythms), Ableton cheatsheet (3 entries), Builder UI. Deployed at music-theory-learner.pages.dev.

**Serum V2 target:** By end of Phase 2, the user can open Serum V2, navigate the UI confidently, build a sub bass from scratch, build a pad from scratch, build a Reese bass, and understand what every section of the synth does in the context of UK garage sounds. All Serum content is anchored to sounds in the 5 source tracks — no abstract synthesis theory.

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

**Step: Verify + commit**
```bash
git commit -m "feat: effects deep dives — saturation, EQ strategy, signal flow"
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
15. Task 19 — Cheatsheet expansion (15+ entries)
16. Task 20 — Drum rack downloads
17. Task 16 — Full spinoffs + originals
18. Task 21 — CI fix

---

## Complete Phase 2 Learning Outcomes

By the end of Phase 2, the user can:

**Theory:**
- Derive any chord in a minor key from the scale (no memorisation)
- Explain why VI→III→i feels inevitable (common tones)
- Hear phrygian tension and identify it by ear
- Transpose any concept (phrygian bass, chord loop) to any key without help

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

**Arrangement:**
- Can describe the psychological job of each section
- Uses transitions intentionally (silence, filter sweep, reverb throw, drum fill)
- Draws an energy curve before building
- Can map the structure of any reference track by ear

**Builds:**
- 25/25 guided builds available
- 3 beginner reps completed (reps available for all 7)
- Full Kettama spinoff guide with Serum patch detail
