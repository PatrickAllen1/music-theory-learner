import { useState } from "react";
import { tracks } from "../content/tracks";
import TrackCard from "../components/TrackCard";

const DIFFICULTIES = ["all", "beginner", "intermediate", "advanced"];

export default function Library() {
  const [filter, setFilter] = useState("all");

  const visible =
    filter === "all" ? tracks : tracks.filter((t) => t.difficulty === filter);

  return (
    <div>
      <div className="flex items-baseline justify-between mb-6">
        <h1 className="text-2xl font-mono font-bold">Track Library</h1>
        <span className="text-xs font-mono text-zinc-600">
          {visible.length} track{visible.length !== 1 ? "s" : ""}
        </span>
      </div>

      <div className="flex gap-2 mb-6">
        {DIFFICULTIES.map((d) => (
          <button
            key={d}
            onClick={() => setFilter(d)}
            className={`text-xs font-mono px-3 py-1.5 rounded transition-colors ${
              filter === d
                ? "bg-zinc-100 text-zinc-900"
                : "bg-zinc-800 text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {d}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {visible.map((track) => (
          <TrackCard key={track.id} track={track} />
        ))}
      </div>
    </div>
  );
}
