# Serum Sound Intelligence Roadmap

This roadmap shifts the Serum work from narrow VST2 slot archaeology toward a
practical system for understanding, cataloging, and using Serum sounds in song
production.

The end goal is:

- understand what each sound is doing
- understand how it is built
- understand how it will likely sit in a mix
- retrieve and combine sounds intentionally when building tracks

## Scope

We will support two source lanes:

- `Serum 2 / VST3 / ALS state` as the primary structured source of truth
- `Serum 1 / VST2 / .fxp` as a legacy-compatibility lane for older banks and
  purchased S1 presets living inside the Serum 2 compatibility folders

The current VST2 work remains useful, but it is no longer the main product. The
main product is a normalized preset profile and, later, an audio-linked preset
catalog.

## Target Artifacts

Immediate artifacts:

- [schemas/serum-preset-profile.schema.json](./schemas/serum-preset-profile.schema.json)
- [build_serum_profile.py](./build_serum_profile.py)

Planned artifacts:

- `als/catalog/` normalized profile outputs
- `als/render_serum_audio.py` controlled audio audition renderer
- `als/extract_serum_audio_features.py` objective audio descriptors
- `als/tag_serum_profiles.py` semantic role/tone tagging
- `als/search_serum_profiles.py` role/tone/mix-aware retrieval
- `als/palette_builder.py` preset pairing and palette suggestions

## Phase 1: Canonical Profile

Goal:

- define one profile format that can represent both Serum 2 named-state extracts
  and legacy VST2-derived compatibility data

Deliverables:

- JSON schema for `serum-preset-profile`
- first builder that converts existing `als/analysis/*-serum.json` files into
  normalized profile objects

Files:

- add `als/schemas/serum-preset-profile.schema.json`
- add `als/build_serum_profile.py`

Acceptance criteria:

- profile schema is versioned
- one CLI can emit normalized profiles from existing ALS analysis JSON
- output contains `source`, `classification`, `summary`, `synthesis`,
  `audio_reference`, and `confidence`

## Phase 2: Serum 2 First-Class Extraction

Goal:

- make named Serum 2 state the primary analysis path

Deliverables:

- extend [parse_serum.py](./parse_serum.py) output adapters so VST3 state maps
  cleanly into the profile schema
- preserve legacy `.fxp` support as a compatibility adapter, not the center of
  the system

Files:

- extend `als/parse_serum.py`
- extend `als/build_serum_profile.py`

Acceptance criteria:

- profile builder can ingest fresh Serum 2 ALS extracts directly
- we stop depending on ad hoc per-song JSON shapes for downstream tooling

## Phase 3: Golden Preset Set

Goal:

- create a small verified preset corpus before trying to catalog everything

Deliverables:

- `25-50` curated Garage / Speed Garage presets
- canonical captured states
- normalized profile JSON for each captured preset

Recommended folders:

- `als/catalog/golden/`
- `als/catalog/golden/audio/`

Acceptance criteria:

- every golden preset has a stable profile ID
- every golden preset has a normalized profile
- role/tone guesses are reviewed against actual listening

## Phase 4: Audio Reference Layer

Goal:

- add the missing audible truth layer so sound understanding is not purely
  parameter-based

Deliverables:

- standard audition renders per preset:
  - sustained root note
  - short stab
  - minor chord stab
  - short riff
  - optional macro sweep
- extracted descriptors such as:
  - RMS / crest
  - spectral centroid
  - stereo width proxy
  - decay length
  - transient sharpness

Files:

- add `als/render_serum_audio.py`
- add `als/extract_serum_audio_features.py`

Acceptance criteria:

- every golden preset has at least one reference render
- every render has machine-readable descriptor JSON

## Phase 5: Semantic Sound Intelligence

Goal:

- turn raw parameters plus audio descriptors into usable musical knowledge

Deliverables:

- role tags: `sub`, `reese`, `pad`, `lead`, `pluck`, `stab`, `fx`
- tone tags: `dark`, `bright`, `clean`, `gritty`, `wide`, `narrow`, `soft`,
  `hard`, `hollow`, `dense`
- mix hints: `low_end_anchor`, `mid_focus`, `high_air`, `mono_safe`,
  `side_heavy`, `transient_forward`, `background`
- preset similarity and clash hints

Files:

- add `als/tag_serum_profiles.py`
- add `als/search_serum_profiles.py`

Acceptance criteria:

- profile search can answer role/tone questions
- profile comparisons can answer pairing questions

## Phase 6: Song-Building Integration

Goal:

- use the preset intelligence layer to help build better tracks and lessons

Deliverables:

- palette suggestions for a reference track or brief
- conflict detection for bass/pad/lead combinations
- lesson metadata that explains why each preset was chosen

Files:

- add `als/palette_builder.py`
- integrate chosen outputs into lesson/content tooling later

Acceptance criteria:

- given a target mood and role list, the system can return a coherent preset
  palette
- lesson content can cite concrete sonic reasons, not only preset names

## Manual vs Automatable Work

Automatable now:

- schema definition
- state parsing
- profile normalization
- cross-run reporting
- tag generation
- search and retrieval

Manual or host-dependent:

- opening a preset in the real Serum plugin
- saving canonical captures from the plugin or host
- rendering audio unless we automate the DAW/plugin session

Important distinction:

- old `.fxp` reverse-engineering is still useful for legacy compatibility
- the practical path to sound understanding is `named Serum 2 state + audio`

## Near-Term Implementation Order

1. Land the schema and first profile builder.
2. Validate the profile shape against existing `als/analysis/*-serum.json`.
3. Choose a small golden preset set from the Garage banks.
4. Add a reproducible audio-render workflow.
5. Add semantic tagging and retrieval.

## Immediate Next Files

Already added in this pass:

- [schemas/serum-preset-profile.schema.json](./schemas/serum-preset-profile.schema.json)
- [build_serum_profile.py](./build_serum_profile.py)

Recommended next code pass:

- extend `build_serum_profile.py` to ingest fresh Serum 2 ALS captures directly
- add `als/catalog/` output support
- add a small checked-in golden profile fixture for regression testing
