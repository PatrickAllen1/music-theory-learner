import sidechain from "./sidechain.json";
import eqEight from "./eq-eight.json";
import drumRack from "./drum-rack.json";

export const entries = [sidechain, eqEight, drumRack];
export const entryById = Object.fromEntries(entries.map((e) => [e.id, e]));
