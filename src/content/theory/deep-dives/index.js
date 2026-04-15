import viIIIi from "./vi-iii-i-loop.json";
import phrygianTension from "./phrygian-tension.json";
import bassImplied from "./bass-implied-harmony.json";
import chordVoicing from "./chord-voicing.json";
import serumV2Ui from "./serum-v2-ui.json";
import arrangementTheory from "./arrangement-theory.json";
import soundDesignEmotion from "./sound-design-emotion.json";
import transposingConcepts from "./transposing-concepts.json";

export const deepDives = [
  viIIIi,
  phrygianTension,
  bassImplied,
  chordVoicing,
  serumV2Ui,
  arrangementTheory,
  soundDesignEmotion,
  transposingConcepts,
];

export const deepDiveById = Object.fromEntries(deepDives.map((d) => [d.id, d]));
