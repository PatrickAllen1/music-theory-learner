# Music Theory Learner — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a static React web app for learning music production through guided track creation, deployed to Cloudflare Pages.

**Architecture:** Vite + React + Tailwind + React Router. All content as static JSON/Markdown in `src/content/`. No backend. Four sections: Guided Track Builder, Track Library, Theory Reference, Ableton Cheatsheet.

**Tech Stack:** React 18, Vite, Tailwind CSS v3, React Router v6, Cloudflare Pages

---

## Phase 1: Project Scaffold

### Task 1: Init Vite + React project

**Files:**
- Create: `package.json`, `vite.config.js`, `index.html`, `src/main.jsx`, `src/App.jsx`

**Step 1: Scaffold with Vite**

```bash
cd /Users/patrickalfante/music-theory-learner
npm create vite@latest . -- --template react
```

**Step 2: Install dependencies**

```bash
npm install
npm install react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Step 3: Configure Tailwind**

Edit `tailwind.config.js`:
```js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

Edit `src/index.css` — replace contents with:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Step 4: Verify it runs**

```bash
npm run dev
```
Expected: Vite dev server at localhost:5173, React app renders.

**Step 5: Commit**

```bash
git add .
git commit -m "feat: scaffold Vite + React + Tailwind"
```

---

### Task 2: Cloudflare Pages config

**Files:**
- Create: `wrangler.toml`, `.github/workflows/deploy.yml` (optional)

**Step 1: Add wrangler.toml**

```toml
name = "music-theory-learner"
compatibility_date = "2024-01-01"

[site]
bucket = "./dist"
```

**Step 2: Add build config**

Verify `package.json` has:
```json
"scripts": {
  "build": "vite build",
  "preview": "vite preview"
}
```

**Step 3: Test build**

```bash
npm run build
```
Expected: `dist/` folder created with static assets.

**Step 4: Commit**

```bash
git add wrangler.toml
git commit -m "feat: add Cloudflare Pages config"
```

---

### Task 3: App shell — layout + routing

**Files:**
- Modify: `src/App.jsx`
- Create: `src/components/Layout.jsx`
- Create: `src/components/Nav.jsx`
- Create: `src/pages/Builder.jsx`
- Create: `src/pages/Library.jsx`
- Create: `src/pages/Theory.jsx`
- Create: `src/pages/Ableton.jsx`

**Step 1: Write Nav component**

`src/components/Nav.jsx`:
```jsx
import { NavLink } from 'react-router-dom'

const links = [
  { to: '/builder', label: 'Builder' },
  { to: '/library', label: 'Library' },
  { to: '/theory', label: 'Theory' },
  { to: '/ableton', label: 'Ableton' },
]

export default function Nav() {
  return (
    <nav className="flex gap-6 px-6 py-4 bg-zinc-900 border-b border-zinc-700">
      <span className="text-zinc-100 font-mono font-bold mr-auto">music-theory-learner</span>
      {links.map(({ to, label }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) =>
            `text-sm font-mono ${isActive ? 'text-white' : 'text-zinc-400 hover:text-zinc-200'}`
          }
        >
          {label}
        </NavLink>
      ))}
    </nav>
  )
}
```

**Step 2: Write Layout component**

`src/components/Layout.jsx`:
```jsx
import Nav from './Nav'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <Nav />
      <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
    </div>
  )
}
```

**Step 3: Write stub pages**

Each page (`Builder.jsx`, `Library.jsx`, `Theory.jsx`, `Ableton.jsx`):
```jsx
export default function Builder() {
  return <div className="text-zinc-400">Builder — coming soon</div>
}
```

**Step 4: Wire up App.jsx**

```jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Builder from './pages/Builder'
import Library from './pages/Library'
import Theory from './pages/Theory'
import Ableton from './pages/Ableton'

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/builder" replace />} />
          <Route path="/builder" element={<Builder />} />
          <Route path="/library" element={<Library />} />
          <Route path="/theory" element={<Theory />} />
          <Route path="/ableton" element={<Ableton />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
```

**Step 5: Verify routing works**

```bash
npm run dev
```
Expected: Nav renders, all four links navigate correctly, dark theme visible.

