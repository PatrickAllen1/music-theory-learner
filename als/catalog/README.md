# Serum Profile Catalog

This folder is the beginning of the Serum sound-intelligence catalog.

Current subfolders:

- `golden/`:
  small checked-in profile fixtures used as stable regression targets while the
  schema and builder are still evolving

Planned subfolders:

- `profiles/`:
  generated normalized profile outputs for the full local Serum analysis corpus
- `audio/`:
  audition renders and extracted audio descriptors

Build a generated profile catalog from the existing ALS analysis set:

```bash
python3 als/build_serum_profile.py \
  --analysis-dir als/analysis \
  --catalog-dir als/catalog/profiles \
  --index-out als/catalog/index.json
```

Search the generated profile catalog:

```bash
python3 als/search_serum_profiles.py --role bass
python3 als/search_serum_profiles.py --role lead --tone bright
python3 als/search_serum_profiles.py --dest-module VoiceFilter
python3 als/search_serum_profiles.py --rendered-only --max-attack-ms 30
python3 als/search_serum_profiles.py --rendered-only --min-side-ratio 0.4 --max-centroid-hz 1200
```

Suggest targeted parameter moves for a profile:

```bash
python3 als/suggest_serum_mutations.py --list-goals
python3 als/suggest_serum_mutations.py --profile-id mph-raw:bass:i1 --goal darker
python3 als/suggest_serum_mutations.py --profile-id mph-raw:bass:i1 --goal tighter --goal mono_safer
```

Recommend a preset for a musical part and bundle the mutation suggestions:

```bash
python3 als/recommend_serum_part.py --role bass --goal darker --goal mono_safer
python3 als/recommend_serum_part.py --role lead --tone bright --prefer-rendered --goal tighter --goal more_presence
```

Build a whole Serum stack from a reusable UKG brief:

```bash
python3 als/design_serum_track_blueprint.py --brief ukg-4x4-pluck-driver
python3 als/design_serum_track_blueprint.py --brief ukg-4x4-lead-driver --prefer-rendered --format json
```

Suggest better replacements for one weak part inside a blueprint:

```bash
python3 als/suggest_serum_blueprint_alternatives.py --brief ukg-2step-dark-stab --part-id secondary-reese
python3 als/suggest_serum_blueprint_alternatives.py --brief ukg-4x4-pluck-driver --part-id hook-pluck --format json
```

Refine a blueprint automatically by swapping conflict-heavy or fallback-heavy parts:

```bash
python3 als/refine_serum_track_blueprint.py --brief ukg-4x4-pluck-driver
python3 als/refine_serum_track_blueprint.py --brief ukg-2step-dark-stab --prefer-rendered --format json
```

Generate a blueprint-level mutation plan that combines part goals with
pairwise conflict fixes:

```bash
python3 als/suggest_serum_blueprint_mutations.py --brief ukg-2step-dark-stab
python3 als/suggest_serum_blueprint_mutations.py --brief ukg-4x4-pluck-driver --refine --format json
```

Prepare an audio render session directly from the chosen blueprint stack:

```bash
python3 als/prepare_serum_blueprint_audio_session.py --brief ukg-4x4-lead-driver --out-dir als/audio-session/ukg-4x4-lead-driver
python3 als/prepare_serum_blueprint_audio_session.py --brief ukg-4x4-pluck-driver --refine --out-dir als/audio-session/ukg-4x4-pluck-driver
```

Generate lesson-facing notes from the chosen blueprint:

```bash
python3 als/generate_serum_lesson_notes.py --brief ukg-4x4-pluck-driver
python3 als/generate_serum_lesson_notes.py --brief ukg-4x4-lead-driver --format json
python3 als/generate_serum_lesson_notes.py --brief ukg-2step-dark-stab --refine --format json
```

Generate a guided-build synth scaffold from the refined brief:

```bash
python3 als/generate_serum_guided_build_synth_plan.py --brief ukg-2step-dark-stab
python3 als/generate_serum_guided_build_synth_plan.py --brief ukg-4x4-pluck-driver --format json
```

Generate draft guided-build step objects for the synth section:

```bash
python3 als/generate_serum_guided_build_steps.py --brief ukg-2step-dark-stab
python3 als/generate_serum_guided_build_steps.py --brief ukg-4x4-pluck-driver --format json
```

