# Serum Sound Intelligence Roadmap

This roadmap shifts the Serum work from narrow VST2 slot archaeology toward a
practical system for understanding, cataloging, and using Serum sounds in
full-song production and guided-build authoring.

The end goal is:

- understand what each sound is doing
- understand how it is built
- understand how it will likely sit in a mix
- retrieve and combine sounds intentionally when building tracks
- author full-quality UK garage songs with intentional sound choices
- transform those finished song decisions into guided-build lesson steps

## Scope

We will support two source lanes:

- `Serum 2 / VST3 / ALS state` as the primary structured source of truth
- `Serum 1 / VST2 / .fxp` as a legacy-compatibility lane for older banks and
  purchased S1 presets living inside the Serum 2 compatibility folders

The current VST2 work remains useful, but it is no longer the main product. The
main product is:

- a normalized preset profile and audio-linked preset catalog
- a song-authoring layer that uses those presets to build coherent, release-
  shaped tracks
- a lesson-compilation layer that converts finished track decisions into
  guided-build content

## Target Artifacts

Immediate artifacts:

- [schemas/serum-preset-profile.schema.json](./schemas/serum-preset-profile.schema.json)
- [build_serum_profile.py](./build_serum_profile.py)

Planned artifacts:

- `als/catalog/` normalized profile outputs
- `als/prepare_serum_audio_session.py` repeatable manual render-session prep
- `als/render_serum_audio.py` controlled audio audition renderer
- `als/extract_serum_audio_features.py` objective audio descriptors
- `als/serum_mutation_rules.py` reusable parameter-mutation heuristics
- `als/suggest_serum_mutations.py` profile-aware change suggestions
- `als/tag_serum_profiles.py` semantic role/tone tagging
- `als/search_serum_profiles.py` role/tone/mix-aware retrieval
- `als/palette_builder.py` preset pairing and palette suggestions
- `als/design_serum_track_blueprint.py` song-level synth stack planning
- `als/prepare_serum_lesson_author_bundle.py` brief-specific lesson authoring
  bundle
- `als/generate_serum_guided_build_synth_plan.py` per-part synth authoring
  scaffold
- `als/generate_serum_guided_build_steps.py` guided-build-style synth step
  scaffolds
- `als/design_full_song_blueprint.py` complete track blueprint for drums,
  harmony, melody, arrangement, FX, mix, and export
- `als/song-production-templates.json` per-layer Ableton chain templates,
  return/send architecture, and sample-slot definitions
- `als/compile_guided_build_lesson.py` conversion from full song blueprint to
  lesson JSON

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

- add `als/serum-audio-audition-spec.json`
- add `als/prepare_serum_audio_session.py`
- add `als/render_serum_audio.py`
- add `als/extract_serum_audio_features.py`
- add `als/attach_serum_audio_descriptors.py`

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

- add `als/serum_mutation_rules.py`
- add `als/suggest_serum_mutations.py`
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

## Phase 7: Full-Song Blueprint Authoring

Goal:

- move from “good synth choices” to “good full songs” by freezing the entire
  production plan before writing lessons

Deliverables:

- a reusable full-song blueprint format that captures:
  - drum sample choices and exact groove logic
  - reserved sample slots for:
    - kick / clap / snare / hat / shaker / percussion
    - drum-loop layers
    - vocal chops or vocal-space placeholders
    - transitions, uplifters, downlifters, impacts, and atmospheres
  - bass/chord/melody roles and synth assignments
  - harmonic plan
  - arrangement sections and section goals
  - per-layer processing plans for:
    - drums
    - bass and sub
    - pad / chord layers
    - pluck / lead / stab layers
    - FX layers
  - send/return architecture:
    - reverb returns
    - delay throws
    - parallel saturation / compression when needed
  - section-aware automation rules:
    - send lifts
    - filter openings
    - reverb/delay throws
    - arrangement mutes and drop-entry resets
  - mix-space rules and reserved spaces for later samples or vocal additions
  - export expectations
- brief-driven helpers that can output release-shaped UKG song plans instead of
  isolated synth suggestions

Files:

- add `als/design_full_song_blueprint.py`
- add `als/song-blueprint-briefs.json`
- add `als/song-production-templates.json`
- add `als/compare_full_song_blueprints.py`

Acceptance criteria:

- given a target brief, the system can output a complete production blueprint,
  not only synth part selections
