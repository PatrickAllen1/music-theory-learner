import { NavLink } from "react-router-dom";

const links = [
  { to: "/builder", label: "Builder" },
  { to: "/library", label: "Library" },
  { to: "/theory", label: "Theory" },
  { to: "/ableton", label: "Ableton" },
];

export default function Nav() {
  return (
    <nav className="flex gap-6 px-6 py-4 bg-zinc-900 border-b border-zinc-700">
      <span className="text-zinc-100 font-mono font-bold mr-auto">
        music-theory-learner
      </span>
      {links.map(({ to, label }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) =>
            `text-sm font-mono ${isActive ? "text-white" : "text-zinc-400 hover:text-zinc-200"}`
          }
        >
          {label}
        </NavLink>
      ))}
    </nav>
  );
}
