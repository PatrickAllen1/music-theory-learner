# Music Theory Learner — Design Document

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** A personal, static web app that teaches music theory, production, and Ableton through guided track creation — built specifically around UK garage, bassline, and house music.

**Architecture:** Static site (React + Vite) deployed to Cloudflare Pages. All content lives as static JSON/Markdown files committed to the repo — no backend, no database, no auth. The Guided Track Builder is the core feature; the Track Library, Theory Reference, and Ableton Cheatsheet all feed into it contextually.

**Tech Stack:** React, Vite, Tailwind CSS, React Router, Web Audio API, Cloudflare Pages, static JSON + Markdown content

---

## User

Analytical background (data science, poker, DFS). No music theory knowledge. Knows a little Ableton. Wants to make tracks like: Kettama, Interplanetary Criminal, Sammy Virji, TS7, DJ Heartstring, Soul Mass Transit System. Learns by doing, not by reading lessons in isolation. Has Splice.

---

## The Four Sections

### 1. Guided Track Builder (primary)

The north star feature. User picks a style/artist, the app walks them through building a complete track step by step. Theory and Ableton skills are introduced exactly when needed — not before. Each step contains:

- What to do in Ableton (exact instruction)
- Why it works (theory concept, one paragraph)
- What it should sound like (reference track + timestamp)
- Suggested Splice search if a sample is needed
- Link to relevant Ableton Cheatsheet entry

Guided builds are pre-authored static JSON/Markdown files. Claude authors them using deep knowledge of UK garage production. User reviews and refines with Claude, then content is committed to repo.

**Initial guided builds to create:**
- Kettama-style rolling garage house (130 BPM, swung, Fmin)
- Interplanetary Criminal-style bassline house (138 BPM, driving)
- Sammy Virji-style breaks-influenced garage
- TS7-style piano house
- DJ Heartstring-style deep/soulful garage

### 2. Track Library

30–50 curated track breakdowns. One JSON file per track. Each breakdown is a teaching document, not just metadata:

```json
{
  "id": "kettama-rolling-forever",
  "title": "Track Title",
  "artist": "Kettama",
  "bpm": 130,
  "key": "F minor",
  "scale": "natural minor",
  "swing_pct": 54,
  "time_sig": "4/4",
  "structure": ["intro", "build", "drop1", "breakdown", "drop2", "outro"],
  "chords": ["Fmin7", "Ebmaj7", "Dbmaj7", "Cm7"],
  "signature_elements": ["rolling garage kick", "pitched vocal chop", "sub bass octave jump"],
  "ableton_techniques": ["swing via groove pool", "sidechain compression", "clip automation"],
  "theory_notes": "Extended explanation of why these chords work, the emotional arc, the rhythmic feel.",
  "splice_searches": ["punchy 130 garage kick", "pitched vocal one shot"],
  "guided_build_id": "kettama-rolling-garage"
}
```

### 3. Theory Reference

UK garage/house specific. Framed analytically — patterns, formulas, structures. Not generic music theory.

**Sections:**
- Keys & scales used in the genre (minor pentatonic, natural minor, dorian)
- Chord voicings (7ths, 9ths — exactly which notes, which octave, which inversion)
- Rhythm patterns (2-step, 4x4, swing math — what 54% swing means numerically)
- Bassline formulas (root–octave jump, walking bass, subs)
- Song structure templates per sub-genre

### 4. Ableton Cheatsheet

A searchable production encyclopedia. Entries unlock contextually when hit in the Guided Builder, but also browsable directly.

**Categories:**
- MIDI & Piano Roll (notes, velocity, quantize, drawing chords)
- Drum Rack (setup, loading samples, mapping, swing)
- Effects: EQ Eight, EQ Three, Compressor, Reverb, Delay
- Sidechain compression (step-by-step)
- Samples & Splice (auditioning, importing, chopping in Simpler)
- Project setup (BPM, time sig, groove pool, track routing)
- Automation (clip vs arrangement, drawing envelopes)
- Stock instruments (Operator, Drift, Wavetable, Simpler — when to use each)

---

## UI Layout

```
┌─────────────────────────────────────────────────────┐
│  music-theory-learner          [Builder] [Library]  │
│                                [Theory] [Ableton]   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Main content area]          [Reference panel]     │
│                               (slides in from right │
│  Step-by-step guide           when contextual ref   │
│  or track breakdown           is available)         │
│  or reference content                               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

Dark theme. Monospace accents for BPM/key/chord data. Clean, no clutter.

---

## Content Pipeline

1. User names an artist/style
2. Claude writes full guided build (step-by-step JSON/Markdown)
3. Review together, refine
4. Commit to `src/content/guided-builds/`
5. App renders it automatically

Track breakdowns follow the same pipeline — Claude writes, user reviews, committed to `src/content/tracks/`.

---

## What This Is NOT

- Not a generic music theory course
- Not a multi-user product (no auth, no accounts)
- Not AI-powered at runtime (no Claude API calls in the app)
- Not a DAW or MIDI editor
- Not auto-analyzing audio files

---

## Phase Breakdown

| Phase | What gets built |
|-------|----------------|
| 1 | Project scaffold — Vite + React + Tailwind + Cloudflare config + routing |
| 2 | Track Library — data model, UI, 5 seed tracks |
| 3 | Ableton Cheatsheet — content structure, searchable UI |
| 4 | Theory Reference — content + pages |
| 5 | Guided Track Builder — step UI + contextual panel + first guided build |
| 6 | Content population — all guided builds, full track library |