Generate a full-song production blueprint that wraps the refined synth stack
with arrangement, sample slots, processing chains, returns, and export rules:

```bash
python3 als/design_full_song_blueprint.py --brief ukg-2step-dark-stab
python3 als/design_full_song_blueprint.py --brief ukg-4x4-pluck-driver --format json
```

Build a model-facing song decision tree from that blueprint:

```bash
python3 als/build_song_decision_tree.py --brief ukg-2step-dark-stab
python3 als/build_song_decision_tree.py --brief ukg-4x4-lead-driver --format json
```

Turn the frozen song stance into actual bass, harmony, hook, and section-writing decisions:

```bash
python3 als/build_song_composition_pass.py --brief ukg-140-og-bounce-driver
python3 als/build_song_composition_pass.py --brief ukg-140-og-bounce-driver --format json
```

Turn that composition pass into exact part-level MIDI variants and section assignments:

```bash
python3 als/build_song_midi_plan.py --brief ukg-140-og-bounce-driver
python3 als/build_song_midi_plan.py --brief ukg-140-og-bounce-driver --format json
```

Recommend transcript-derived production techniques for a brief:

```bash
python3 als/recommend_production_techniques.py --brief ukg-2step-dark-stab
python3 als/recommend_production_techniques.py --brief ukg-4x4-pluck-driver --format json
```

Compare two full-song blueprints before turning either one into a lesson:

```bash
python3 als/compare_full_song_blueprints.py --left-brief ukg-2step-dark-stab --right-brief ukg-4x4-pluck-driver
```

Compile a full-song blueprint into a guided-build lesson draft:

```bash
python3 als/compile_guided_build_lesson.py --brief ukg-2step-dark-stab
python3 als/compile_guided_build_lesson.py --brief ukg-4x4-pluck-driver --lesson-only --format json
```

Validate whether a compiled lesson is still a scaffold or close to app-ready:

```bash
python3 als/validate_guided_build_lesson.py --brief ukg-2step-dark-stab
python3 als/validate_guided_build_lesson.py --lesson-json path/to/lesson.json --format json
```

Report which song briefs are actually closest to full guided-build authoring:

```bash
python3 als/report_full_song_blueprint_readiness.py
python3 als/report_full_song_blueprint_readiness.py --format json
```

Export the whole lesson packet in one shot:

```bash
python3 als/export_serum_lesson_packet.py --brief ukg-4x4-pluck-driver --out-dir als/lesson-packets/ukg-4x4-pluck-driver
python3 als/export_serum_lesson_packet.py --brief ukg-4x4-pluck-driver --refine --out-dir als/lesson-packets/ukg-4x4-pluck-driver
```

The lesson packet now includes:

- `blueprint.json` / `blueprint.md`
- `lesson-notes.json` / `lesson-notes.md`
- `mutation-plan.json` / `mutation-plan.md`
- `audio-session/`

Report how well the current catalog covers all briefs and which profiles to render first:

```bash
python3 als/report_serum_brief_coverage.py
python3 als/report_serum_brief_coverage.py --format json
```

Report whether each brief is actually ready for lesson-packet export after
refinement and mutation planning:

```bash
python3 als/report_serum_packet_readiness.py
python3 als/report_serum_packet_readiness.py --format json
```

Rank which non-rendered profiles should be rendered next based on packet
readiness pressure, fallback pressure, and conflict participation:

```bash
python3 als/report_serum_render_backlog.py
python3 als/report_serum_render_backlog.py --format json
```

Report which sound targets are still underserved by the current catalog:

```bash
python3 als/report_serum_catalog_gaps.py
python3 als/report_serum_catalog_gaps.py --format json
```

Recommend actual S1 Garage preset files to capture next for those gaps:

```bash
python3 als/report_serum_preset_capture_candidates.py
python3 als/report_serum_preset_capture_candidates.py --format json
```

Prepare a capture-session queue from that preset shortlist:

```bash
python3 als/prepare_serum_preset_capture_session.py --out-dir als/preset-capture-session
```

Rank which briefs are strongest candidates for actual lesson authoring:

```bash
python3 als/report_serum_lesson_author_queue.py
python3 als/report_serum_lesson_author_queue.py --format json
```

Recommend real Garage/Speed Garage bank presets for one weak brief:

```bash
python3 als/report_serum_brief_bank_candidates.py --brief ukg-2step-dark-stab
python3 als/report_serum_brief_bank_candidates.py --brief ukg-4x4-pluck-driver --format json
```

