import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { scales, chords, rhythms, deepDives } from "../content/theory";
import { buildById } from "../content/guided-builds";

const TABS = ["Scales", "Chords", "Rhythms", "Deep Dives"];

const difficultyStyles = {
  beginner: "bg-green-900/40 text-green-400",
  intermediate: "bg-yellow-900/40 text-yellow-400",
  advanced: "bg-red-900/40 text-red-400",
};

// ─── Existing reference cards ─────────────────────────────────────────────

function PracticePills({ repIds, onPractice }) {
  if (!repIds?.length) return null;
  const reps = repIds.map((id) => buildById[id]).filter(Boolean);
  if (!reps.length) return null;
  return (
    <div className="pt-3 border-t border-zinc-800">
      <p className="text-xs font-mono text-zinc-600 mb-2">practice in:</p>
      <div className="flex gap-2 flex-wrap">
        {reps.map((rep) => (
          <button
            key={rep.id}
            onClick={() => onPractice(rep)}
            className="text-xs font-mono px-2 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-zinc-100 rounded transition-colors"
          >
            → {rep.title}
          </button>
        ))}
      </div>
    </div>
  );
}

function ScaleCard({ entry, onPractice }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-lg">
      <button className="w-full text-left" onClick={() => setOpen((o) => !o)}>
        <div className="flex justify-between items-baseline">
          <span className="font-mono font-bold text-zinc-100">
            {entry.name}
          </span>
          <span className="text-xs font-mono text-zinc-600">{entry.aka}</span>
        </div>
        <p className="text-xs text-zinc-500 mt-1">{entry.feel}</p>
      </button>
      {open && (
        <div className="mt-4 space-y-3 border-t border-zinc-800 pt-4">
          <div className="flex gap-2 flex-wrap">
            {entry.notes_from_root.map((n, i) => (
              <span
                key={i}
                className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-300"
              >
                +{n}
              </span>
            ))}
          </div>
          <p className="text-xs font-mono text-zinc-500">
            Formula: {entry.interval_formula}
          </p>
          <p className="text-xs text-zinc-400 leading-relaxed">
            {entry.analytical_note}
          </p>
          <div>
            <p className="text-xs font-mono text-zinc-600 mb-1">heard in:</p>
            <ul className="space-y-0.5">
              {entry.examples.map((ex, i) => (
                <li key={i} className="text-xs text-zinc-500">
                  — {ex}
                </li>
              ))}
            </ul>
          </div>
          <div className="flex gap-2 flex-wrap">
            {entry.common_keys.map((k, i) => (
              <span
                key={i}
                className="px-2 py-0.5 bg-zinc-800 rounded text-xs font-mono text-zinc-500"
              >
                {k}
              </span>
            ))}
          </div>
          <PracticePills
            repIds={entry.linked_rep_ids}
            onPractice={onPractice}
          />
        </div>
      )}
    </div>
  );
}

