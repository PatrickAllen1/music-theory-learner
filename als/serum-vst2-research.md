# Serum VST2 / FXP Research

This repo already had a VST2 Serum chunk parser for `.als` files in
[`als/parse_serum.py`](./parse_serum.py). The first reverse-engineering pass for
standalone Serum 1 / VST2 `.fxp` presets now reuses that same chunk parser.

## New tooling

### Standalone preset parser

```bash
python3 als/parse_serum_preset.py '/path/to/preset.fxp'
```

Prints:

- preset header metadata (`FPCh`, plugin id, preset name)
- wavetable / sample references discovered in the chunk
- embedded vendor / bank text when present
- embedded macro labels when present
- the currently-known VST2 parameter subset from the existing ALS parser

### Raw slot inspection

```bash
python3 als/parse_serum_preset.py '/path/to/preset.fxp' --slots 160 --nonzero-only
```

Prints the raw float slot block starting from `SERUM_V2_PARAM_OFFSET` with:

- slot index
- byte offset
- raw float
- known parameter label when already mapped

### Printable string scan

```bash
python3 als/parse_serum_preset.py '/path/to/preset.fxp' --strings 20 --strings-start 18784 --strings-end 19200
```

Useful for:

- verifying embedded vendor and bank metadata
- seeing custom macro labels directly from the chunk
- checking whether a preset family uses text-backed controls or defaults

### Preset diffing

```bash
python3 als/parse_serum_preset.py --diff preset-a.fxp preset-b.fxp --slots 220 --threshold 0.05
```

Useful for answering:

- which slots separate `Lead- Just` from `Lead- Saturn`
- which slots likely correspond to FX or macro behavior
- which blocks stay constant across a family of similar presets

The diff output now also includes `diff_clusters`, which groups nearby slot
changes into contiguous regions so you can target specific unknown blocks
instead of reasoning about a flat list of deltas.

### Multi-preset varying-slot scan

```bash
python3 als/parse_serum_preset.py preset-a.fxp preset-b.fxp preset-c.fxp --varying --slots 220 --threshold 0.1
```

This is the best way to spot candidate slot ranges worth mapping next.

The varying output now also includes `varying_clusters` for the same reason.

### Host parameter catalog extractor

```bash
python3 als/extract_serum_host_params.py
python3 als/extract_serum_host_params.py --limit 60
python3 als/extract_serum_host_params.py --labels-only
```

This reads the installed Serum VST2 plugin binary directly and extracts a
machine-readable catalog of host-facing labels and nearby descriptions.

What this gives us:

- oscillator controls like `A Vol`, `A WTPos`, `B UniDet`
- filter controls like `Fil Cutoff`, `Fil Reso`, `Fil Drive`
- FX controls like `Dist_Wet`, `Dly_TimL`, `Comp_Wet`, `Hyp_Detune`
- toggles like `Dist_On`, `Rev_On`, `FX Fil On`
- modulation entries like `Mod Matrix Depth 1`, `Mod Dest 1`
- matrix curve controls like `Matrix Curve A 1`

Important limit:

- this is a discovery catalog, not a proven one-to-one mapping to the `.fxp`
  float slots yet
- the ALS files report `315` host parameters for Serum VST2
- the binary text catalog is broader than that and also includes some UI-adjacent
  labels, so it should be treated as a source of names/descriptions to align,
  not as final slot truth

### Coverage report

```bash
python3 als/report_serum_vst2_coverage.py --summary-only
python3 als/report_serum_vst2_coverage.py --category fx
```

This cross-references the current standalone `.fxp` parser against the binary
host catalog using only safe aliases.

What it tells us:

- which named Serum host controls are already covered by the parser
- which broad categories are still dark
- where to spend the next controlled-diff mapping pass

Current safe-coverage picture from that report:

