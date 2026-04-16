# Production Technique Bank

This folder stores transcript-derived production techniques in a reusable form.

Current files:

- `bank.json`
  canonical technique bank used by the authoring tooling

Current entry shape:

- `id`
- `name`
- `source`
- `what_it_does`
- `when_to_use`
- `works_well_with`
- `likely_clashes_with`
- `why`
- `mitigations`

Useful commands:

Validate the bank:

```bash
python3 als/validate_technique_bank.py
```

Search the bank:

```bash
python3 als/query_technique_bank.py --q "pitch bend lead"
python3 als/query_technique_bank.py --source "Raw — MPH"
```

Recommend techniques for a full-song brief:

```bash
python3 als/recommend_production_techniques.py --brief ukg-2step-dark-stab
python3 als/recommend_production_techniques.py --brief ukg-4x4-pluck-driver --format json
```

Intended workflow:

1. Clean a transcript without losing track-specific production details.
2. Split it into tagged spans.
3. Turn those spans into reusable techniques in `bank.json`.
4. Query and recommend those techniques during blueprint and lesson authoring.
