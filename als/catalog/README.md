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

Export the whole lesson packet in one shot:

```bash
python3 als/export_serum_lesson_packet.py --brief ukg-4x4-pluck-driver --out-dir als/lesson-packets/ukg-4x4-pluck-driver
python3 als/export_serum_lesson_packet.py --brief ukg-4x4-pluck-driver --refine --out-dir als/lesson-packets/ukg-4x4-pluck-driver
```

Report how well the current catalog covers all briefs and which profiles to render first:

```bash
python3 als/report_serum_brief_coverage.py
python3 als/report_serum_brief_coverage.py --format json
```

Prepare one consolidated priority render session across all briefs:

```bash
python3 als/prepare_serum_priority_render_session.py --out-dir als/audio-session/priority-renders
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