- the blueprint is detailed enough that a human could build the same finished
  song from it
- the blueprint reads like a song plan first and a teaching aid second
- the blueprint includes enough production detail that every major layer has:
  - a defined sound source
  - a processing path
  - an arrangement role
  - a reserved space for any still-unfilled sample or vocal layer

## Phase 8: Guided-Lesson Compilation

Goal:

- convert a finished song blueprint into guided-build lesson content without
  losing production quality

Deliverables:

- a compiler that turns a full-song blueprint into:
  - guided-build-style `steps[]`
  - lesson metadata
  - rationale for each section and sound choice
  - exact production steps for:
    - loading samples
    - loading synths
    - applying Ableton devices
    - routing to returns
    - automating transitions and drop entries
    - staging mix and export passes
- structured rules for converting:
  - production decisions -> learner instructions
  - arrangement sections -> lesson sequencing
  - mix/export choices -> exact final steps
  - sample-slot placeholders -> explicit “leave this lane open for later fill”
    instructions when the song plan intentionally reserves space

Files:

- add `als/compile_guided_build_lesson.py`
- add `als/validate_guided_build_lesson.py`

Acceptance criteria:

- the compiled lesson preserves the full song’s quality and intent
- the lesson remains fully hand-held and pre-composed
- resulting JSON is close enough to existing `src/content/guided-builds/originals/*.json`
  that only light editorial cleanup is needed
- the compiled lesson includes production steps for effects, routing, and
  sample-space management, not only note writing and synth choice

## Phase 9: Quality Gate And Audio Verification

Goal:

- stop the system from producing “educational but weak” songs

Deliverables:

- a quality gate that checks:
  - release-shaped arrangement
  - no unresolved key sound roles
  - no major fallback-heavy synth parts left unreviewed
  - no unplanned empty sample lanes
  - no undefined layer processing on core parts
  - mix/export scaffolding present
- audio-verification workflow for the highest-impact synth parts and blueprint
  choices

Files:

- add `als/report_full_song_blueprint_readiness.py`
- extend `als/prepare_serum_render_handoff.py`
- extend `als/prepare_serum_lesson_author_bundle.py`

Acceptance criteria:

- the system can tell the difference between “teachable loop” and “finished
  song plan”
- top lesson candidates are prioritized by song quality, not just synth
  coverage
- render/audio verification is attached to the song-authoring loop, not treated
  as a separate afterthought
- a blueprint cannot pass as “ready” if it still lacks core sample placement
  decisions or effect-chain decisions for important layers

## Manual vs Automatable Work

Automatable now:

- schema definition
- state parsing
- profile normalization
- cross-run reporting
- tag generation
- search and retrieval
- song-blueprint generation from briefs
- layer-by-layer production templating
- lesson-step scaffolding from frozen song decisions

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
6. Build full-song blueprints on top of the sound-intelligence layer.
7. Add per-layer production templates and sample-slot planning to those
   blueprints.
8. Compile those blueprints into guided-build lesson JSON.
9. Add quality gates so “full-quality song first” remains the rule.

## Immediate Next Files

Already added in this pass:

- [schemas/serum-preset-profile.schema.json](./schemas/serum-preset-profile.schema.json)
- [build_serum_profile.py](./build_serum_profile.py)
- [search_serum_profiles.py](./search_serum_profiles.py)
- [serum_mutation_rules.py](./serum_mutation_rules.py)
- [suggest_serum_mutations.py](./suggest_serum_mutations.py)
- [serum-audio-audition-spec.json](./serum-audio-audition-spec.json)
- [prepare_serum_audio_session.py](./prepare_serum_audio_session.py)
- [extract_serum_audio_features.py](./extract_serum_audio_features.py)
- [attach_serum_audio_descriptors.py](./attach_serum_audio_descriptors.py)
- [palette_builder.py](./palette_builder.py)

Recommended next code pass:

- extend `build_serum_profile.py` to ingest fresh Serum 2 ALS captures directly
- add audio descriptor extraction on top of prepared audio sessions
- tighten semantic tagging so fewer profiles remain `unknown`
- add the full-song blueprint layer so the system can author whole tracks, not
  only synth sections
- add explicit Ableton production templates so every core layer has device-chain
  guidance and every song leaves intentional room for sample-based layers
- add the lesson compiler layer so finished song decisions can be turned into
  guided-build JSON
