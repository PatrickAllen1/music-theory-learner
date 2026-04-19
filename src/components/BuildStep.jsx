/* eslint-disable react/prop-types */
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const SECTION_TREATMENTS = {
  action: {
    eyebrow: "Do this",
    className: "border-sky-500/30 bg-sky-950/20",
    heading: "text-sky-200",
    accent: "bg-sky-400",
  },
  why: {
    eyebrow: "Reason",
    className: "border-emerald-500/30 bg-emerald-950/20",
    heading: "text-emerald-200",
    accent: "bg-emerald-400",
  },
  rule: {
    eyebrow: "Rule",
    className: "border-amber-500/30 bg-amber-950/20",
    heading: "text-amber-200",
    accent: "bg-amber-400",
  },
  "expected answer": {
    eyebrow: "Checkpoint",
    className: "border-green-500/30 bg-green-950/20",
    heading: "text-green-200",
    accent: "bg-green-400",
  },
  screenshot: {
    eyebrow: "Capture",
    className: "border-blue-500/30 bg-blue-950/20",
    heading: "text-blue-200",
    accent: "bg-blue-400",
  },
  "screenshot set": {
    eyebrow: "Capture",
    className: "border-blue-500/30 bg-blue-950/20",
    heading: "text-blue-200",
    accent: "bg-blue-400",
  },
  "visual requirement": {
    eyebrow: "Visual check",
    className: "border-violet-500/30 bg-violet-950/20",
    heading: "text-violet-200",
    accent: "bg-violet-400",
  },
  troubleshooting: {
    eyebrow: "Fix path",
    className: "border-rose-500/30 bg-rose-950/20",
    heading: "text-rose-200",
    accent: "bg-rose-400",
  },
};

const DEFAULT_SECTION_TREATMENT = {
  eyebrow: "Detail",
  className: "border-zinc-800 bg-zinc-950/70",
  heading: "text-zinc-100",
  accent: "bg-zinc-500",
};

function normalizeHeading(title) {
  return title.trim().toLowerCase().replace(/:$/, "");
}

function getSectionTreatment(title) {
  const normalized = normalizeHeading(title);
  return SECTION_TREATMENTS[normalized] ?? DEFAULT_SECTION_TREATMENT;
}

function splitByH3(markdown) {
  const regex = /^### (.+)$/gm;
  const matches = [...markdown.matchAll(regex)];

  if (matches.length === 0) {
    return {
      intro: markdown.trim(),
      sections: [],
    };
  }

  const intro = markdown.slice(0, matches[0].index).trim();
  const sections = matches.map((match, index) => {
    const title = match[1].trim();
    const bodyStart = match.index + match[0].length;
    const bodyEnd =
      index + 1 < matches.length ? matches[index + 1].index : markdown.length;

    return {
      title,
      body: markdown.slice(bodyStart, bodyEnd).trim(),
    };
  });

  return { intro, sections };
}

const markdownComponents = {
  h1: ({ children }) => (
    <h2 className="mb-6 text-2xl font-mono font-bold tracking-tight text-zinc-50">
      {children}
    </h2>
  ),
  h2: ({ children }) => (
    <h3 className="mb-4 mt-8 rounded-xl border border-zinc-800 bg-zinc-900/70 px-4 py-3 text-sm font-mono font-semibold uppercase tracking-[0.12em] text-zinc-300 first:mt-0">
      {children}
    </h3>
  ),
  h3: ({ children }) => (
    <h4 className="mb-3 mt-6 text-base font-mono font-semibold text-zinc-100">
      {children}
    </h4>
  ),
  h4: ({ children }) => (
    <h5 className="mb-2 mt-5 text-sm font-mono font-semibold text-zinc-200">
      {children}
    </h5>
  ),
  p: ({ children }) => (
    <p className="mb-4 max-w-3xl text-[15px] leading-7 text-zinc-300 last:mb-0">
      {children}
    </p>
  ),
  ul: ({ children }) => (
    <ul className="mb-5 max-w-3xl list-disc space-y-2 pl-6 text-[15px] leading-7 text-zinc-300 marker:text-zinc-500">
      {children}
    </ul>
  ),
  ol: ({ children }) => (
    <ol className="mb-5 max-w-3xl list-decimal space-y-3 pl-6 text-[15px] leading-7 text-zinc-300 marker:font-mono marker:text-zinc-500">
      {children}
    </ol>
  ),
  li: ({ children }) => <li className="pl-1 leading-7">{children}</li>,
  strong: ({ children }) => (
    <strong className="font-semibold text-zinc-100">{children}</strong>
  ),
  code: ({ className, children }) => {
    const text = String(children).replace(/\n$/, "");
    const isInline = !className && !text.includes("\n");

    return isInline ? (
      <code className="rounded-md border border-zinc-700/80 bg-zinc-900/90 px-1.5 py-0.5 font-mono text-[0.9em] text-zinc-100">
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
    <pre className="mb-5 max-w-full overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-4">
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
    <blockquote className="mb-5 max-w-3xl rounded-r-lg border-l-2 border-zinc-700 bg-zinc-900/50 py-1 pl-4 text-[15px] leading-7 text-zinc-400">
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
};

function MarkdownContent({ children }) {
  if (!children) return null;

  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
      {children}
    </ReactMarkdown>
  );
}

function LessonSection({ title, body }) {
  const treatment = getSectionTreatment(title);

  return (
    <section
      className={`rounded-2xl border px-5 py-5 shadow-[0_0_0_1px_rgba(255,255,255,0.015)] ${treatment.className}`}
    >
      <div className="mb-4 flex items-center gap-3">
        <span className={`h-2.5 w-2.5 rounded-full ${treatment.accent}`} />
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-zinc-500">
            {treatment.eyebrow}
          </p>
          <h3 className={`font-mono text-lg font-bold ${treatment.heading}`}>
            {title}
          </h3>
        </div>
      </div>
      <MarkdownContent>{body}</MarkdownContent>
    </section>
  );
}

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
  const { intro, sections } = splitByH3(content);

  return (
    <div className="mb-8 space-y-5 rounded-3xl border border-zinc-800/80 bg-zinc-950/80 p-4 shadow-[0_0_0_1px_rgba(255,255,255,0.01)] sm:p-6">
      {intro && (
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/35 px-5 py-5">
          <MarkdownContent>{intro}</MarkdownContent>
        </div>
      )}

      {sections.length > 0 ? (
        <div className="space-y-4">
          {sections.map((section) => (
            <LessonSection
              key={`${section.title}-${section.body.slice(0, 24)}`}
              title={section.title}
              body={section.body}
            />
          ))}
        </div>
      ) : (
        !intro && <MarkdownContent>{content}</MarkdownContent>
      )}
    </div>
  );
}

export default function BuildStep({
  step,
  stepNumber,
  total,
  isComplete,
  onMark,
  onNext,
  onPrev,
  onOpenRef,
  stepLabel = "Step",
}) {
  const hasMarkdown = Boolean(step.content_markdown);

  return (
    <div className="max-w-5xl">
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

      {hasMarkdown && (
        <div className="mb-5 rounded-2xl border border-zinc-800 bg-zinc-950/80 px-4 py-3">
          <p className="text-sm leading-6 text-zinc-400">
            Work through this page from top to bottom. The blue{" "}
            <span className="font-mono text-sky-200">Action</span> cards are
            the clicks and placements; the green{" "}
            <span className="font-mono text-emerald-200">Why</span> cards
            explain the design reason; checkpoint and screenshot cards tell you
            what must be true before moving on.
          </p>
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
            Search term: {step.splice_search}
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