Prepare one author-ready bundle for a specific brief:

```bash
python3 als/prepare_serum_lesson_author_bundle.py --brief ukg-2step-dark-stab --out-dir als/lesson-author/ukg-2step-dark-stab
python3 als/prepare_serum_lesson_author_bundle.py --brief ukg-4x4-pluck-driver --out-dir als/lesson-author/ukg-4x4-pluck-driver --prefer-rendered
```

Prepare a studio-facing build session for the eventual Ableton writing pass:

```bash
python3 als/prepare_song_build_session.py --brief ukg-140-og-bounce-driver
python3 als/prepare_song_build_session.py --brief ukg-140-og-bounce-driver --format json
```

The author bundle includes:

- `packet/` with the refined lesson packet
- `full-song-blueprint.json` / `full-song-blueprint.md`
- `decision-tree.json` / `decision-tree.md`
- `frozen-song-spec.json` / `frozen-song-spec.md`
- `song-composition-pass.json` / `song-composition-pass.md`
- `song-midi-plan.json` / `song-midi-plan.md`
- `song-build-session.json` / `song-build-session.md`
- `phrase-evidence.json` / `phrase-evidence.md`
- `production-techniques.json` / `production-techniques.md`
- `full-song-readiness.json`
- `compiled-lesson.json` / `compiled-lesson.md`
- `compiled-lesson-diagnostics.json`
- `lesson-validation.json` / `lesson-validation.md`
- `synth-plan.md` / `synth-plan.json`
- `synth-steps.md` / `synth-steps.json`
- `render-blockers.tsv` / `render-blockers.json`
- `bank-candidates.tsv` / `bank-candidates.json`
- `author-queue.json`
- `packet-readiness.json`
- `README.md` with explicit next actions

Prepare one consolidated priority render session across all briefs:

```bash
python3 als/prepare_serum_priority_render_session.py --out-dir als/audio-session/priority-renders
python3 als/prepare_serum_priority_render_session.py --out-dir als/audio-session/priority-renders --priority-source backlog
```

Prepare a full render handoff bundle for the later Ableton/Serum pass:

```bash
python3 als/prepare_serum_render_handoff.py --out-dir als/audio-session/render-handoff
python3 als/prepare_serum_render_handoff.py --out-dir als/audio-session/render-handoff --include-medium
```

After the WAVs have been rendered into that handoff bundle, ingest them and
recompute the readiness/backlog/gap reports:

```bash
python3 als/complete_serum_render_handoff.py --handoff-dir als/audio-session/render-handoff
```

Find similar alternatives to a chosen profile:

```bash
python3 als/find_similar_serum_profiles.py --profile-id mph-raw:bass:i1
python3 als/find_similar_serum_profiles.py --profile-id mph-raw:bass:i1 --prefer-rendered --format json
```

Compare two chosen profiles for clash risk and separation moves:

```bash
python3 als/compare_serum_profiles.py --left mph-raw:bass:i1 --right mph-raw:lead:i3
python3 als/compare_serum_profiles.py --left mph-raw:bass:i1 --right mph-raw:reese:i5 --format json
```

Prepare a manual audio audition session:

```bash
python3 als/prepare_serum_audio_session.py --out-dir als/audio-session --role bass --limit 10
python3 als/prepare_serum_audio_session.py --out-dir als/audio-session --profile-id mph-raw:bass:i1 --force
```

Extract audio descriptors from rendered audition WAV files and attach them back
to the catalog:

```bash
python3 als/extract_serum_audio_features.py --session-dir als/audio-session --force
python3 als/attach_serum_audio_descriptors.py --session-dir als/audio-session --force
```

The audition spec is:

- [../serum-audio-audition-spec.json](../serum-audio-audition-spec.json)

Build small preset palettes:

```bash
python3 als/palette_builder.py --role bass --role pad --role lead
python3 als/palette_builder.py --role bass --role pad --role pluck --target-tone dark
python3 als/palette_builder.py --role bass --role lead --prefer-rendered
```

The canonical schema for each profile is:

- [../schemas/serum-preset-profile.schema.json](../schemas/serum-preset-profile.schema.json)

The broader implementation plan is:

- [../serum-sound-intelligence-roadmap.md](../serum-sound-intelligence-roadmap.md)
