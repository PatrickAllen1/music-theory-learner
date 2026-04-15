import { useState } from "react";
import { builds } from "../content/guided-builds";

const TABS = ["Reps", "Spinoffs", "Originals"];

const difficultyStyles = {
  beginner: "bg-green-900/40 text-green-400",
  intermediate: "bg-yellow-900/40 text-yellow-400",
  advanced: "bg-red-900/40 text-red-400",
};

const spinoffLevelStyles = {
  entry: "bg-zinc-700 text-zinc-300",
  mid: "bg-blue-900/40 text-blue-400",
  full: "bg-purple-900/40 text-purple-400",
};

function ProgressBar({ done, total }) {
  const pct = total === 0 ? 0 : Math.round((done / total) * 100);
  const complete = done >= total;
  return (
    <div className="mt-3">
      {complete ? (
        <span className="text-xs font-mono text-green-400 bg-green-900/30 px-2 py-0.5 rounded">
          ✓ Complete
        </span>
      ) : (
        <div className="flex items-center gap-2">
          <div className="flex-1 h-1 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-zinc-500 rounded-full transition-all"
              style={{ width: `${pct}%` }}
            />
          </div>
          <span className="text-xs font-mono text-zinc-600 shrink-0">
            {done}/{total}
          </span>
        </div>
      )}
    </div>
  );
}

export default function BuildSelector({
  onSelect,
  stepsComplete,
  isBuildComplete,
}) {
  const [tab, setTab] = useState("Reps");
  const [repFilter, setRepFilter] = useState("beginner");

  const reps = builds.filter((b) => b.build_type === "rep");
  const spinoffs = builds.filter((b) => b.build_type === "spinoff");
  const originals = builds.filter((b) => b.build_type === "original");

  const visibleReps = reps.filter((b) => b.difficulty === repFilter);

  const visible =
    tab === "Reps" ? visibleReps : tab === "Spinoffs" ? spinoffs : originals;

  return (
    <div>
      <h1 className="text-2xl font-mono font-bold mb-2">
        Guided Track Builder
      </h1>
      <p className="text-zinc-400 text-sm mb-6">
        Pick a build. Follow the steps. Learn as you go.
      </p>

      {/* Tab bar */}
      <div className="flex gap-2 mb-4">
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

      {/* Reps difficulty filter */}
      {tab === "Reps" && (
        <div className="flex gap-2 mb-6">
          {["beginner", "intermediate"].map((d) => (
            <button
              key={d}
              onClick={() => setRepFilter(d)}
              className={`text-xs font-mono px-3 py-1 rounded transition-colors ${
                repFilter === d
                  ? "bg-zinc-700 text-zinc-100"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {d}
            </button>
          ))}
        </div>
      )}

      {/* Build cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {visible.map((build) => (
          <button
            key={build.id}
            onClick={() => onSelect(build)}
            className="text-left p-5 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-600 transition-colors"
          >
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-mono text-zinc-600">
                {build.build_type === "spinoff"
                  ? `spinoff · ${build.spinoff_level}`
                  : build.build_type}
              </span>
              <div className="flex gap-2">
                {build.spinoff_level && (
                  <span
                    className={`text-xs font-mono px-1.5 py-0.5 rounded ${spinoffLevelStyles[build.spinoff_level]}`}
                  >
                    {build.spinoff_level}
                  </span>
                )}
                <span
                  className={`text-xs font-mono px-1.5 py-0.5 rounded ${difficultyStyles[build.difficulty] ?? "bg-zinc-800 text-zinc-400"}`}
                >
                  {build.difficulty}
                </span>
              </div>
            </div>

            <h3 className="font-mono font-bold text-zinc-100 mb-3">
              {build.title}
            </h3>

            <div className="flex gap-3 text-xs font-mono text-zinc-500 mb-3">
              <span>{build.bpm} BPM</span>
              <span>{build.key}</span>
              <span>~{build.estimated_time_mins}min</span>
            </div>

            <ul className="space-y-1">
              {build.what_youll_learn.slice(0, 2).map((item, i) => (
                <li key={i} className="text-xs text-zinc-500 flex gap-2">
                  <span className="text-zinc-700">→</span>
                  {item}
                </li>
              ))}
            </ul>

            <ProgressBar
              done={stepsComplete ? stepsComplete(build.id) : 0}
              total={build.steps.length}
            />
          </button>
        ))}

        {visible.length === 0 && (
          <p className="text-zinc-600 font-mono text-sm col-span-2">
            No builds yet — coming soon.
          </p>
        )}
      </div>
    </div>
  );
}
