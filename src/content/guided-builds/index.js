import rep01 from "./reps/rep-01-four-on-floor-emin.json";
import rep15 from "./reps/rep-15-drum-rack-from-scratch.json";
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
import spinoff01 from "./spinoffs/spinoff-01-mph-dmin-entry.json";
import spinoff02 from "./spinoffs/spinoff-02-ic-amin-entry.json";
import spinoff03 from "./spinoffs/spinoff-03-ic-dmin-mid.json";
import spinoff04 from "./spinoffs/spinoff-04-kettama-fmin-mid.json";
import spinoff05 from "./spinoffs/spinoff-05-ic-full.json";
import spinoff06 from "./spinoffs/spinoff-06-sammy-full.json";
import spinoff07 from "./spinoffs/spinoff-07-bl3ss-full.json";
import original01 from "./originals/original-01-slow-fade.json";
import original02 from "./originals/original-02-glass-road.json";
import original03 from "./originals/original-03-midnight-circuit.json";
import original04 from "./originals/original-04-static-amber.json";
import original05 from "./originals/original-05-night-walk.json";
import original06 from "./originals/original-06-open-road.json";
import original07 from "./originals/original-07-glass-hour.json";
import original08 from "./originals/original-08-city-current.json";
import original09 from "./originals/original-09-soft-tide.json";
import original10 from "./originals/original-10-held-light.json";
import original11 from "./originals/original-11-low-pull.json";
import original12 from "./originals/original-12-far-signal.json";
import original13 from "./originals/original-13-slow-ember.json";
import original14 from "./originals/original-14-evening-run.json";
import original15 from "./originals/original-15-pressure-drop.json";
import original16 from "./originals/original-16-your-sound.json";

export const builds = [
  rep01,
  rep15,
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
  spinoff01,
  spinoff02,
  spinoff03,
  spinoff04,
  spinoff05,
  spinoff06,
  spinoff07,
  original01,
  original02,
  original03,
  original04,
  original05,
  original06,
  original07,
  original08,
  original09,
  original10,
  original11,
  original12,
  original13,
  original14,
  original15,
  original16,
];

export const buildById = Object.fromEntries(builds.map((b) => [b.id, b]));

export const repsByDifficulty = (diff) =>
  builds.filter((b) => b.build_type === "rep" && b.difficulty === diff);

export const spinoffs = builds.filter((b) => b.build_type === "spinoff");

export const originals = builds.filter((b) => b.build_type === "original");
