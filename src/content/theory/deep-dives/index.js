import viIIIi from "./vi-iii-i-loop.json";
import phrygianTension from "./phrygian-tension.json";
import bassImplied from "./bass-implied-harmony.json";
import chordVoicing from "./chord-voicing.json";
import serumV2Ui from "./serum-v2-ui.json";

export const deepDives = [
  viIIIi,
  phrygianTension,
  bassImplied,
  chordVoicing,
  serumV2Ui,
];

export const deepDiveById = Object.fromEntries(deepDives.map((d) => [d.id, d]));
