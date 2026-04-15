import viIIIi from "./vi-iii-i-loop.json";
import phrygianTension from "./phrygian-tension.json";
import bassImplied from "./bass-implied-harmony.json";
import chordVoicing from "./chord-voicing.json";

export const deepDives = [viIIIi, phrygianTension, bassImplied, chordVoicing];

export const deepDiveById = Object.fromEntries(deepDives.map((d) => [d.id, d]));
