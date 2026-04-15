import { builds } from "../content/guided-builds";

function suggestBuild(stepsComplete) {
  // First incomplete rep (beginner first, then intermediate)
  const reps = builds.filter((b) => b.build_type === "rep");
  const incomplete = reps.find((b) => stepsComplete(b.id) < b.steps.length);
  if (incomplete) return incomplete;

  // All reps done — suggest first incomplete spinoff
  const spinoffs = builds.filter((b) => b.build_type === "spinoff");
  const incompleteSpinoff = spinoffs.find(
    (b) => stepsComplete(b.id) < b.steps.length,
  );
  if (incompleteSpinoff) return incompleteSpinoff;

  // Everything done — suggest the first build as a revisit
  return builds[0] ?? null;
}

const difficultyStyles = {
  beginner: "text-green-400",
  intermediate: "text-yellow-400",
  advanced: "text-red-400",
};

export default function DailyPractice({
  onSelect,
  stepsComplete,
  streak,
  practicedToday,
  recordPractice,
}) {
  const suggested = suggestBuild(stepsComplete);

  if (!suggested) return null;

  const done = stepsComplete(suggested.id);
  const total = suggested.steps.length;
  const started = done > 0;

  const handleStart = () => {
    recordPractice();
    onSelect(suggested);
  };

  return (
    <div className="mb-8 p-5 bg-zinc-900 border border-zinc-800 rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xs font-mono text-zinc-400 uppercase tracking-wider">
          Today's practice
        </h2>
        {streak > 0 && (
          <span className="text-xs font-mono text-zinc-500">
            {streak} day streak{practicedToday ? " ✓" : ""}
          </span>
        )}
      </div>

      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span
              className={`text-xs font-mono ${difficultyStyles[suggested.difficulty] ?? "text-zinc-500"}`}
            >
              {suggested.difficulty}
            </span>
            <span className="text-xs font-mono text-zinc-600">
              {suggested.bpm} BPM · {suggested.key}
            </span>
          </div>
          <h3 className="font-mono font-bold text-zinc-100 mb-1">
            {suggested.title}
          </h3>
          <p className="text-xs text-zinc-500 line-clamp-2">
            {suggested.description}
          </p>
          {started && (
            <p className="text-xs font-mono text-zinc-600 mt-2">
              {done}/{total} steps done — pick up where you left off
            </p>
          )}
        </div>

        <button
          onClick={handleStart}
          className="shrink-0 px-4 py-2 bg-zinc-100 text-zinc-900 hover:bg-white rounded font-mono text-sm font-bold transition-colors"
        >
          {started ? "Continue →" : "Start →"}
        </button>
      </div>
    </div>
  );
}