**Step 6: Commit**

```bash
git add src/
git commit -m "feat: app shell with nav, layout, routing"
```

---

## Phase 2: Track Library

### Task 4: Track data model + seed content

**Files:**
- Create: `src/content/tracks/kettama-rolling-forever.json`
- Create: `src/content/tracks/interplanetary-criminal-bassline-ting.json`
- Create: `src/content/tracks/sammy-virji-bruk-out.json`
- Create: `src/content/tracks/ts7-piano-joint.json`
- Create: `src/content/tracks/dj-heartstring-deep-one.json`
- Create: `src/content/tracks/index.js`

**Step 1: Write first seed track JSON**

`src/content/tracks/kettama-rolling-forever.json`:
```json
{
  "id": "kettama-rolling-forever",
  "title": "Example Rolling Track",
  "artist": "Kettama",
  "bpm": 130,
  "key": "F minor",
  "scale": "natural minor",
  "swing_pct": 54,
  "time_sig": "4/4",
  "structure": ["intro", "build", "drop1", "breakdown", "drop2", "outro"],
  "chords": ["Fmin7", "Ebmaj7", "Dbmaj7", "Cm7"],
  "signature_elements": [
    "Rolling 4-on-the-floor kick with open hat on the off-beat",
    "Pitched vocal chop on the 2 and 4",
    "Sub bass with octave jump on bar 3",
    "Swung hi-hats at 54% groove"
  ],
  "ableton_techniques": [
    "Groove pool swing (54%) applied to MIDI clips",
    "Sidechain compressor on pads triggered by kick",
    "Simpler for vocal chop — single shot mode, mapped across keys",
    "Drum Rack with layered kick (sub + click)"
  ],
  "theory_notes": "This track sits in F natural minor. The chord loop — Fmin7, Ebmaj7, Dbmaj7, Cm7 — borrows from the relative major (Ab major) family. The Ebmaj7 and Dbmaj7 give it that bittersweet, slightly jazzy quality that defines Kettama's sound. The Cm7 resolves back to the root with tension. In an analytical frame: think of these chords as vectors — each one has a direction and weight, and the progression cycles through tension and release every 4 bars.",
  "splice_searches": [
    "punchy garage kick 130bpm",
    "pitched vocal one shot uk garage",
    "swung open hi-hat"
  ],
  "guided_build_id": "kettama-rolling-garage"
}
```

**Step 2: Write the track index**

`src/content/tracks/index.js`:
```js
import kettamaRolling from './kettama-rolling-forever.json'
// add others as created

export const tracks = [
  kettamaRolling,
]

export const trackById = Object.fromEntries(tracks.map(t => [t.id, t]))
```

**Step 3: Write remaining 4 seed tracks** (same structure, different artists/data)

**Step 4: Commit**

```bash
git add src/content/
git commit -m "feat: track data model + 5 seed tracks"
```

---

### Task 5: Track Library UI

**Files:**
- Modify: `src/pages/Library.jsx`
- Create: `src/components/TrackCard.jsx`
- Create: `src/pages/TrackDetail.jsx`

**Step 1: Write TrackCard component**

`src/components/TrackCard.jsx`:
```jsx
import { Link } from 'react-router-dom'

export default function TrackCard({ track }) {
  return (
    <Link to={`/library/${track.id}`} className="block p-4 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-600 transition-colors">
      <div className="flex justify-between items-start mb-2">
        <span className="text-xs font-mono text-zinc-500">{track.artist}</span>
        <span className="text-xs font-mono text-zinc-500">{track.bpm} BPM</span>
      </div>
      <h3 className="font-mono font-medium text-zinc-100 mb-1">{track.title}</h3>
      <div className="flex gap-3 text-xs font-mono text-zinc-400">
        <span>{track.key}</span>
        <span>swing {track.swing_pct}%</span>
        <span>{track.chords.slice(0, 2).join(' → ')}...</span>
      </div>
    </Link>
  )
}
```

**Step 2: Write Library page**

