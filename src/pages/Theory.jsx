import { useState } from "react";
import { scales, chords, rhythms } from "../content/theory";

const TABS = ["Scales", "Chords", "Rhythms"];

function ScaleCard({ entry }) {
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
        </div>
      )}
    </div>
  );
}

function ChordCard({ entry }) {
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
        </div>
      )}
    </div>
  );
}

function RhythmCard({ entry }) {
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
        </div>
      )}
    </div>
  );
}

export default function Theory() {
  const [tab, setTab] = useState("Scales");

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-mono font-bold mb-6">Theory Reference</h1>

      <div className="flex gap-2 mb-6">
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

      <div className="space-y-3">
        {tab === "Scales" &&
          scales.map((s) => <ScaleCard key={s.id} entry={s} />)}
        {tab === "Chords" &&
          chords.map((c) => <ChordCard key={c.id} entry={c} />)}
        {tab === "Rhythms" &&
          rhythms.map((r) => <RhythmCard key={r.id} entry={r} />)}
      </div>
    </div>
  );
}
