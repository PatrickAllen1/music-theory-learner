import mphRaw from "./mph-raw.json";
import kettamaItGetsBetter from "./kettama-it-gets-better.json";
import interplanetaryCriminalSlowBurner from "./interplanetary-criminal-slow-burner.json";
import sammyVirjiCopsAndRobbers from "./sammy-virji-cops-and-robbers.json";
import bl3ssKisses from "./bl3ss-camrinwatsin-kisses.json";

export const tracks = [
  mphRaw,
  kettamaItGetsBetter,
  interplanetaryCriminalSlowBurner,
  sammyVirjiCopsAndRobbers,
  bl3ssKisses,
];

export const trackById = Object.fromEntries(tracks.map((t) => [t.id, t]));
