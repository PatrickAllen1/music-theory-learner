import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function BulletSection({ title, items, accent = "text-zinc-500" }) {
  if (!items || items.length === 0) return null;

  return (
    <div className="mb-6">
      <h3
        className={`text-xs font-mono uppercase tracking-wider mb-2 ${accent}`}
      >
        {title}
      </h3>
      <ul className="space-y-2">
        {items.map((item, index) => (
          <li key={index} className="flex gap-3 text-sm leading-relaxed">
            <span className="text-zinc-600 font-mono shrink-0">→</span>
            <span className="text-zinc-300">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function MarkdownLesson({ content }) {
  if (!content) return null;

  return (
    <div className="mb-8 rounded-2xl border border-zinc-800/80 bg-zinc-950/80 px-6 py-6 shadow-[0_0_0_1px_rgba(255,255,255,0.01)]">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h2 className="mb-6 text-2xl font-mono font-bold tracking-tight text-zinc-50">
              {children}
            </h2>
          ),
          h2: ({ children }) => (
            <h3 className="mb-4 mt-8 border-t border-zinc-800 pt-5 text-xs font-mono uppercase tracking-[0.18em] text-zinc-500 first:mt-0 first:border-t-0 first:pt-0">
              {children}
            </h3>
          ),
          h3: ({ children }) => (
            <h4 className="mb-3 mt-6 text-base font-mono font-semibold text-zinc-100">
              {children}
            </h4>
          ),
          p: ({ children }) => (
            <p className="mb-4 text-[15px] leading-7 text-zinc-300 last:mb-0">
              {children}
            </p>
          ),
          ul: ({ children }) => (
            <ul className="mb-5 list-disc space-y-2 pl-6 text-[15px] leading-7 text-zinc-300 marker:text-zinc-500">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="mb-5 list-decimal space-y-2 pl-6 text-[15px] leading-7 text-zinc-300 marker:font-mono marker:text-zinc-500">
              {children}
            </ol>
          ),
          li: ({ children }) => <li className="pl-1 leading-7">{children}</li>,
          strong: ({ children }) => (
            <strong className="font-semibold text-zinc-100">{children}</strong>
          ),
          code: ({ node, className, children }) => {
            const text = String(children).replace(/\n$/, "");
            const isInline =
              !className &&
              node?.position?.start?.line === node?.position?.end?.line &&
              !text.includes("\n");

            return isInline ? (
              <code className="rounded-md border border-zinc-800 bg-zinc-900 px-1.5 py-0.5 font-mono text-[0.9em] text-zinc-100">
                {children}
              </code>
            ) : (
              <code
                className={`block font-mono text-sm leading-6 text-zinc-100 ${className ?? ""}`}
              >
                {text}
              </code>
            );
          },
          pre: ({ children }) => (
            <pre className="mb-5 overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-900/80 p-4">
              {children}
            </pre>
          ),
          hr: () => <hr className="my-8 border-zinc-800" />,
          a: ({ href, children }) => {
            if (!href || href.startsWith("/Users/")) {
              return (
                <span className="font-mono text-zinc-300 underline decoration-zinc-700 decoration-dotted underline-offset-2">
                  {children}
                </span>
              );
            }

            return (
              <a
                href={href}
                target="_blank"
                rel="noreferrer"
                className="text-zinc-200 underline decoration-zinc-600 underline-offset-2 hover:text-white"
              >
                {children}
              </a>
            );
          },
          blockquote: ({ children }) => (
            <blockquote className="mb-5 rounded-r-lg border-l-2 border-zinc-700 bg-zinc-900/50 py-1 pl-4 text-[15px] leading-7 text-zinc-400">
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div className="mb-5 overflow-x-auto rounded-xl border border-zinc-800">
              <table className="min-w-full border-collapse text-left text-sm text-zinc-300">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => <thead className="bg-zinc-900/80">{children}</thead>,
          th: ({ children }) => (
            <th className="border-b border-zinc-800 px-3 py-2 font-mono text-xs uppercase tracking-wider text-zinc-400">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border-t border-zinc-800 px-3 py-2 align-top leading-6">
              {children}
            </td>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

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
  stepLabel = "Step",
}) {
  const hasMarkdown = Boolean(step.content_markdown);

  return (
    <div className="max-w-4xl">
      <div className="flex justify-between items-center mb-6">
        <span className="text-xs font-mono text-zinc-500">
          {stepLabel} {stepNumber} of {total}
        </span>
        <span className="text-xs font-mono text-zinc-600 uppercase">
          {step.category}
        </span>
      </div>

      {step.part_heading && (
        <div className="mb-4 rounded-lg border border-zinc-800 bg-zinc-950 px-4 py-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono uppercase tracking-wider text-zinc-500">
              {step.part_heading}
            </span>
            {step.part_step_index && step.part_step_total && (
              <span className="text-xs font-mono text-zinc-600">
                {step.short_label} · {step.part_step_index} of {step.part_step_total}
              </span>
            )}
          </div>
        </div>
      )}

      <h2 className="mb-4 text-2xl font-mono font-bold tracking-tight text-zinc-50">
        {step.title}
      </h2>

      {(step.focus || step.estimated_minutes) && (
        <div className="flex flex-wrap gap-2 mb-4">
          {step.focus && (
            <span className="px-2.5 py-1 bg-zinc-900 border border-zinc-800 rounded text-xs font-mono text-zinc-300">
              Focus: {step.focus}
            </span>
          )}
          {step.estimated_minutes && (
            <span className="px-2.5 py-1 bg-zinc-900 border border-zinc-800 rounded text-xs font-mono text-zinc-500">
              ~{step.estimated_minutes} min
            </span>
          )}
        </div>
      )}

      {step.outcome && (
        <div className="mb-6 px-4 py-3 bg-zinc-900 border border-zinc-800 rounded-lg">
          <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-2">
            End State
          </h3>
          <p className="text-zinc-300 text-sm leading-relaxed">
            {step.outcome}
          </p>
        </div>
      )}

      {step.instruction && (
        <div className="p-5 bg-zinc-900 border border-zinc-700 rounded-lg mb-6">
          <p className="text-zinc-200 leading-relaxed">{step.instruction}</p>
        </div>
      )}

      {hasMarkdown && <MarkdownLesson content={step.content_markdown} />}

      {!hasMarkdown &&
        step.instruction_sections?.map((section, index) => (
        <BulletSection
          key={`${section.title}-${index}`}
          title={section.title}
          items={section.items}
        />
        ))}

      {!hasMarkdown && step.why && (
        <div className="mb-6">
          <h3 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-2">
            Why this works
          </h3>
          <p className="text-zinc-400 text-sm leading-relaxed">{step.why}</p>
        </div>
      )}

      {!hasMarkdown && (
        <>
          <BulletSection title="Checklist" items={step.checklist} />
          <BulletSection
            title="Verify Before Moving On"
            items={step.verify}
            accent="text-green-500"
          />
          <BulletSection
            title="Common Mistakes"
            items={step.common_mistakes}
            accent="text-amber-500"
          />
          <BulletSection
            title="Save These Artifacts"
            items={step.save_artifacts}
            accent="text-blue-500"
          />
        </>
      )}

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

      {step.images && step.images.length > 0 && (
        <div className="mb-6 space-y-3">
          {step.images.map((img, i) => (
            <figure
              key={i}
              className="bg-zinc-900 rounded-lg overflow-hidden border border-zinc-800"
            >
              <img
                src={img.src}
                alt={img.caption}
                className="w-full object-contain max-h-72"
              />
              {img.caption && (
                <figcaption className="px-3 py-2 text-xs font-mono text-zinc-500">
                  {img.caption}
                </figcaption>
              )}
            </figure>
          ))}
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
