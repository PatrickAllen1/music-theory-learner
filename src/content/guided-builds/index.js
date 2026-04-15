import rep01 from "./reps/rep-01-four-on-floor-emin.json";
import rep02 from "./reps/rep-02-two-step-gmin.json";
import rep03 from "./reps/rep-03-phrygian-bass-emin.json";

export const builds = [rep01, rep02, rep03];

export const buildById = Object.fromEntries(builds.map((b) => [b.id, b]));

export const repsByDifficulty = (diff) =>
  builds.filter((b) => b.build_type === "rep" && b.difficulty === diff);

export const spinoffs = builds.filter((b) => b.build_type === "spinoff");

export const originals = builds.filter((b) => b.build_type === "original");