function ChordCard({ entry, onPractice }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-lg">
      <button className="w-full text-left" onClick={() => setOpen((o) => !o)}>
        <div className="flex justify-between items-baseline">
          <span className="font-mono font-bold text-zinc-100">
            {entry.name}
          </span>
          <span className="text-xs font-mono text-zinc-600">
            {entry.symbol}
          </span>
        </div>
        <p className="text-xs text-zinc-500 mt-1">{entry.feel}</p>
      </button>
      {open && (
        <div className="mt-4 space-y-3 border-t border-zinc-800 pt-4">
          {entry.intervals?.length > 0 && (
            <div className="flex gap-2 flex-wrap">
              {entry.intervals.map((n, i) => (
                <span
                  key={i}
                  className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-300"
                >
                  +{n}
                  {entry.interval_names?.[i] && (
                    <span className="text-zinc-600 ml-1">
                      {entry.interval_names[i]}
                    </span>
                  )}
                </span>
              ))}
            </div>
          )}
          <p className="text-xs text-zinc-400 leading-relaxed">
            {entry.analytical_note}
          </p>
          <div>
            <p className="text-xs font-mono text-zinc-600 mb-1">heard in:</p>
            <ul className="space-y-0.5">
              {entry.examples.map((ex, i) => (
                <li key={i} className="text-xs text-zinc-500">
                  — {ex}
                </li>
              ))}
            </ul>
          </div>
          {entry.in_progressions?.length > 0 && (
            <div>
              <p className="text-xs font-mono text-zinc-600 mb-1">
                in progressions:
              </p>
              <ul className="space-y-0.5">
                {entry.in_progressions.map((p, i) => (
                  <li key={i} className="text-xs font-mono text-zinc-500">
                    {p}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <PracticePills
            repIds={entry.linked_rep_ids}
            onPractice={onPractice}
          />
        </div>
      )}
    </div>
  );
}

function RhythmCard({ entry, onPractice }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-lg">
      <button className="w-full text-left" onClick={() => setOpen((o) => !o)}>
        <div className="flex justify-between items-baseline">
          <span className="font-mono font-bold text-zinc-100">
            {entry.name}
          </span>
          <span className="text-xs font-mono text-zinc-600">
            {entry.bpm_range} BPM
          </span>
        </div>
        <p className="text-xs text-zinc-500 mt-1">{entry.feel}</p>
      </button>
      {open && (
        <div className="mt-4 space-y-3 border-t border-zinc-800 pt-4">
          <p className="text-xs font-mono text-zinc-400">
            {entry.pattern_description}
          </p>
          {entry.velocity_pattern && (
            <div className="flex gap-2 flex-wrap">
              {entry.velocity_pattern.map((v, i) => (
                <span
                  key={i}
                  className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-300"
                >
                  {v}
                </span>
              ))}
            </div>
          )}
          <p className="text-xs text-zinc-400 leading-relaxed">
            {entry.analytical_note}
          </p>
          <div>
            <p className="text-xs font-mono text-zinc-600 mb-1">heard in:</p>
            <ul className="space-y-0.5">
              {entry.examples.map((ex, i) => (
                <li key={i} className="text-xs text-zinc-500">
                  — {ex}
                </li>
              ))}
            </ul>
          </div>
          <PracticePills
            repIds={entry.linked_rep_ids}
            onPractice={onPractice}
          />
        </div>
      )}
    </div>
  );
}

// ─── Deep Dive components ──────────────────────────────────────────────────

function DeepDiveCard({ entry, onOpen }) {
  return (
    <button
      onClick={() => onOpen(entry)}
      className="text-left p-5 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-600 transition-colors w-full"
    >
      <div className="flex justify-between items-start mb-2">
        <span
          className={`text-xs font-mono px-1.5 py-0.5 rounded ${difficultyStyles[entry.difficulty] ?? "bg-zinc-800 text-zinc-400"}`}
        >
          {entry.difficulty}
        </span>
        <span className="text-xs font-mono text-zinc-600">
          {entry.read_time_mins} min read
        </span>
      </div>
      <h3 className="font-mono font-bold text-zinc-100 mb-1">{entry.title}</h3>
      <p className="text-xs text-zinc-500 leading-relaxed mb-3">
        {entry.subtitle}
      </p>
      <div className="flex gap-2 flex-wrap">
        {entry.track_references.map((ref) => (
          <span
            key={ref}
            className="text-xs font-mono px-2 py-0.5 bg-zinc-800 text-zinc-400 rounded"
          >
            {ref}
          </span>
        ))}
      </div>
    </button>
  );
}

function ListeningCue({ cue }) {
  return (
    <div className="my-4 px-4 py-3 bg-zinc-900 border-l-2 border-yellow-700 rounded-r">
      <p className="text-xs font-mono text-yellow-600 mb-1">
        → Listen: {cue.track_id} {cue.timestamp}
        {cue.technique && (
          <span className="ml-2 px-1.5 py-0.5 bg-zinc-800 text-zinc-500 rounded text-xs">
            {cue.technique}
          </span>
        )}
      </p>
      <p className="text-xs text-zinc-400 leading-relaxed">
        {cue.what_to_hear}
      </p>
    </div>
  );
}

function MidiPill({ example }) {
  return (
    <div className="mb-3 p-3 bg-zinc-800 rounded">
      <p className="text-xs font-mono text-zinc-400 mb-2">{example.label}</p>
      <div className="flex gap-1.5 flex-wrap mb-2">
        {example.notes.map((n, i) => (
          <span
            key={i}
            className="px-2 py-1 bg-zinc-700 rounded text-xs font-mono text-zinc-200"
          >
            {n}
          </span>
        ))}
      </div>
      <p className="text-xs text-zinc-500">{example.context}</p>
    </div>
  );
}

function PracticeExercise({ exercise, onPractice }) {
  const [hintOpen, setHintOpen] = useState(false);
  const linkedBuild = exercise.linked_rep_id
    ? buildById[exercise.linked_rep_id]
    : null;

  return (
    <div className="p-5 bg-zinc-900 border border-zinc-700 rounded-lg">
      <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
        Practice Exercise
      </h3>
      <p className="text-zinc-200 text-sm leading-relaxed mb-4 whitespace-pre-line">
        {exercise.instruction}
      </p>
      <button
        onClick={() => setHintOpen((o) => !o)}
        className="text-xs font-mono text-zinc-500 hover:text-zinc-300 mb-3 transition-colors"
      >
        {hintOpen ? "▾ Hide answer hint" : "▸ Show answer hint"}
      </button>
      {hintOpen && (
        <p className="text-xs text-zinc-500 leading-relaxed mb-4 pl-3 border-l border-zinc-700 whitespace-pre-line">
          {exercise.answer_hint}
        </p>
      )}
      {linkedBuild && (
        <button
          onClick={() => onPractice(linkedBuild)}
          className="text-xs font-mono text-zinc-100 bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded transition-colors"
        >
          Practice this in the Builder → {linkedBuild.title}
        </button>
      )}
      {exercise.linked_rep_id && !linkedBuild && (
        <p className="text-xs font-mono text-zinc-600">
          Builder rep coming soon: {exercise.linked_rep_id}
        </p>
      )}
    </div>
  );
}

function DeepDiveArticle({ entry, onBack, onPractice }) {
  return (
    <div className="max-w-2xl">
      <button
        onClick={onBack}
        className="text-xs font-mono text-zinc-500 hover:text-zinc-300 mb-8 block transition-colors"
      >
        ← Back to Deep Dives
      </button>

      {/* Header */}
      <div className="mb-8">
        <div className="flex gap-3 items-center mb-3">
          <span
            className={`text-xs font-mono px-1.5 py-0.5 rounded ${difficultyStyles[entry.difficulty] ?? "bg-zinc-800 text-zinc-400"}`}
          >
            {entry.difficulty}
          </span>
          <span className="text-xs font-mono text-zinc-600">
            {entry.read_time_mins} min read
          </span>
        </div>
        <h1 className="text-2xl font-mono font-bold text-zinc-100 mb-2">
          {entry.title}
        </h1>
        <p className="text-zinc-400 leading-relaxed">{entry.subtitle}</p>
      </div>

      {/* Sections */}
      <div className="space-y-8 mb-10">
        {entry.sections.map((section) => (
          <div key={section.id}>
            {section.heading && (
              <h2 className="font-mono font-bold text-zinc-100 text-lg mb-3">
                {section.heading}
              </h2>
            )}
            <div className="text-zinc-300 text-sm leading-relaxed whitespace-pre-line">
              {section.body}
            </div>
            {section.images?.length > 0 && (
              <div className="mt-4 space-y-3">
                {section.images.map((img, i) => (
                  <figure key={i} className="m-0">
                    <img
                      src={img.src}
                      alt={img.caption}
                      className="w-full rounded border border-zinc-800"
                    />
                    {img.caption && (
                      <figcaption className="text-xs text-zinc-600 font-mono mt-1 leading-relaxed">
                        {img.caption}
                      </figcaption>
                    )}
                  </figure>
                ))}
              </div>
            )}
            {/* Listening cues that reference this section — rendered inline after body */}
            {entry.listening_cues
              ?.filter((_, i) => {
                // distribute cues across sections approximately
                const sectionIdx = entry.sections.findIndex(
                  (s) => s.id === section.id,
                );
                return i === sectionIdx;
              })
              .map((cue, i) => (
                <ListeningCue key={i} cue={cue} />
              ))}
          </div>
        ))}
      </div>

      {/* Any remaining listening cues not distributed above */}
      {entry.listening_cues?.length > entry.sections.length && (
        <div className="mb-10">
          <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-4">
            Listening Cues
          </h3>
          {entry.listening_cues.slice(entry.sections.length).map((cue, i) => (
            <ListeningCue key={i} cue={cue} />
          ))}
        </div>
      )}

      {/* MIDI examples */}
      {entry.midi_examples?.length > 0 && (
        <div className="mb-10">
          <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-4">
            MIDI Examples
          </h3>
          {entry.midi_examples.map((ex, i) => (
            <MidiPill key={i} example={ex} />
          ))}
        </div>
      )}

      {/* Practice exercise */}
      {entry.practice_exercise && (
        <div className="mb-8">
          <PracticeExercise
            exercise={entry.practice_exercise}
            onPractice={onPractice}
          />
        </div>
      )}

      {/* Key takeaway */}
      {entry.key_takeaway && (
        <div className="p-4 bg-zinc-900 border-l-2 border-zinc-500 rounded-r">
          <p className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-1">
            Key Takeaway
          </p>
          <p className="text-zinc-200 text-sm leading-relaxed">
            {entry.key_takeaway}
          </p>
        </div>
      )}
    </div>
  );
}

// ─── Main Theory page ──────────────────────────────────────────────────────

export default function Theory() {
  const navigate = useNavigate();
  const [tab, setTab] = useState("Scales");
  const [activeDeepDive, setActiveDeepDive] = useState(null);

  function handlePractice(build) {
    navigate("/builder", { state: { buildId: build.id } });
  }

  if (activeDeepDive) {
    return (
      <div className="max-w-3xl">
        <DeepDiveArticle
          entry={activeDeepDive}
          onBack={() => setActiveDeepDive(null)}
          onPractice={handlePractice}
        />
      </div>
    );
  }

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-mono font-bold mb-6">Theory Reference</h1>

      <div className="flex gap-2 mb-6 flex-wrap">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`text-xs font-mono px-3 py-1.5 rounded transition-colors ${
              tab === t
                ? "bg-zinc-100 text-zinc-900"
                : "bg-zinc-800 text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {tab !== "Deep Dives" && (
        <div className="space-y-3">
          {tab === "Scales" &&
            scales.map((s) => (
              <ScaleCard key={s.id} entry={s} onPractice={handlePractice} />
            ))}
          {tab === "Chords" &&
            chords.map((c) => (
              <ChordCard key={c.id} entry={c} onPractice={handlePractice} />
            ))}
          {tab === "Rhythms" &&
            rhythms.map((r) => (
              <RhythmCard key={r.id} entry={r} onPractice={handlePractice} />
            ))}
        </div>
      )}

      {tab === "Deep Dives" && (
        <div>
          <p className="text-zinc-500 text-sm mb-6">
            Long-form articles on the theory behind the source tracks. Each one
            ends with a practice exercise you can do in the Builder.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {deepDives.map((d) => (
              <DeepDiveCard key={d.id} entry={d} onOpen={setActiveDeepDive} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
