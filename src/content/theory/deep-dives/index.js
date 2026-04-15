import viIIIi from "./vi-iii-i-loop.json";
import phrygianTension from "./phrygian-tension.json";
import bassImplied from "./bass-implied-harmony.json";
import chordVoicing from "./chord-voicing.json";
import serumV2Ui from "./serum-v2-ui.json";
import arrangementTheory from "./arrangement-theory.json";
import soundDesignEmotion from "./sound-design-emotion.json";
import transposingConcepts from "./transposing-concepts.json";
import serumLayering from "./serum-layering.json";
import reverb from "./reverb.json";
import delay from "./delay.json";
import compression from "./compression.json";
import saturation from "./saturation.json";
import eqStrategy from "./eq-strategy.json";

export const deepDives = [
  viIIIi,
  phrygianTension,
  bassImplied,
  chordVoicing,
  serumV2Ui,
  arrangementTheory,
  soundDesignEmotion,
  transposingConcepts,
  serumLayering,
  reverb,
  delay,
  compression,
  saturation,
  eqStrategy,
];

export const deepDiveById = Object.fromEntries(deepDives.map((d) => [d.id, d]));
