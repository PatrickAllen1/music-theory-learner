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

The canonical schema for each profile is:

- [../schemas/serum-preset-profile.schema.json](../schemas/serum-preset-profile.schema.json)

The broader implementation plan is:

- [../serum-sound-intelligence-roadmap.md](../serum-sound-intelligence-roadmap.md)
