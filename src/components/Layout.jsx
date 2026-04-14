import Nav from "./Nav";

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <Nav />
      <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
    </div>
  );
}
