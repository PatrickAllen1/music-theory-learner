export default function BuildStep({
  step,
  stepNumber,
  total,
  buildId,
  isComplete,
  onMark,
  onNext,
  onPrev,
  onOpenRef,
}) {
  return (
    <div className="max-w-2xl">
      <div className="flex justify-between items-center mb-6">
        <span className="text-xs font-mono text-zinc-500">
          Step {stepNumber} of {total}
        </span>
        <span className="text-xs font-mono text-zinc-600 uppercase">
          {step.category}
        </span>
      </div>

      <h2 className="text-xl font-mono font-bold mb-4">{step.title}</h2>

      <div className="p-5 bg-zinc-900 border border-zinc-700 rounded-lg mb-6">
        <p className="text-zinc-200 leading-relaxed">{step.instruction}</p>
      </div>

      <div className="mb-6">
        <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-2">
          Why this works
        </h3>
        <p className="text-zinc-400 text-sm leading-relaxed">{step.why}</p>
      </div>

      {step.tip && (
        <div className="px-4 py-3 bg-zinc-900 border-l-2 border-zinc-600 rounded mb-6">
          <p className="text-xs font-mono text-zinc-400">→ {step.tip}</p>
        </div>
      )}

      {step.splice_search && (
        <div className="mb-6">
          <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-2">
            Splice Search
          </h3>
          <span className="font-mono text-sm text-zinc-300 bg-zinc-900 px-3 py-1 rounded">
            "{step.splice_search}"
          </span>
        </div>
      )}

      {step.ableton_cheatsheet_id && (
        <button
          onClick={() => onOpenRef(step.ableton_cheatsheet_id)}
          className="text-xs font-mono text-zinc-400 hover:text-zinc-200 border border-zinc-700 hover:border-zinc-500 px-3 py-2 rounded mb-6 block transition-colors"
        >
          → Open Ableton reference: {step.ableton_cheatsheet_id}
        </button>
      )}

      <div className="flex items-center gap-3 mt-8">
        {stepNumber > 1 && (
          <button
            onClick={onPrev}
            className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded font-mono text-sm transition-colors"
          >
            ← Back
          </button>
        )}
        <button
          onClick={onNext}
          className="px-6 py-2 bg-zinc-100 text-zinc-900 hover:bg-white rounded font-mono text-sm font-bold transition-colors"
        >
          {stepNumber === total ? "Finish" : "Next step →"}
        </button>

        <button
          onClick={onMark}
          className={`ml-auto flex items-center gap-2 text-xs font-mono px-3 py-2 rounded border transition-colors ${
            isComplete
              ? "border-green-700 bg-green-900/30 text-green-400"
              : "border-zinc-700 text-zinc-500 hover:border-zinc-500 hover:text-zinc-300"
          }`}
        >
          <span
            className={`w-3.5 h-3.5 rounded-sm border flex items-center justify-center shrink-0 ${
              isComplete ? "bg-green-600 border-green-600" : "border-zinc-600"
            }`}
          >
            {isComplete && (
              <svg
                viewBox="0 0 10 10"
                className="w-2.5 h-2.5 text-white"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <polyline points="1.5,5 4,7.5 8.5,2" />
              </svg>
            )}
          </span>
          {isComplete ? "Done" : "Mark done"}
        </button>
      </div>
    </div>
  );
}
