# Golden Serum Profiles

These are checked-in normalized profile fixtures.

Purpose:

- provide stable examples for downstream tooling
- make schema evolution explicit
- keep a small trusted sample in git before the wider generated catalog is
  treated as durable output

Current fixture set:

- `mph-raw-serum-profiles.json`

Rebuild manually if the profile schema changes:

```bash
python3 als/build_serum_profile.py \
  --analysis-json als/analysis/mph-raw-serum.json \
  --out als/catalog/golden/mph-raw-serum-profiles.json
```
