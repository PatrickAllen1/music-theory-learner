# Serum Audio Catalog

This folder holds catalog-level audio summaries derived from rendered Serum
audition WAV files.

Expected structure after running the audio pipeline:

- `index.json`:
  top-level summary of rendered profiles and attached descriptor coverage
- `profiles/`:
  one audio summary JSON per profile, grouped from individual audition renders

Typical workflow:

```bash
python3 als/prepare_serum_audio_session.py --out-dir als/audio-session --role bass --limit 10
python3 als/extract_serum_audio_features.py --session-dir als/audio-session --force
python3 als/attach_serum_audio_descriptors.py --session-dir als/audio-session --force
```

The profile catalog in `../profiles/` will then point each rendered profile at
its corresponding audio summary JSON.
