import { Link } from "react-router-dom";

const difficultyStyles = {
  beginner: "bg-green-900/40 text-green-400",
  intermediate: "bg-yellow-900/40 text-yellow-400",
  advanced: "bg-red-900/40 text-red-400",
};

export default function TrackCard({ track }) {
  const chords = track.chord_progression?.chords;

  return (
    <Link
      to={`/library/${track.id}`}
      className="block p-4 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-600 transition-colors"
    >
      <div className="flex justify-between items-start mb-2">
        <span className="text-xs font-mono text-zinc-500">{track.artist}</span>
        <span
          className={`text-xs font-mono px-1.5 py-0.5 rounded ${difficultyStyles[track.difficulty] ?? "bg-zinc-800 text-zinc-400"}`}
        >
          {track.difficulty}
        </span>
      </div>

      <h3 className="font-mono font-semibold text-zinc-100 mb-3">
        {track.title}
      </h3>

      <div className="flex gap-3 text-xs font-mono text-zinc-400 mb-3">
        <span>{track.bpm} BPM</span>
        <span>{track.key}</span>
        {track.swing && track.swing !== "none" && (
          <span className="text-zinc-600">{track.swing}</span>
        )}
      </div>

      {chords ? (
        <div className="text-xs font-mono text-zinc-500">
          {chords.slice(0, 3).join(" → ")}
          {chords.length > 3 && " …"}
        </div>
      ) : (
        <div className="text-xs font-mono text-zinc-700">no chord loop</div>
      )}
    </Link>
  );
}