- oscillator A host labels: about half covered
- oscillator B host labels: about half covered
- envelopes: partial (`Env1` + `Env2` core ADSR, but no hold/curves/`Env3+`)
- filter: partial (`Cutoff`, `Reso`, `Drive`, `Mix`)
- modulation: almost entirely missing beyond `LFO1Rate`
- FX: effectively missing
- matrix: entirely missing
- macros: labels covered, macro-source controls still missing

### Corpus slot profiler

```bash
python3 als/analyze_serum_vst2_slots.py --summary-only
python3 als/analyze_serum_vst2_slots.py --unknown-only --top 40
python3 als/analyze_serum_vst2_slots.py --bank garage
```

This profiles float-slot behavior across the Garage / Speed Garage preset corpus.

What it tells us:

- which unknown slots are boolean-like, discrete, or continuous
- which contiguous regions move together across many presets
- which regions are likely to be better next targets for manual mapping

Current useful outcome from that profiler:

- unknown slots `34-66` form a mixed region with continuous, enum-like, and a
  few boolean behaviors
- unknown slots `71-163` are the biggest unmapped block and include many binary,
  enum-like, and continuous slots
- unknown slots `166-175` look like a smaller mostly enum/discrete tail
- unknown slots `178-179` look strongly enum-like

That means the next controlled-diff passes should probably focus on:

1. one small boolean/discrete region
2. one FX-heavy continuous region
3. one modulation / matrix region

instead of trying to decode the entire unknown space in one shot

## What we can parse confidently now

From the existing VST2 map plus standalone `.fxp` extraction:

- `OSC A` level, detune, pan, WT position, octave, semitone, unison voices
- `OSC B` level, detune, pan, WT position, octave, semitone, unison voices
- `Sub` and `Noise` level guesses
- Filter cutoff / resonance / drive / pan / mix guesses
- `Env1` and `Env2` ADSR
- a small amount of `LFO1`
- wavetable and sample references embedded in the chunk
- embedded vendor / bank text
- embedded macro labels when the preset author named them
- a binary-derived host parameter catalog with named FX / matrix / global controls

## Example useful findings

### `Sub- Turn The Page`

- Wavetables / sources:
  - `Analog/Analog_BD_Sin.wav`
  - `Analog/Basic Shapes.wav`
  - `Analog/OrganNoise.wav`
- `OSC B` is off
- Instant amp attack with short release
- This supports the inference that it is a sine-heavy sub patch with a little harmonic/noise support

### `Pad- Wanderlust`

- Wavetables / sources:
  - `Analog/Jno.wav`
  - `Analog/Basic Mini.wav`
  - `Analog/J106.wav`
- `OSC A` unison voices decode to 6
- Filter cutoff is materially darker than a bright lead
- This supports the inference that it is a wide analog-style pad

### `Lead- Just`

- `OSC B` is active and materially different from `Lead- Saturn`
- Uses `Analog/Basic Shapes.wav` plus `Organics/AC hum1.wav`
- `Env1` attack is slower than `Lead- Saturn`
- Embedded macro labels decode directly as:
  - `FILTER`
  - `OPEN`
  - `SUSTAIN`
  - `REVEERB`
- This supports the inference that it is a layered, slightly more textured lead with more body

## Current reverse-engineering status

The standalone parser is real and useful, but the VST2 map is still partial.

The first directly-parsed non-float metadata is now confirmed:

- preset title
- vendor
- bank / pack name
- some macro labels
- a large host-parameter label catalog from the installed Serum binary

That matters because it gives us a second evidence source beyond float deltas:
we can now tell whether a preset intentionally exposes named performance
controls such as `FILTER` or `OPEN`, which helps prioritize which slot clusters
are likely to be macro-linked or FX-related.

The new binary catalog matters for a different reason:

- we no longer have to guess the names of many Serum controls
- we can mine the plugin binary for labels like `Dist_Wet`, `Dly_TimL`,
  `Comp_Wet`, `Mod Matrix Depth 1`, and `Matrix Curve A 1`
- the remaining job is alignment: proving which slot or slot cluster corresponds
  to which named control

There are clearly more active float slots after the currently-mapped block. In
early scans, the ranges below show meaningful variation across presets:

