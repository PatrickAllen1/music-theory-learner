# Serum VST2 Manual Checkpoints

Deferred manual checkpoint pack for the current Serum VST2 mapping pass. This is the primary end-of-run handoff for controlled save-diff work. The machine-readable companion is `als/serum-vst2-manual-probes.json`. If checkpoints A-E are not enough, layer in `als/serum-vst2-expansion-probes.json` rather than replacing the primary pack.

Common diff command after saving the two `.fxp` variants:

```bash
python3 als/parse_serum_preset.py --diff before.fxp after.fxp --slots 180 --threshold 0.01 --cluster-gap 0
```

End-of-run ingest command for a folder of completed pairs:

```bash
python3 als/ingest_serum_manual_diff.py --pairs-dir /path/to/serum-probe-pairs
python3 als/ingest_serum_manual_diff.py --pairs-dir /path/to/serum-probe-pairs --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json
```

## Checkpoint A
- Objective: prove the `40-43` voicing toggle strip, then map the `166-175` global/voicing tail and the `172-173` pitch-or-misc subpair.
- Target controls: `Note Latch`, `Polyphony Count`, `Bend Range Up`, `Bend Range Down`.
- Suggested control order: `Note Latch` -> `Polyphony Count` -> `Bend Range Up` -> `Bend Range Down` if needed.
- Candidate windows: `40-43`, `166-175`, `172-173`.
- Best candidate presets:
- `Note Latch`: `Garage/Lead- Saturn.fxp`, fallbacks `Garage/Sub- Turn The Page.fxp`, `Garage/Pad- June.fxp`, `Garage/Pad- Wanderlust.fxp`, `Garage/Lead- Just.fxp`
- `Polyphony Count`: `Garage/Stab - digi.fxp`, fallbacks `Garage/Reese - Dusty Heever.fxp`, `Garage/Pad -  Alicee.fxp`, `Garage/Lead - If U Ever.fxp`, `Garage/Bass- Face Melter.fxp`
- `Bend Range`: `Speed Garage/Warp- Speed On Smoke.fxp`, fallbacks `Speed Garage/Warp- Shakhov.fxp`, `Speed Garage/Warp- Rudeboy.fxp`, `Speed Garage/Warp- Don't Stop.fxp`, `Speed Garage/Warp- Big W.fxp`

## Checkpoint B
- Objective: collapse the ambiguous FX corridors at `88-96` and `121-130`.
- Target controls: `EQ TypL`, `EQ TypH`, `Cho_BPM_Sync`, `Flg_BPM_Sync`.
- Suggested control order: `EQ TypL/H` first, then `Cho_BPM_Sync` or `Flg_BPM_Sync`.
- Candidate windows: `88-96`, `94-95`, `121-130`, `127-128`.
- Best candidate presets:
- `EQ TypL/H`: `Garage/Sub- Turn The Page.fxp`, fallbacks `Garage/Lead- Saturn.fxp`, `Garage/Pad- June.fxp`
- `Cho/Flg BPM_Sync`: `Speed Garage/Warp- Shakhov.fxp`, fallbacks `Speed Garage/Warp- Rudeboy.fxp`, `Garage/Lead- Saturn.fxp`

## Checkpoint C
- Objective: pin the `154-163` FX enable block using single-module enable toggles.
- Target controls: `EQ On`, `Delay On`, `Hyper On`; use `Filter On` as the explicit fallback.
- Suggested control order: `EQ On` -> `Delay On` -> `Hyper On` -> `Filter On` only if Hyper is noisy.
- Candidate window: `154-163`.
- Best candidate presets:
- `EQ On`: `Garage/Reese -  Dusty Heever.fxp`, fallbacks `Garage/Stab - digi.fxp`, `Garage/Pad- Wanderlust.fxp`
- `Delay On`: `Garage/Pad- Wanderlust.fxp`, fallbacks `Garage/Sub- Turn The Page.fxp`, `Speed Garage/Warp- Big W.fxp`
- `Hyper On`: `Speed Garage/Warp- Shakhov.fxp`, fallbacks `Speed Garage/Warp- Rudeboy.fxp`, `Garage/Sub- Turn The Page.fxp`
- `Filter On` fallback: `Garage/Reese -  Dusty Heever.fxp`, fallbacks `Garage/Stab - digi.fxp`, `Speed Garage/Bass- Turn Back Time.fxp`

