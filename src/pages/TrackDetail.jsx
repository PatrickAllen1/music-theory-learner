import { useParams, Link } from "react-router-dom";
import { trackById } from "../content/tracks";

function StatBox({ label, value }) {
  return (
    <div>
      <span className="text-zinc-500 block text-xs font-mono mb-0.5">
        {label}
      </span>
      <span className="font-mono text-sm text-zinc-100">{value}</span>
    </div>
  );
}

function SectionTag({ label }) {
  return (
    <span className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-300">
      {label}
    </span>
  );
}

export default function TrackDetail() {
  const { id } = useParams();
  const track = trackById[id];

  if (!track)
    return (
      <div className="font-mono text-zinc-500">
        Track not found.{" "}
        <Link to="/library" className="underline hover:text-zinc-300">
          Back to library
        </Link>
      </div>
    );

  const chords = track.chord_progression?.chords;

  return (
    <div className="max-w-3xl">
      <Link
        to="/library"
        className="text-xs font-mono text-zinc-500 hover:text-zinc-300 mb-6 block"
      >
        ← Library
      </Link>

      {/* Header */}
      <div className="mb-1">
        <span className="text-sm font-mono text-zinc-400">{track.artist}</span>
      </div>
      <h1 className="text-3xl font-mono font-bold mb-6">{track.title}</h1>

      {/* Stats */}
      <div className="grid grid-cols-3 sm:grid-cols-6 gap-4 p-4 bg-zinc-900 rounded-lg mb-8">
        <StatBox label="BPM" value={track.bpm} />
        <StatBox label="KEY" value={track.key} />
        <StatBox
          label="SWING"
          value={track.swing === "none" ? "—" : track.swing}
        />
        <StatBox label="TIME" value={track.time_sig} />
        <StatBox label="BARS" value={track.total_bars} />
        <StatBox label="LEVEL" value={track.difficulty} />
      </div>

      {/* Structure */}
      <section className="mb-8">
        <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
          Structure
        </h2>
        <div className="space-y-2">
          {track.structure.map((s, i) => (
            <div
              key={i}
              className="flex gap-4 items-baseline p-3 bg-zinc-900 rounded"
            >
              <span className="font-mono text-xs text-zinc-500 w-24 shrink-0">
                {s.bars}
              </span>
              <span className="font-mono text-xs font-semibold text-zinc-300 w-32 shrink-0">
                {s.section}
              </span>
              <span className="text-xs text-zinc-400 leading-relaxed">
                {s.description}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Chord Progression */}
      {track.chord_progression ? (
        <section className="mb-8">
          <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
            Chord Progression
          </h2>
          <div className="p-4 bg-zinc-900 rounded-lg">
            <div className="flex gap-2 flex-wrap mb-3">
              {chords.map((c, i) => (
                <span
                  key={i}
                  className="px-3 py-2 bg-zinc-800 rounded font-mono text-zinc-100 text-sm"
                >
                  {c}
                </span>
              ))}
            </div>
            <p className="text-xs font-mono text-zinc-500 mb-3">
              {track.chord_progression.roman_numerals}
            </p>
            <p className="text-xs text-zinc-400 leading-relaxed">
              {track.chord_progression.theory_notes}
            </p>
          </div>
        </section>
      ) : (
        <section className="mb-8">
          <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
            Harmonic Approach
          </h2>
          <div className="p-4 bg-zinc-900 rounded-lg">
            <p className="text-xs font-mono text-zinc-500 mb-2">
              no chord progression
            </p>
            <p className="text-xs text-zinc-400 leading-relaxed">
              {track.theory_notes}
            </p>
          </div>
        </section>
      )}

      {/* Key Techniques */}
      <section className="mb-8">
        <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
          Key Techniques
        </h2>
        <ul className="space-y-2">
          {track.key_techniques.map((t, i) => (
            <li key={i} className="flex gap-3 text-sm">
              <span className="text-zinc-600 font-mono shrink-0">—</span>
              <span className="text-zinc-300">{t}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Theory Notes (only show if chord_progression exists, since we already showed it above otherwise) */}
      {track.chord_progression && (
        <section className="mb-8">
          <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
            Theory Notes
          </h2>
          <p className="text-zinc-300 text-sm leading-relaxed">
            {track.theory_notes}
          </p>
        </section>
      )}

      {/* Tracks */}
      <section className="mb-8">
        <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
          Tracks ({track.tracks.length})
        </h2>
        <div className="space-y-1">
          {track.tracks.map((t, i) => (
            <div
              key={i}
              className="flex gap-3 items-baseline py-1.5 border-b border-zinc-800/60"
            >
              <span
                className={`text-xs font-mono px-1.5 py-0.5 rounded shrink-0 ${
                  t.type === "MIDI"
                    ? "bg-blue-900/40 text-blue-400"
                    : "bg-purple-900/40 text-purple-400"
                }`}
              >
                {t.type}
              </span>
              <span className="font-mono text-xs text-zinc-300 w-32 shrink-0">
                {t.name}
              </span>
              <span className="text-xs text-zinc-500">{t.role}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Spinoff Potential */}
      {track.spinoff_potential && (
        <section className="mb-8">
          <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
            Spinoff Potential
          </h2>
          <div className="p-4 bg-zinc-900 rounded-lg">
            <div className="flex gap-4 mb-4 text-xs font-mono">
              <div>
                <span className="text-zinc-600 block mb-1">BPM range</span>
                <span className="text-zinc-300">
                  {track.spinoff_potential.bpm_range}
                </span>
              </div>
              <div>
                <span className="text-zinc-600 block mb-1">Try these keys</span>
                <span className="text-zinc-300">
                  {track.spinoff_potential.key_changes.join(", ")}
                </span>
              </div>
            </div>
            <ul className="space-y-1.5">
              {track.spinoff_potential.elements_to_transplant.map((el, i) => (
                <li key={i} className="flex gap-2 text-xs">
                  <span className="text-zinc-600 font-mono">→</span>
                  <span className="text-zinc-400">{el}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* Splice Searches */}
      <section className="mb-8">
        <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-wider mb-3">
          Splice Searches
        </h2>
        <div className="flex gap-2 flex-wrap">
          {track.splice_searches.map((s, i) => (
            <span
              key={i}
              className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-400"
            >
              "{s}"
            </span>
          ))}
        </div>
      </section>
    </div>
  );
}