`src/pages/Library.jsx`:
```jsx
import { tracks } from '../content/tracks'
import TrackCard from '../components/TrackCard'

export default function Library() {
  return (
    <div>
      <h1 className="text-2xl font-mono font-bold mb-6">Track Library</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tracks.map(track => (
          <TrackCard key={track.id} track={track} />
        ))}
      </div>
    </div>
  )
}
```

**Step 3: Write TrackDetail page**

`src/pages/TrackDetail.jsx`:
```jsx
import { useParams, Link } from 'react-router-dom'
import { trackById } from '../content/tracks'

export default function TrackDetail() {
  const { id } = useParams()
  const track = trackById[id]

  if (!track) return <div className="text-zinc-500 font-mono">Track not found.</div>

  return (
    <div className="max-w-3xl">
      <Link to="/library" className="text-xs font-mono text-zinc-500 hover:text-zinc-300 mb-6 block">← Library</Link>
      <div className="flex gap-4 items-baseline mb-2">
        <span className="text-sm font-mono text-zinc-400">{track.artist}</span>
      </div>
      <h1 className="text-3xl font-mono font-bold mb-6">{track.title}</h1>

      <div className="grid grid-cols-4 gap-4 mb-8 p-4 bg-zinc-900 rounded-lg font-mono text-sm">
        <div><span className="text-zinc-500 block text-xs">BPM</span>{track.bpm}</div>
        <div><span className="text-zinc-500 block text-xs">KEY</span>{track.key}</div>
        <div><span className="text-zinc-500 block text-xs">SWING</span>{track.swing_pct}%</div>
        <div><span className="text-zinc-500 block text-xs">TIME</span>{track.time_sig}</div>
      </div>

      <section className="mb-8">
        <h2 className="text-sm font-mono text-zinc-500 uppercase tracking-wider mb-3">Structure</h2>
        <div className="flex gap-2 flex-wrap">
          {track.structure.map((s, i) => (
            <span key={i} className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-300">{s}</span>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-mono text-zinc-500 uppercase tracking-wider mb-3">Chord Progression</h2>
        <div className="flex gap-3 font-mono text-lg">
          {track.chords.map((c, i) => (
            <span key={i} className="px-3 py-2 bg-zinc-800 rounded text-zinc-100">{c}</span>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-mono text-zinc-500 uppercase tracking-wider mb-3">Theory Notes</h2>
        <p className="text-zinc-300 leading-relaxed">{track.theory_notes}</p>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-mono text-zinc-500 uppercase tracking-wider mb-3">Signature Elements</h2>
        <ul className="space-y-2">
          {track.signature_elements.map((el, i) => (
            <li key={i} className="text-zinc-300 text-sm flex gap-2">
              <span className="text-zinc-600">—</span>{el}
            </li>
          ))}
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-mono text-zinc-500 uppercase tracking-wider mb-3">Ableton Techniques</h2>
        <ul className="space-y-2">
          {track.ableton_techniques.map((t, i) => (
            <li key={i} className="text-zinc-300 text-sm flex gap-2">
              <span className="text-zinc-600">—</span>{t}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="text-sm font-mono text-zinc-500 uppercase tracking-wider mb-3">Splice Searches</h2>
        <div className="flex gap-2 flex-wrap">
          {track.splice_searches.map((s, i) => (
            <span key={i} className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-400">"{s}"</span>
          ))}
        </div>
      </section>
    </div>
  )
}
```

**Step 4: Add TrackDetail route to App.jsx**

```jsx
<Route path="/library/:id" element={<TrackDetail />} />
```

**Step 5: Verify**

```bash
npm run dev
```
Expected: Library page shows track cards, clicking a card shows full breakdown.

**Step 6: Commit**

```bash
git add src/
git commit -m "feat: track library UI with detail pages"
```

---

## Phase 3: Ableton Cheatsheet

### Task 6: Cheatsheet content + UI

**Files:**
- Create: `src/content/cheatsheet/index.js`
- Create: `src/content/cheatsheet/drum-rack.json`
- Create: `src/content/cheatsheet/eq-eight.json`
- Create: `src/content/cheatsheet/sidechain.json`
- Modify: `src/pages/Ableton.jsx`

