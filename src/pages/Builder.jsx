import { useState } from "react";
import { useLocation } from "react-router-dom";
import BuildSelector from "../components/BuildSelector";
import BuildStep from "../components/BuildStep";
import DailyPractice from "../components/DailyPractice";
import { entryById } from "../content/cheatsheet";
import { buildById } from "../content/guided-builds";
import { useProgress } from "../hooks/useProgress";
import { usePracticeStreak } from "../hooks/usePracticeStreak";

export default function Builder() {
  const location = useLocation();
  const initialBuildId = location.state?.buildId;
  const initialBuild = initialBuildId
    ? (buildById[initialBuildId] ?? null)
    : null;

  const [build, setBuild] = useState(initialBuild);
  const [stepIndex, setStepIndex] = useState(0);
  const [refEntry, setRefEntry] = useState(null);

  const {
    markStep,
    unmarkStep,
    stepsComplete,
    isBuildComplete,
    isStepComplete,
  } = useProgress();

  const { streak, practicedToday, recordPractice } = usePracticeStreak();

  const handleSelect = (b) => {
    setBuild(b);
    setStepIndex(0);
    recordPractice();
  };

  if (!build)
    return (
      <div>
        <DailyPractice
          onSelect={handleSelect}
          stepsComplete={stepsComplete}
          streak={streak}
          practicedToday={practicedToday}
          recordPractice={recordPractice}
        />
        <BuildSelector
          onSelect={handleSelect}
          stepsComplete={stepsComplete}
          isBuildComplete={isBuildComplete}
        />
      </div>
    );

  const step = build.steps[stepIndex];
  const stepDone = isStepComplete(build.id, step.id);

  return (
    <div className="flex gap-8">
      <div className="flex-1">
        <button
          onClick={() => {
            setBuild(null);
            setRefEntry(null);
          }}
          className="text-xs font-mono text-zinc-500 hover:text-zinc-300 mb-6 block"
        >
          ← All builds
        </button>

        {/* Build header */}
        <div className="mb-6 p-4 bg-zinc-900 rounded-lg">
          <p className="text-xs font-mono text-zinc-600 mb-1">
            {build.build_type}
          </p>
          <h2 className="font-mono font-bold text-zinc-100">{build.title}</h2>
          <div className="flex items-center gap-3 mt-2">
            <div className="flex gap-3 text-xs font-mono text-zinc-500">
              <span>{build.bpm} BPM</span>
              <span>{build.key}</span>
              <span>~{build.estimated_time_mins}min</span>
            </div>
            {isBuildComplete(build) ? (
              <span className="ml-auto text-xs font-mono text-green-400 bg-green-900/30 px-2 py-0.5 rounded">
                ✓ Complete
              </span>
            ) : (
              <span className="ml-auto text-xs font-mono text-zinc-600">
                {stepsComplete(build.id)}/{build.steps.length} steps
              </span>
            )}
          </div>
        </div>

        <BuildStep
          step={step}
          stepNumber={stepIndex + 1}
          total={build.steps.length}
          buildId={build.id}
          isComplete={stepDone}
          onMark={() =>
            stepDone
              ? unmarkStep(build.id, step.id)
              : markStep(build.id, step.id)
          }
          onNext={() =>
            setStepIndex((i) => Math.min(i + 1, build.steps.length - 1))
          }
          onPrev={() => setStepIndex((i) => Math.max(i - 1, 0))}
          onOpenRef={(id) => setRefEntry(entryById[id] || null)}
        />
      </div>

      {refEntry && (
        <div className="w-80 shrink-0 p-5 bg-zinc-900 border border-zinc-800 rounded-lg h-fit sticky top-8">
          <div className="flex justify-between items-start mb-3">
            <h3 className="font-mono font-bold text-zinc-100 text-sm">
              {refEntry.title}
            </h3>
            <button
              onClick={() => setRefEntry(null)}
              className="text-zinc-600 hover:text-zinc-400 font-mono"
            >
              ×
            </button>
          </div>
          <p className="text-xs text-zinc-500 mb-3">{refEntry.summary}</p>
          <ol className="space-y-2">
            {refEntry.steps.map((s, i) => (
              <li key={i} className="text-zinc-300 text-xs flex gap-2">
                <span className="text-zinc-600 min-w-[16px]">{i + 1}.</span>
                {s}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}
