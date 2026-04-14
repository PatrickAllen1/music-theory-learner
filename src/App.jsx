import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import Builder from "./pages/Builder";
import Library from "./pages/Library";
import Theory from "./pages/Theory";
import Ableton from "./pages/Ableton";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/builder" replace />} />
          <Route path="/builder" element={<Builder />} />
          <Route path="/library" element={<Library />} />
          <Route path="/theory" element={<Theory />} />
          <Route path="/ableton" element={<Ableton />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