**Step 1: Write cheatsheet entry schema**

Each entry:
```json
{
  "id": "sidechain-compression",
  "title": "Sidechain Compression",
  "category": "Effects",
  "tags": ["compression", "sidechain", "kick", "pump"],
  "summary": "Ducking your pads/bass in time with the kick for that pumping garage feel.",
  "steps": [
    "Add a Compressor to the pad/synth track you want to duck",
    "Click the headphone icon in the Compressor to enable sidechain",
    "Set the 'Audio From' dropdown to your kick track",
    "Set Ratio to 4:1, Attack to 0.1ms, Release to 100–200ms",
    "Adjust Threshold until the pad ducks noticeably on each kick hit"
  ],
  "tips": [
    "Longer release = slower pump, shorter = tighter duck",
    "For subtle glue, use 2:1 ratio. For obvious garage pump, use 8:1+"
  ],
  "ableton_version_note": "Works in Ableton Live 10+"
}
```

**Step 2: Write 3 seed cheatsheet entries** (sidechain, EQ Eight, Drum Rack)

**Step 3: Write cheatsheet index**

`src/content/cheatsheet/index.js`:
```js
import sidechain from './sidechain.json'
import eqEight from './eq-eight.json'
import drumRack from './drum-rack.json'

export const entries = [sidechain, eqEight, drumRack]
export const entryById = Object.fromEntries(entries.map(e => [e.id, e]))
```

**Step 4: Write Ableton page with search**

