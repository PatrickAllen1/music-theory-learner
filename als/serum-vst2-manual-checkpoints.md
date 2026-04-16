# Serum VST2 Manual Checkpoints

Deferred manual checkpoint pack for the current Serum VST2 mapping pass. This is the primary end-of-run handoff for controlled save-diff work. The machine-readable companions are:

- `als/serum-vst2-manual-probes.json` for checkpoints A-E
- `als/serum-vst2-expansion-probes.json` for checkpoint F
- `als/serum-vst2-phase3-probes.json` for checkpoint G
- `als/serum-vst2-phase4-probes.json` for checkpoint H

Session prep helper:

```bash
python3 als/prepare_serum_manual_session.py --out-dir /tmp/serum-manual-session
python3 als/prepare_serum_manual_session.py --out-dir /tmp/serum-manual-session-A --checkpoint A --force
```

The prepared session folder now includes:

- `capture_queue.tsv` for the canonical probe order
- `subprobe_queue.tsv` for chunked views of oversized probes like matrix, oscillator-detail, and LFO families
- `expected-files.txt` for the exact `.before/.after` filenames
- `session_state.json` as the authoritative resume source for completed probes, pending probes, and the next queue item

Refresh session state during a long capture run:

```bash
python3 als/report_serum_vst2_session_progress.py --session-dir /tmp/serum-manual-session --write-state
python3 als/render_serum_manual_bundle.py --state-json /tmp/serum-manual-session/session_state.json | sed -n '1,40p'
```

Common diff command after saving the two `.fxp` variants:

```bash
python3 als/parse_serum_preset.py --diff before.fxp after.fxp --slots 180 --threshold 0.01 --cluster-gap 0
```

End-of-run ingest command for a folder of completed pairs:

```bash
python3 als/ingest_serum_manual_diff.py --pairs-dir /path/to/serum-probe-pairs
python3 als/ingest_serum_manual_diff.py --pairs-dir /path/to/serum-probe-pairs --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json
python3 als/ingest_serum_manual_diff.py --pairs-dir /path/to/serum-probe-pairs --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json --manifest als/serum-vst2-phase3-probes.json
python3 als/ingest_serum_manual_diff.py --pairs-dir /path/to/serum-probe-pairs --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json --manifest als/serum-vst2-phase3-probes.json --manifest als/serum-vst2-phase4-probes.json
```

One-shot post-diff wrapper:

```bash
python3 als/run_serum_vst2_postdiff.py --pairs-dir /path/to/serum-probe-pairs --out-dir /tmp/serum-postdiff
python3 als/run_serum_vst2_postdiff.py --pairs-dir /path/to/serum-probe-pairs --out-dir /tmp/serum-postdiff-A --checkpoint A
```

The wrapper now writes:

- `ingest.json` with raw per-probe diff summaries plus consensus/follow-up queues
- `mapping.json` with promoted mappings for accepted statuses (`confirmed` and `expected_hit` by default)
- `gaps.json` with unresolved checkpoint/probe status after promotion
- `mapping_coverage.json` with parser-covered vs manually evidenced vs still-dark modules
- `summary.md` with the readable post-diff queue

`mapping.json` also includes aggregated `parser_work_items`, so the next parser-alignment pass can start with file-level edit groups instead of raw promoted rows.

Preflight a capture folder before ingest:

```bash
python3 als/validate_serum_manual_bundle.py --pairs-dir /path/to/serum-probe-pairs
python3 als/validate_serum_manual_bundle.py --pairs-dir /path/to/serum-probe-pairs --ingest-json /tmp/serum-postdiff/ingest.json --reject-status no_diff --reject-status unexpected_cluster --max-follow-up 0
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

## After F
- If checkpoint F still leaves dark surfaces, layer in `als/serum-vst2-phase3-probes.json`.
- Phase-3 targets:
- Compressor core: `Comp Enable`, `Comp_Wet`, `Cmp_Thr`, `Cmp_Rat`, `Cmp_Att`, `Cmp_Rel`, `Comp_On`, `CmpGain`
- Phaser core: `Phs Enable`, `Phs_BPM_Sync`, `Phs_Rate`, `Phs_Dpth`, `Phs_Frq`, `Phs_Feed`, `Phs_Stereo`, `Phs_On`
- Reverb core: `Rev Enable`, `FX Reverb Level`, `Rev_On`, `Reverb Type -`
- Sub oscillator core: `SubOscShape`, `SubOscOctave`, `Sub Osc Pan`, `Osc Enable sub`, `SubOsc Direct`
- Noise oscillator core: `Noise Oscillator Color`, `Noise Oscillator Fine`, `Noise Oscillator Pan`, `Noise Random Phase`, `Noise Initial Phase`, `Osc Enable noise`, `Noise Osc Direct`
- Oscillator A/B detail: on/off, fine, coarse, random phase, initial phase, pitch track, unison LR/warp/WTPos/stack
- Envelope family: `Amp Hold`, `Env2 Hld`, full `Env3` ADSR, and the envelope-curve family
- Matrix aux/output families: `Mod Aux Source 1-32` and `Mod Matrix Output 1-32`
- Chaos family: both Chaos rate/sync/mono/SNH/source lanes
- Low-confidence host-global sweep: `Master Volume`, `Quality`, `GUI Size`
- Delay bridge: `FX Delay Level`

## After G
- If checkpoint G still leaves broad FX and LFO surfaces open, layer in `als/serum-vst2-phase4-probes.json`.
- Phase-4 targets:
- EQ core: `EQ FrqL/H`, `EQ Q L/H`, `EQ VolL/H`
- Delay core: wet, filter, sync, link, time left/right, mode, feedback, offsets
- Chorus core: enable/on, wet, rate, depth, feed, LPF, chorus level
- Flanger core: enable/on, wet, rate, depth, feed, stereo, flanger level
- FX filter core: wet, type, freq, reso, drive, var, pan, filter level
- Hyper/Dimension core: wet, rate, detune, unison, retrig, Hyper/Dimension levels
- Distortion extended: wet, level, low/band/high, freq, bandwidth, pre/post
- Canonical post-LFO1 sweep: `LFO1-4` smooth/rate/rise/delay
- After applying the current alias/residue overrides, the four-pack bundle effectively covers every remaining uncovered module in the host catalog.
