import part00 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-00-setup.md?raw";
import part01 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-01-foundation-kick-air.md?raw";
import part02 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-02-groove.md?raw";
import part03 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-03-bass-floor.md?raw";
import part04 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-04-harmonic-bed.md?raw";
import part05 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-05-identity-hook-answer.md?raw";
import part06 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-06-arrangement-build.md?raw";
import part07 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-07-transitions-toolkit.md?raw";
import part08 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-08-mix.md?raw";
import part09 from "../../../../docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-09-master.md?raw";

function normalizeTutorialChapter(raw) {
  return raw
    .replace(/^# .*\n+/, "")
    .replace(/^Related documents:\n(?:- .*\n)+/m, "")
    .trim();
}

const chapter = (id, title, category, estimated_minutes, focus, content) => ({
  id,
  title,
  category,
  estimated_minutes,
  focus,
  instruction:
    "Follow the full chapter below exactly. This lesson chapter contains the complete step-by-step guidance, placements, settings, checks, and troubleshooting for this part of the build.",
  content_markdown: normalizeTutorialChapter(content),
});

const original17 = {
  id: "original-17-ukg-140-og-bounce-driver",
  title: "UKG 140 — OG Bounce Driver (D Minor)",
  build_type: "original",
  difficulty: "advanced",
  estimated_time_mins: 420,
  bpm: 140,
  key: "D minor",
  source_track_id: null,
  spinoff_level: null,
  step_label: "Part",
  description:
    "A full hand-holding tutorial for a 144-bar modern UKG / speed-garage original. The site now uses the actual authored tutorial chapters, so the lesson walks through every lane, every MIDI placement, every knob move, and every structural decision instead of summarizing the song in a few paragraphs.",
  what_youll_learn: [
    "How to set up a full 144-bar UKG session with every lane and return already in the right place",
    "How to build kick, hats, bass, chords, hook, answer, arrangement, transitions, mix, and master with exact placements and settings",
    "How to keep all drum lanes separate from the start for later mixing control",
    "How to stage restrained versus bloomed harmony and a real Drop B conversation",
    "How to clear the named blockers during the build instead of hoping the mix fixes them"
  ],
  steps: [
    chapter(0, "Part 0 — Setup", "ableton", 20, "Project foundation", part00),
    chapter(
      1,
      "Part 1 — Foundation (Kick + Air Ceiling)",
      "drums",
      30,
      "Floor and ceiling",
      part01,
    ),
    chapter(2, "Part 2 — Groove", "drums", 75, "Separate drum lanes", part02),
    chapter(3, "Part 3 — Bass Floor", "bass", 90, "Rolling bass core", part03),
    chapter(
      4,
      "Part 4 — Harmonic Bed",
      "chords",
      75,
      "Restrained vs bloomed harmony",
      part04,
    ),
    chapter(
      5,
      "Part 5 — Identity (Hook + Answer)",
      "melody",
      60,
      "Instrumental identity",
      part05,
    ),
    chapter(
      6,
      "Part 6 — Arrangement Build",
      "ableton",
      90,
      "144-bar song form",
      part06,
    ),
    chapter(
      7,
      "Part 7 — Transitions Toolkit",
      "ableton",
      75,
      "Section-boundary motion",
      part07,
    ),
    chapter(8, "Part 8 — Mix", "mix", 90, "Premaster and blockers", part08),
    chapter(9, "Part 9 — Master", "mix", 45, "Final delivery", part09),
  ],
};

export default original17;