`src/pages/Ableton.jsx`:
```jsx
import { useState } from 'react'
import { entries } from '../content/cheatsheet'

export default function Ableton() {
  const [query, setQuery] = useState('')

  const filtered = entries.filter(e =>
    query === '' ||
    e.title.toLowerCase().includes(query.toLowerCase()) ||
    e.tags.some(t => t.includes(query.toLowerCase()))
  )

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-mono font-bold mb-6">Ableton Cheatsheet</h1>
      <input
        type="text"
        placeholder="Search — sidechain, EQ, drum rack..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        className="w-full px-4 py-2 bg-zinc-900 border border-zinc-700 rounded font-mono text-sm text-zinc-100 placeholder-zinc-600 mb-6 focus:outline-none focus:border-zinc-500"
      />
      <div className="space-y-6">
        {filtered.map(entry => (
          <div key={entry.id} className="p-5 bg-zinc-900 border border-zinc-800 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <h2 className="font-mono font-bold text-zinc-100">{entry.title}</h2>
              <span className="text-xs font-mono text-zinc-600">{entry.category}</span>
            </div>
            <p className="text-zinc-400 text-sm mb-4">{entry.summary}</p>
            <ol className="space-y-2">
              {entry.steps.map((step, i) => (
                <li key={i} className="text-zinc-300 text-sm flex gap-3">
                  <span className="text-zinc-600 font-mono min-w-[20px]">{i + 1}.</span>
                  {step}
                </li>
              ))}
            </ol>
            {entry.tips?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-zinc-800">
                {entry.tips.map((tip, i) => (
                  <p key={i} className="text-xs text-zinc-500 font-mono">→ {tip}</p>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Step 5: Verify**

```bash
npm run dev
```
Expected: Ableton page shows searchable entries, filtering works.

**Step 6: Commit**

```bash
git add src/content/cheatsheet/ src/pages/Ableton.jsx
git commit -m "feat: ableton cheatsheet with search"
```

---

## Phase 4: Theory Reference

### Task 7: Theory content + pages

**Files:**
- Create: `src/content/theory/scales.json`
- Create: `src/content/theory/chords.json`
- Create: `src/content/theory/rhythms.json`
- Create: `src/content/theory/index.js`
- Modify: `src/pages/Theory.jsx`

**Step 1: Write scales content (UK garage/house specific)**

`src/content/theory/scales.json`:
```json
[
  {
    "id": "natural-minor",
    "name": "Natural Minor",
    "aka": "Aeolian mode",
    "notes_from_root": [0, 2, 3, 5, 7, 8, 10],
    "feel": "Dark, emotive, melancholic — used constantly in UK garage",
    "examples": ["Kettama", "Interplanetary Criminal"],
    "common_keys": ["F minor", "G minor", "A minor"],
    "analytical_note": "Interval formula: W H W W H W W. The flattened 3rd, 6th, and 7th give the sadder quality vs major."
  },
  {
    "id": "dorian",
    "name": "Dorian Mode",
    "aka": "Natural minor with raised 6th",
    "notes_from_root": [0, 2, 3, 5, 7, 9, 10],
    "feel": "Minor but with a lift — jazzy, soulful. Used in deeper/soulful garage.",
    "examples": ["DJ Heartstring", "Soul Mass Transit System"],
    "common_keys": ["D dorian", "G dorian"],
    "analytical_note": "Like natural minor but the 6th is 1 semitone higher. Creates a less 'heavy' minor feel. Think of it as minor with brightness added."
  }
]
```

**Step 2: Write chords and rhythms content**

Similar structure — analytical framing, genre-specific examples, formulas.

**Step 3: Write Theory page**

Tabbed layout: Scales | Chords | Rhythms. Each tab renders its content with expandable entries.

**Step 4: Commit**

```bash
git add src/content/theory/ src/pages/Theory.jsx
git commit -m "feat: theory reference — scales, chords, rhythms"
```

---

## Phase 5: Guided Track Builder

### Task 8: Guided build data model + first build

**Files:**
- Create: `src/content/guided-builds/kettama-rolling-garage.json`
- Create: `src/content/guided-builds/index.js`

**Step 1: Write guided build schema**

```json
{
  "id": "kettama-rolling-garage",
  "title": "Rolling Garage House",
  "artist_style": "Kettama",
  "bpm": 130,
  "key": "F minor",
  "difficulty": "beginner",
  "estimated_time_mins": 90,
  "description": "Build a rolling, swung garage house track from scratch. You'll learn 2-step drum programming, chord voicings in the piano roll, sub bass layering, and sidechain compression.",
  "what_youll_learn": [
    "How to program a 2-step garage drum pattern",
    "How to draw Fmin7–Ebmaj7–Dbmaj7–Cm7 in the piano roll",
    "How to layer a sub bass with a mid bass",
    "How to set up sidechain compression for the pump",
    "How to apply groove pool swing"
  ],
  "reference_track_id": "kettama-rolling-forever",
  "steps": [
    {
      "id": 1,
      "title": "Set up your project",
      "category": "ableton",
      "instruction": "Open a new Ableton project. Set BPM to 130. Set time signature to 4/4. Save it as 'rolling-garage-130'.",
      "why": "130 BPM is the sweet spot for UK garage — fast enough to feel energetic, slow enough for the bass to breathe. 4/4 time means 4 beats per bar, which is the grid everything else locks to.",
      "ableton_cheatsheet_id": null,
      "splice_search": null,
      "tip": "Use Ctrl+S (Mac: Cmd+S) to save immediately. Ableton doesn't auto-save."
    },
    {
      "id": 2,
      "title": "Program the kick pattern",
      "category": "drums",
      "instruction": "Add a Drum Rack to a MIDI track. Load a punchy kick sample. In the piano roll, place kicks on beats 1 and 3 (positions 1.1, 1.3, 2.1, 2.3 etc) across a 2-bar loop.",
      "why": "4-on-the-floor means kick on every beat. This is the foundation of the rolling garage sound — it gives the track forward momentum. Beats 1 and 3 are 'strong' beats in 4/4.",
      "ableton_cheatsheet_id": "drum-rack-setup",
      "splice_search": "punchy garage kick 130bpm",
      "tip": "Keep velocity at 100–110 for the kick. Consistent velocity = consistent energy."
    },
    {
      "id": 3,
      "title": "Program the hi-hats",
      "category": "drums",
      "instruction": "Add an open hi-hat to beat 2 and beat 4 (off-beats). Add a closed hi-hat on every 8th note (8 per bar). Apply the 'Swing 54%' groove from the Groove Pool to the MIDI clip.",
      "why": "The open hat on 2 and 4 is the signature 2-step feel. The closed hats fill in the gaps. The 54% swing delays every second 8th note slightly — this is what makes garage feel 'bouncy' rather than rigid. Analytically: swing % controls how much the even 8th notes shift toward the next beat.",
      "ableton_cheatsheet_id": "groove-pool-swing",
      "splice_search": "swung open hi-hat garage",
      "tip": "Groove Pool is in the browser panel (B key). Drag 'Swing 54%' directly onto the clip."
    }
  ]
}
```

**Step 2: Write remaining 8-12 steps** (chord programming, bass, sidechain, automation, arrangement, mixdown basics)

**Step 3: Write guided builds index**

`src/content/guided-builds/index.js`:
```js
import kettamaRolling from './kettama-rolling-garage.json'

