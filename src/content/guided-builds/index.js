import rep01 from "./reps/rep-01-four-on-floor-emin.json";
import rep02 from "./reps/rep-02-two-step-gmin.json";
import rep03 from "./reps/rep-03-phrygian-bass-emin.json";
import rep04 from "./reps/rep-04-phrygian-bass-dmin.json";
import rep05 from "./reps/rep-05-phrygian-bass-amin.json";
import rep06 from "./reps/rep-06-mini-track-emin.json";
import rep07 from "./reps/rep-07-mini-track-gmin.json";
import rep08 from "./reps/rep-08-bVI-lift-emin.json";
import rep09 from "./reps/rep-09-bVI-lift-amin.json";
import rep10 from "./reps/rep-10-bVI-lift-dmin.json";
import rep11 from "./reps/rep-11-VI-III-i-loop-bbmin.json";
import rep12 from "./reps/rep-12-VI-III-i-loop-fmin.json";
import rep13 from "./reps/rep-13-bass-implied-dmin.json";
import rep14 from "./reps/rep-14-bass-implied-gmin.json";
import repSerumSubBass from "./reps/rep-serum-sub-bass.json";
import repSerumChordPad from "./reps/rep-serum-chord-pad.json";
import repSerumReeseBass from "./reps/rep-serum-reese-bass.json";
import repSerumStab from "./reps/rep-serum-stab.json";
import spinoffKettama from "./spinoffs/spinoff-kettama-bbmin-full.json";

export const builds = [
  rep01,
  rep02,
  rep03,
  rep04,
  rep05,
  rep06,
  rep07,
  rep08,
  rep09,
  rep10,
  rep11,
  rep12,
  rep13,
  rep14,
  repSerumSubBass,
  repSerumChordPad,
  repSerumReeseBass,
  repSerumStab,
  spinoffKettama,
];

export const buildById = Object.fromEntries(builds.map((b) => [b.id, b]));

export const repsByDifficulty = (diff) =>
  builds.filter((b) => b.build_type === "rep" && b.difficulty === diff);

export const spinoffs = builds.filter((b) => b.build_type === "spinoff");

export const originals = builds.filter((b) => b.build_type === "original");
