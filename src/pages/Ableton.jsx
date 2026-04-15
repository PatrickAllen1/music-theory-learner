import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { entries } from "../content/cheatsheet";
import { buildById } from "../content/guided-builds";

export default function Ableton() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");

  const filtered = entries.filter(
    (e) =>
      query === "" ||
      e.title.toLowerCase().includes(query.toLowerCase()) ||
      e.tags.some((t) => t.includes(query.toLowerCase())),
  );

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-mono font-bold mb-6">Ableton Cheatsheet</h1>
      <input
        type="text"
        placeholder="Search — sidechain, EQ, drum rack..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full px-4 py-2 bg-zinc-900 border border-zinc-700 rounded font-mono text-sm text-zinc-100 placeholder-zinc-600 mb-6 focus:outline-none focus:border-zinc-500"
      />
      <div className="space-y-6">
        {filtered.map((entry) => (
          <div
            key={entry.id}
            className="p-5 bg-zinc-900 border border-zinc-800 rounded-lg"
          >
            <div className="flex justify-between items-start mb-2">
              <h2 className="font-mono font-bold text-zinc-100">
                {entry.title}
              </h2>
              <span className="text-xs font-mono text-zinc-600">
                {entry.category}
              </span>
            </div>
            <p className="text-zinc-400 text-sm mb-4">{entry.summary}</p>
            {entry.images?.length > 0 && (
              <div className="mb-4 space-y-3">
                {entry.images.map((img, i) => (
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
            <ol className="space-y-2">
              {entry.steps.map((step, i) => (
                <li key={i} className="text-zinc-300 text-sm flex gap-3">
                  <span className="text-zinc-600 font-mono min-w-[20px]">
                    {i + 1}.
                  </span>
                  {step}
                </li>
              ))}
            </ol>
            {entry.tips?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-zinc-800 space-y-1">
                {entry.tips.map((tip, i) => (
                  <p key={i} className="text-xs text-zinc-500 font-mono">
                    → {tip}
                  </p>
                ))}
              </div>
            )}
            {entry.practice_rep_id && buildById[entry.practice_rep_id] && (
              <div className="mt-4 pt-4 border-t border-zinc-800">
                <button
                  onClick={() =>
                    navigate("/builder", {
                      state: { buildId: entry.practice_rep_id },
                    })
                  }
                  className="text-xs font-mono text-zinc-100 bg-zinc-700 hover:bg-zinc-600 px-3 py-1.5 rounded transition-colors"
                >
                  Try it in a build → {buildById[entry.practice_rep_id].title}
                </button>
              </div>
            )}
            {!entry.practice_rep_id && entry.practice_hint && (
              <div className="mt-4 pt-4 border-t border-zinc-800">
                <p className="text-xs font-mono text-zinc-500">
                  → Practice: {entry.practice_hint}
                </p>
              </div>
            )}
          </div>
        ))}
        {filtered.length === 0 && (
          <p className="text-zinc-600 font-mono text-sm">
            No entries match "{query}"
          </p>
        )}
      </div>
    </div>
  );
}