export const builds = [kettamaRolling]
export const buildById = Object.fromEntries(builds.map(b => [b.id, b]))
```

**Step 4: Commit**

```bash
git add src/content/guided-builds/
git commit -m "feat: guided build data model + Kettama rolling garage build"
```

---

### Task 9: Guided Track Builder UI

**Files:**
- Modify: `src/pages/Builder.jsx`
- Create: `src/components/BuildSelector.jsx`
- Create: `src/components/BuildStep.jsx`
- Create: `src/components/ReferencePanel.jsx`

**Step 1: Write BuildSelector**

`src/components/BuildSelector.jsx`:
```jsx
import { builds } from '../content/guided-builds'

export default function BuildSelector({ onSelect }) {
  return (
    <div>
      <h1 className="text-2xl font-mono font-bold mb-2">Guided Track Builder</h1>
      <p className="text-zinc-400 text-sm mb-8">Pick a style. Build a track. Learn as you go.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {builds.map(build => (
          <button
            key={build.id}
            onClick={() => onSelect(build)}
            className="text-left p-5 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-600 transition-colors"
          >
            <span className="text-xs font-mono text-zinc-500 block mb-1">{build.artist_style} style</span>
            <h3 className="font-mono font-bold text-zinc-100 mb-2">{build.title}</h3>
            <div className="flex gap-3 text-xs font-mono text-zinc-500 mb-3">
              <span>{build.bpm} BPM</span>
              <span>{build.key}</span>
              <span>~{build.estimated_time_mins}min</span>
            </div>
            <ul className="space-y-1">
              {build.what_youll_learn.slice(0, 3).map((item, i) => (
                <li key={i} className="text-xs text-zinc-400 flex gap-2">
                  <span className="text-zinc-600">→</span>{item}
                </li>
              ))}
            </ul>
          </button>
        ))}
      </div>
    </div>
  )
}
```

**Step 2: Write BuildStep component**

`src/components/BuildStep.jsx`:
```jsx
export default function BuildStep({ step, stepNumber, total, onNext, onPrev, onOpenRef }) {
  return (
    <div className="max-w-2xl">
      <div className="flex justify-between items-center mb-6">
        <span className="text-xs font-mono text-zinc-500">Step {stepNumber} of {total}</span>
        <span className="text-xs font-mono text-zinc-600 uppercase">{step.category}</span>
      </div>

      <h2 className="text-xl font-mono font-bold mb-4">{step.title}</h2>

      <div className="p-5 bg-zinc-900 border border-zinc-700 rounded-lg mb-6">
        <p className="text-zinc-200 leading-relaxed">{step.instruction}</p>
      </div>

      <div className="mb-6">
        <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-2">Why this works</h3>
        <p className="text-zinc-400 text-sm leading-relaxed">{step.why}</p>
      </div>

      {step.tip && (
        <div className="px-4 py-3 bg-zinc-900 border-l-2 border-zinc-600 rounded mb-6">
          <p className="text-xs font-mono text-zinc-400">→ {step.tip}</p>
        </div>
      )}

      {step.splice_search && (
        <div className="mb-6">
          <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-2">Splice Search</h3>
          <span className="font-mono text-sm text-zinc-300 bg-zinc-900 px-3 py-1 rounded">"{step.splice_search}"</span>
        </div>
      )}

      {step.ableton_cheatsheet_id && (
        <button
          onClick={() => onOpenRef(step.ableton_cheatsheet_id)}
          className="text-xs font-mono text-zinc-400 hover:text-zinc-200 border border-zinc-700 hover:border-zinc-500 px-3 py-2 rounded mb-6 block transition-colors"
        >
          → Open Ableton reference: {step.ableton_cheatsheet_id}
        </button>
      )}

      <div className="flex gap-3 mt-8">
        {stepNumber > 1 && (
          <button onClick={onPrev} className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded font-mono text-sm transition-colors">
            ← Back
          </button>
        )}
        <button onClick={onNext} className="px-6 py-2 bg-zinc-100 text-zinc-900 hover:bg-white rounded font-mono text-sm font-bold transition-colors">
          {stepNumber === total ? 'Finish' : 'Next step →'}
        </button>
      </div>
    </div>
  )
}
```

**Step 3: Write Builder page**

`src/pages/Builder.jsx`:
```jsx
import { useState } from 'react'
import BuildSelector from '../components/BuildSelector'
import BuildStep from '../components/BuildStep'
import { entryById } from '../content/cheatsheet'