- around indices `34-59`
- around indices `65-83`
- around indices `96-116`
- around indices `124-132`
- around indices `166-171`

These likely contain some mix of:

- additional envelopes / LFO settings
- noise / sub / filter-mode flags
- FX amounts and enable states
- macro amounts or modulation depth
- routing / matrix state

That said, those assignments are still hypotheses. We should not label them as
FX / macros / routing until they are validated against controlled preset diffs.

## Recommended next mapping workflow

1. Choose deliberately contrasting presets for one category only.
   - Example: two leads, or two pads, not a sub vs pad vs lead mix.
2. Run `--diff` and note slots with large deltas.
3. Open both presets in Serum and change one parameter manually.
4. Save as two adjacent presets.
5. Diff those two saved presets.
6. Attribute the changed slot(s) to the one edited parameter.

This is the fastest safe way to map:

- FX enable / amount slots
- macro labels and amounts
- modulation matrix slot structure
- filter type / route flags
- global / voicing settings

The current tooling should be treated as the staging layer for that work:

- use `--strings` to find embedded labels
- use `--diff` to locate changed slots
- use `diff_clusters` to see which unknown regions move together
- use `extract_serum_host_params.py` to inspect named host controls from the
  plugin binary
- use `report_serum_vst2_coverage.py` to decide which named categories and
  modules to target next
- then validate those regions with one-parameter saves from Serum

## Manual-aware catalog structure

The public Serum manual is useful for alignment, but not because it reveals the
raw VST2 slot order. What it gives us is the correct UI/module structure:

- oscillators
- filter + filter routing
- envelopes
- LFOs / Chaos
- mod matrix
- voicing / global
- FX modules such as Distortion, Delay, Compressor, Hyper/Dimension, etc.

The host-control extractor now enriches each label with:

- `category`
- `module`
- `manual_section`
- `control_kind_hint`

That means we can filter the 499-label host catalog in ways that match the
manual and Serum UI, for example:

- `python3 als/extract_serum_host_params.py --module fx_delay`
- `python3 als/report_serum_vst2_coverage.py --module fx_delay`
- `python3 als/report_serum_vst2_coverage.py --module global_voicing`

This does not prove slot indices by itself, but it materially improves the next
alignment step because we can target a narrower, semantically-correct surface
instead of treating `fx` or `global` as one flat bucket.

## Existing ALS anchors

The local ALS analysis set already contains named Serum 2 global/voicing params
that are useful as semantic anchors, even though they do not directly reveal the
old VST2 slot layout. Examples from the analysis JSON:

- `kParamPortamentoTime`
- `kParamLegato`
- `kParamPortaAlways`
- `kParamMonoToggle`

These confirm that portamento / legato / mono are real, active controls in the
kind of bass and lead patches we care about. They should inform targeting, but
they should NOT be used to claim a direct VST2 slot mapping.

## Module candidate ranking

There is now a helper script for behavior-based candidate ranking:

- `python3 als/rank_serum_vst2_module_candidates.py --module global_portamento`

This script:

- takes a host module's expected control kinds from the extracted VST2 host
  catalog
- profiles unknown VST2 float slots across the preset corpus
- ranks contiguous unknown windows by how well they match the target module's
  kind signature

It still does not prove mappings, but it turns "somewhere in the unknown
region" into a short candidate list for controlled diffs.

Current `global_portamento` signature:

- `continuous`: 2
- `discrete_or_enum`: 1
- `boolean_or_toggle`: 1

Current top candidate windows from the Garage / Speed Garage corpus:

- `140-143`
- `149-152`
- `150-153`
- `128-131`
- `138-141`

These are the best current targets for the next controlled-save pass if we want
to prove:

- Portamento Time
- Portamento Curve
- Porta Mode
- Porta Scaled

## Synthetic family results

Module ranking is useful, but some Serum surfaces are better treated as control
families before we try to prove exact per-label mappings.

The first strong example is:

- `fx_enable_toggles`

This synthetic family is defined as the ten FX on/off labels:

