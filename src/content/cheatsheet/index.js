import sidechain from "./sidechain.json";
import eqEight from "./eq-eight.json";
import drumRack from "./drum-rack.json";
import serumOscillators from "./serum-v2-oscillators.json";
import serumFilter from "./serum-v2-filter.json";
import serumEnvelopes from "./serum-v2-envelopes.json";
import simpler from "./simpler.json";
import glueCompressor from "./glue-compressor.json";
import reverb from "./reverb.json";
import chorus from "./chorus.json";
import limiter from "./limiter.json";
import saturator from "./saturator.json";
import simplerLfo from "./simpler-lfo.json";
import simplerFilter from "./simpler-filter.json";
import autoFilter from "./auto-filter.json";
import compressor from "./compressor.json";
import simpleDelay from "./simple-delay.json";
import overdrive from "./overdrive.json";
import flanger from "./flanger.json";
import operator from "./operator.json";
import gate from "./gate.json";
import grainDelay from "./grain-delay.json";
import filterDelay from "./filter-delay.json";
import amp from "./amp.json";
import groovePool from "./groove-pool.json";
import automation from "./automation.json";
import returnTracks from "./return-tracks.json";
import utilityMono from "./utility-mono.json";
import instrumentRack from "./instrument-rack.json";
import audioEffectRack from "./audio-effect-rack.json";
import midiEffects from "./midi-effects.json";
import clipEnvelopes from "./clip-envelopes.json";
import arrangementView from "./arrangement-view.json";
import resampling from "./resampling.json";
import trackGrouping from "./track-grouping.json";
import operatorSubBass from "./operator-sub-bass.json";

export const entries = [
  // Original 3
  drumRack,
  eqEight,
  sidechain,
  // Serum entries
  serumOscillators,
  serumFilter,
  serumEnvelopes,
  // Tier 1 — used in all 5 source tracks
  simpler,
  glueCompressor,
  reverb,
  chorus,
  // Tier 2 — used in 4/5 tracks
  limiter,
  saturator,
  simplerLfo,
  simplerFilter,
  // Tier 3 — used in 3/5 tracks
  autoFilter,
  compressor,
  // Tier 4 — used in 2/5 tracks
  simpleDelay,
  overdrive,
  flanger,
  // Tier 5 — Kettama-specific (Suite-only noted)
  operator,
  gate,
  grainDelay,
  filterDelay,
  amp,
  // Tier 6 — Workflow & routing
  groovePool,
  automation,
  returnTracks,
  utilityMono,
  instrumentRack,
  audioEffectRack,
  midiEffects,
  clipEnvelopes,
  arrangementView,
  resampling,
  trackGrouping,
  operatorSubBass,
];

export const entryById = Object.fromEntries(entries.map((e) => [e.id, e]));

export const entriesByCategory = entries.reduce((acc, e) => {
  if (!acc[e.category]) acc[e.category] = [];
  acc[e.category].push(e);
  return acc;
}, {});