export default function Builder() {
  const [build, setBuild] = useState(null)
  const [stepIndex, setStepIndex] = useState(0)
  const [refEntry, setRefEntry] = useState(null)

  if (!build) return <BuildSelector onSelect={b => { setBuild(b); setStepIndex(0) }} />

  const step = build.steps[stepIndex]

  return (
    <div className="flex gap-8">
      <div className="flex-1">
        <button onClick={() => setBuild(null)} className="text-xs font-mono text-zinc-500 hover:text-zinc-300 mb-6 block">
          ← {build.title}
        </button>
        <BuildStep
          step={step}
          stepNumber={stepIndex + 1}
          total={build.steps.length}
          onNext={() => setStepIndex(i => Math.min(i + 1, build.steps.length - 1))}
          onPrev={() => setStepIndex(i => Math.max(i - 1, 0))}
          onOpenRef={id => setRefEntry(entryById[id] || null)}
        />
      </div>

      {refEntry && (
        <div className="w-80 shrink-0 p-5 bg-zinc-900 border border-zinc-800 rounded-lg h-fit sticky top-8">
          <div className="flex justify-between items-start mb-3">
            <h3 className="font-mono font-bold text-zinc-100 text-sm">{refEntry.title}</h3>
            <button onClick={() => setRefEntry(null)} className="text-zinc-600 hover:text-zinc-400 font-mono">×</button>
          </div>
          <ol className="space-y-2">
            {refEntry.steps.map((s, i) => (
              <li key={i} className="text-zinc-300 text-xs flex gap-2">
                <span className="text-zinc-600 min-w-[16px]">{i + 1}.</span>{s}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  )
}
```

**Step 4: Verify end-to-end**

```bash
npm run dev
```
Expected: Builder shows style selector → click → steps through instructions → reference panel slides in when Ableton ref available.

**Step 5: Commit**

```bash
git add src/
git commit -m "feat: guided track builder UI with reference panel"
```

---

## Phase 6: Deploy

### Task 10: Deploy to Cloudflare Pages

**Step 1: Build**

```bash
npm run build
```

**Step 2: Deploy via Wrangler or connect GitHub**

Option A (Wrangler):
```bash
npx wrangler pages deploy dist --project-name music-theory-learner
```

Option B (GitHub integration — recommended):
- Go to Cloudflare Dashboard → Pages → Connect to Git
- Select `PatrickAllen1/music-theory-learner`
- Build command: `npm run build`
- Output directory: `dist`
- Deploy

**Step 3: Push all commits**

```bash
git push origin main
```

---

## Content Backlog (post-scaffold)

Once the app is built, fill it with Claude-authored content:

- [ ] 5 guided builds (one per artist style)
- [ ] 30 track breakdowns
- [ ] 10+ cheatsheet entries (all effects, MIDI, instruments)
- [ ] Theory reference (scales, chords, rhythms fully populated)
- [ ] Guided build: Interplanetary Criminal bassline style
- [ ] Guided build: Sammy Virji breaks garage style
- [ ] Guided build: TS7 piano house style
- [ ] Guided build: DJ Heartstring deep garage style