## Checkpoint D
- Objective: resolve the `137-145` portamento/global corridor and separate slot `44` from the `40-43` toggle strip.
- Target controls: `Portamento Time`, `Portamento Curve`, `Porta Mode`, `Porta Scaled`, then the slot `44` neighbor probe.
- Suggested control order: `Portamento Time` -> `Portamento Curve` -> `Porta Mode` -> `Porta Scaled` -> slot `44` probe.
- Candidate windows: `137-145`, `44`.
- Best candidate presets:
- Portamento lane: `Garage/Pad - Yoboy.fxp`, fallbacks `Garage/Bass- Crackhead.fxp`, `Garage/Bass - Donkey.fxp`, `Garage/Bass- Turbo Sally.fxp`
- Slot `44` lane: `Garage/Pad -  Alicee.fxp`, fallbacks `Garage/Pad- Flanger.fxp`, `Garage/Pad- Nora.fxp`, `Garage/Pluck - Pussy.fxp`

## Checkpoint E
- Objective: finish the macro and matrix surfaces after the main synthesis and FX corridors are pinned down.
- Target controls: macro rename, macro amount/source movement, mod route add/remove, matrix curve change.
- Suggested control order: macro rename -> macro amount -> mod route -> matrix curve.
- Candidate windows: `178-179` is the only current explicit tail hint; the rest remain open.
- Best candidate presets:
- `Macro rename`: `Garage/Lead- Just.fxp`, fallbacks `Garage/Pad - Yoboy.fxp`, `Garage/Bass- Face Melter.fxp`, `Garage/Bass- Crackhead.fxp`, `Speed Garage/Bass- Sidewinda.fxp`
- `Macro amount`: `Garage/Lead- Saturn.fxp`, fallbacks `Garage/Bass - 100%.fxp`, `Garage/Pad - Yoboy.fxp`, `Garage/Bass- Sidewinda.fxp`, `Garage/Bass- Crackhead.fxp`
- `Mod route add/remove`: `Garage/Pad- June.fxp`, fallbacks `Garage/Bass- Duality.fxp`, `Garage/Bass- Wide Reese.fxp`, `Garage/Reese - If Bass could kill.fxp`, `Speed Garage/Bass- Sidewinda.fxp`
- `Matrix curve`: `Garage/Bass- Wide Reese.fxp`, fallbacks `Garage/Bass- Duality.fxp`, `Garage/Reese - If Bass could kill.fxp`, `Garage/Bass- Optic Sine.fxp`, `Garage/Bass- Crackhead.fxp`

## After A-E
- If A-E is not enough, the next highest-value unplanned manual probes are:
- Machine-readable companion: `als/serum-vst2-expansion-probes.json`
- `Osc A/B Warp`: `A Warp`, `B Warp`, `Warp Menu OSC A`
- Best preset: `Speed Garage/Warp- Speed On Smoke.fxp`
- Fallbacks: `Speed Garage/Warp- Shakhov.fxp`, `Speed Garage/Warp- Rudeboy.fxp`, `Garage/Bass - Basic Warper.fxp`, `Garage/Bass - Warpie.fxp`
- Remaining global voicing: `Monophonic / Polyphonic switch`, `Legato`, `Unison Stereo Width`, `Unison Warp`, `Unison Stack`, `Unison Detune Mode`
- Best preset: `Garage/Bass- Wide Reese.fxp`
- Fallbacks: `Garage/Lead- Saturn.fxp`, `Garage/Stab - digi.fxp`, `Garage/Bass- Duality.fxp`, `Speed Garage/Warp- Shakhov.fxp`
- LFO family beyond `LFO1Rate`: `LFO2 Rate` / `LFO2 smooth`, then `LFO3`
- Best preset: `Garage/Pad- June.fxp`
- Fallbacks: `Garage/Pad- Wanderlust.fxp`, `Garage/Lead- Saturn.fxp`, `Garage/Lead- Just.fxp`, `Speed Garage/Warp- Shakhov.fxp`
- Filter topology and routing: `Fil Type`, `Fil Var`, `Filter KeyTrack`, `OscA/B/N/S>Fil`
- Best preset: `Garage/Sub- Turn The Page.fxp`
- Fallbacks: `Garage/Reese - Dusty Heever.fxp`, `Garage/Stab - digi.fxp`, `Garage/Pad- June.fxp`, `Garage/Lead- Saturn.fxp`
- Missing FX core family: `Distortion On / Drive / Mode`
- Best preset: `Garage/Bass- Face Melter.fxp`
- Fallbacks: `Garage/Bass- Crackhead.fxp`, `Garage/Bass- Sidewinda.fxp`, `Garage/Reese - If Bass could kill.fxp`, `Garage/Lead- Saturn.fxp`
