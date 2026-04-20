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

const PARTS = [
  {
    id: "part-00",
    part_number: 0,
    title: "Setup",
    category: "ableton",
    estimated_minutes: 20,
    focus: "Project foundation",
    content: part00,
  },
  {
    id: "part-01",
    part_number: 1,
    title: "Foundation (Kick + Air Ceiling)",
    category: "drums",
    estimated_minutes: 30,
    focus: "Floor and ceiling",
    content: part01,
  },
  {
    id: "part-02",
    part_number: 2,
    title: "Groove",
    category: "drums",
    estimated_minutes: 75,
    focus: "Separate drum lanes",
    content: part02,
  },
  {
    id: "part-03",
    part_number: 3,
    title: "Bass Floor",
    category: "bass",
    estimated_minutes: 90,
    focus: "Rolling bass core",
    content: part03,
  },
  {
    id: "part-04",
    part_number: 4,
    title: "Harmonic Bed",
    category: "chords",
    estimated_minutes: 75,
    focus: "Restrained vs bloomed harmony",
    content: part04,
  },
  {
    id: "part-05",
    part_number: 5,
    title: "Vocal Phrase + Chop Vocabulary",
    category: "sampling",
    estimated_minutes: 120,
    focus: "Vocal identity lane",
    content: part05,
  },
  {
    id: "part-06",
    part_number: 6,
    title: "Arrangement Build",
    category: "ableton",
    estimated_minutes: 90,
    focus: "144-bar song form",
    content: part06,
  },
  {
    id: "part-07",
    part_number: 7,
    title: "Transitions Toolkit",
    category: "ableton",
    estimated_minutes: 75,
    focus: "Section-boundary motion",
    content: part07,
  },
  {
    id: "part-08",
    part_number: 8,
    title: "Mix",
    category: "mix",
    estimated_minutes: 90,
    focus: "Premaster and blockers",
    content: part08,
  },
  {
    id: "part-09",
    part_number: 9,
    title: "Master",
    category: "mix",
    estimated_minutes: 45,
    focus: "Final delivery",
    content: part09,
  },
];

function stripRelatedDocuments(raw) {
  return raw.replace(/^Related documents:\n(?:- .*\n)+/m, "").trim();
}

function extractH1(raw) {
  const match = raw.match(/^# (.+)$/m);
  return match?.[1]?.trim() ?? "";
}

function splitH2Sections(markdown) {
  const regex = /^## (.+)$/gm;
  const matches = [...markdown.matchAll(regex)];
  if (matches.length === 0) return [];

  return matches.map((match, index) => {
    const title = match[1].trim();
    const start = match.index + match[0].length;
    const end = index + 1 < matches.length ? matches[index + 1].index : markdown.length;
    const body = markdown.slice(start, end).trim();
    return { title, body };
  });
}

function sectionMarkdown(section) {
  return `## ${section.title}\n\n${section.body}`.trim();
}

function sectionsMarkdown(sections) {
  return sections.map(sectionMarkdown).join("\n\n").trim();
}

function parseStepTitle(title) {
  const match = title.match(/^Step\s+(\d+):\s*(.+)$/);
  if (!match) return null;

  return {
    number: Number(match[1]),
    title: match[2].trim(),
  };
}

function estimateMinutes(total, introCount, stepCount, wrapCount) {
  const overview = Math.max(5, Math.round(total * 0.15));
  const wrap = wrapCount ? Math.max(5, Math.round(total * 0.1)) : 0;
  const remaining = Math.max(total - overview - wrap, stepCount);
  const perStep = stepCount ? Math.max(5, Math.round(remaining / stepCount)) : 5;

  return {
    overview,
    perStep,
    wrap,
  };
}

function chapterToMicroSteps(part) {
  const cleaned = stripRelatedDocuments(part.content);
  const body = cleaned.replace(/^# .*\n+/, "").trim();
  const sections = splitH2Sections(body);

  const introSections = [];
  const stepSections = [];
  const tailSections = [];
  let reachedSteps = false;

  sections.forEach((section) => {
    const parsedStep = parseStepTitle(section.title);
    if (parsedStep) {
      reachedSteps = true;
      stepSections.push({ ...section, parsedStep });
      return;
    }

    if (!reachedSteps) {
      introSections.push(section);
      return;
    }

    tailSections.push(section);
  });

  const timing = estimateMinutes(
    part.estimated_minutes,
    introSections.length ? 1 : 0,
    stepSections.length,
    tailSections.length ? 1 : 0,
  );

  const localTotal =
    (introSections.length ? 1 : 0) +
    stepSections.length +
    (tailSections.length ? 1 : 0);

  const microSteps = [];

  if (introSections.length) {
    microSteps.push({
      id: `${part.id}-overview`,
      title: "Start Here",
      short_label: "Overview",
      category: part.category,
      estimated_minutes: timing.overview,
      focus: part.focus,
      content_markdown: sectionsMarkdown(introSections),
      part_id: part.id,
      part_number: part.part_number,
      part_title: part.title,
      part_heading: `Part ${part.part_number} — ${part.title}`,
      part_step_index: 1,
      part_step_total: localTotal,
    });
  }

  stepSections.forEach((section, index) => {
    microSteps.push({
      id: `${part.id}-step-${section.parsedStep.number}`,
      title: section.parsedStep.title,
      short_label: `Step ${section.parsedStep.number}`,
      category: part.category,
      estimated_minutes: timing.perStep,
      focus: part.focus,
      content_markdown: section.body,
      part_id: part.id,
      part_number: part.part_number,
      part_title: part.title,
      part_heading: `Part ${part.part_number} — ${part.title}`,
      part_step_index: (introSections.length ? 1 : 0) + index + 1,
      part_step_total: localTotal,
    });
  });

  if (tailSections.length) {
    microSteps.push({
      id: `${part.id}-wrap`,
      title: "Troubleshooting + Capture",
      short_label: "Wrap Up",
      category: part.category,
      estimated_minutes: timing.wrap,
      focus: part.focus,
      content_markdown: sectionsMarkdown(tailSections),
      part_id: part.id,
      part_number: part.part_number,
      part_title: part.title,
      part_heading: `Part ${part.part_number} — ${part.title}`,
      part_step_index: localTotal,
      part_step_total: localTotal,
    });
  }

  return microSteps;
}

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
  step_label: "Lesson Step",
  description:
    "A true hand-holding tutorial for a 144-bar modern UKG / speed-garage original. The site now splits the build into part overviews plus one guided lesson step for each authored action block, so the lesson can walk through the session one small decision at a time instead of dumping an entire chapter at once.",
  what_youll_learn: [
    "How to set up the full Ableton session and label, color, route, and organize it before any writing starts",
    "How to build every lane on separate tracks so later mixing and troubleshooting stay visible",
    "How to enter exact MIDI notes and timings for bass, chords, hook, and answer instead of guessing from chord symbols",
    "How to assemble the full 144-bar arrangement with section-by-section growth rules",
    "How to clear the named blockers during the premix instead of hoping the mix fixes them",
  ],
  steps: PARTS.flatMap(chapterToMicroSteps),
};

export default original17;
