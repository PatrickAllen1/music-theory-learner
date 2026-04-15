import sidechain from "./sidechain.json";
import eqEight from "./eq-eight.json";
import drumRack from "./drum-rack.json";
import serumOscillators from "./serum-v2-oscillators.json";
import serumFilter from "./serum-v2-filter.json";
import serumEnvelopes from "./serum-v2-envelopes.json";

export const entries = [
  sidechain,
  eqEight,
  drumRack,
  serumOscillators,
  serumFilter,
  serumEnvelopes,
];
export const entryById = Object.fromEntries(entries.map((e) => [e.id, e]));