- `Dist_On`
- `Flg_On`
- `Phs_On`
- `Cho_On`
- `Dly_On`
- `Comp_On`
- `Rev_On`
- `EQ_On`
- `FX Fil On`
- `Hyper FX On`

The family ranking result is currently the strongest structural clue in the
whole VST2 reverse-engineering pass:

- top candidate window: `154-163`
- score: `1.0`
- shape: `10 / 10` boolean-style slots

This is not yet a proven per-label ordering, but it is a high-confidence family
level hypothesis:

- cluster `154-163` is very likely the VST2 storage region for Serum FX enable
  toggles

That gives us a better next proof path:

1. save one preset with only one FX module toggled on/off
2. diff the preset
3. check whether the changed slot falls inside `154-163`
4. repeat for a second FX module to test ordering inside the family

## Exclusion-aware FX correlation pass

The first FX-enable correlation pass produced strong-looking hits around
`137-145`, but that region overlaps the current best `global_portamento`
candidates:

- `140-143`
- `149-152`
- `150-153`

That means early FX correlations into `137-145` are likely contaminated by a
non-FX region.

The ranking/correlation tools now support explicit exclusion ranges, which is
useful for stripping known or likely non-target regions out of the candidate
pool before comparing FX modules.

Example:

```bash
python3 als/rank_serum_vst2_module_candidates.py --module fx_eq \
  --exclude-range 40-44 \
  --exclude-range 137-145 \
  --exclude-range 154-163

python3 als/correlate_serum_vst2_fx_enables.py \
  --module-exclude-range 40-44 \
  --module-exclude-range 137-145 \
  --module-exclude-range 154-163
```

The current working interpretation of those excluded ranges is:

- `40-44`: likely oscillator/filter/global boolean region, not a safe FX target
- `137-145`: likely polluted by `global_portamento`
- `154-163`: the high-confidence FX enable family itself, so it should not also
  be treated as an FX parameter window

Once those ranges are excluded, the strongest FX parameter families shift:

- `fx_distortion` / `fx_filter`: `88-95`
- `fx_eq`: `88-96`
- `fx_compressor`: `88-93`
- `fx_delay`: `121-132`
- `fx_flanger` / `fx_chorus`: `123-129`
- `fx_phaser` / `fx_hyper_dimension`: `123-130`

That does not prove exact assignments, but it is a better search space than the
earlier broad `137-145` guess.

The strongest exclusion-aware correlations inside the `154-163` FX-enable block
now look like this:

- slot `158` strongly aligns with the `121-130` family
  - `fx_flanger` / `fx_chorus` window `123-129`: `delta 0.141798`, `pearson 0.704613`
  - `fx_phaser` / `fx_hyper_dimension` window `123-130`: `delta 0.129998`, `pearson 0.674650`
  - `fx_delay` window `121-132`: `delta 0.124852`, `pearson 0.705655`
- slot `161` strongly aligns with the `88-96` family
  - `fx_distortion` / `fx_filter` window `88-95`: `delta 0.165771`, `pearson 0.660423`
  - `fx_eq` window `88-96`: `delta 0.155637`, `pearson 0.679637`
  - `fx_compressor` window `88-93`: `delta 0.084283`, `pearson 0.537714`
- slot `155` weakly favors `fx_delay`, but the signal is much weaker than
  slots `158` and `161`

The practical consequence is:

- the next controlled-save diff should prioritize one FX from the `121-130`
  family and one FX from the `88-96` family
- those two saves should tell us much more than toggling modules that keep
  collapsing into the same broad candidate window

## Good immediate targets

- `Lead- Just` vs `Lead- Saturn`
- `Pad- Wanderlust` vs `Pad- June`
- `Sub- Turn The Page` vs `Sub- Sidewinda`
- one preset saved twice with only `Delay Mix` changed
- one preset saved twice with only `Macro 1` renamed
- one preset saved twice with only one modulation matrix route added

Those controlled diffs will tell us much more than broad preset-family comparison.
