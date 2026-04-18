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
      <div className="hidden xl:block w-72 shrink-0">
        <div className="sticky top-8 p-4 bg-zinc-900 border border-zinc-800 rounded-lg">
          <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
            Lesson Outline
          </h3>
          <div className="space-y-2 max-h-[75vh] overflow-auto pr-1">
            {build.steps.map((buildStep, index) => {
              const active = index === stepIndex;
              const done = isStepComplete(build.id, buildStep.id);
              return (
                <button
                  key={buildStep.id}
                  onClick={() => setStepIndex(index)}
                  className={`w-full text-left p-3 rounded border transition-colors ${
                    active
                      ? "border-zinc-500 bg-zinc-800"
                      : "border-zinc-800 bg-zinc-950 hover:border-zinc-700"
                  }`}
                >
                  <div className="flex items-start justify-between gap-3 mb-1">
                    <span className="text-[11px] font-mono text-zinc-500">
                      Step {index + 1}
                    </span>
                    {done && (
                      <span className="text-[11px] font-mono text-green-400">
                        done
                      </span>
                    )}
                  </div>
                  <div className="text-sm font-mono text-zinc-100 leading-snug mb-1">
                    {buildStep.title}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="text-[11px] font-mono text-zinc-600 uppercase">
                      {buildStep.category}
                    </span>
                    {buildStep.estimated_minutes && (
                      <span className="text-[11px] font-mono text-zinc-600">
                        ~{buildStep.estimated_minutes} min
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <div className="flex-1 min-w-0">
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
          onNext={() => {
            if (stepIndex === build.steps.length - 1) {
              setBuild(null);
              setRefEntry(null);
            } else {
              setStepIndex((i) => i + 1);
            }
          }}
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
