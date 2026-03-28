import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { lazy, Suspense } from "react";

// 🔥 Lazy load pages (code splitting)
const Home = lazy(() => import("./pages/Home"));
const Chat = lazy(() => import("./pages/Chat"));
const Evaluation = lazy(() => import("./pages/Evaluation"));

export default function App() {
  return (
    <Router>
      <Suspense
        fallback={
          <div className="h-screen flex items-center justify-center text-white">
            Loading AI Tutor...
          </div>
        }
      >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/evaluation" element={<Evaluation />} />
        </Routes>
      </Suspense>
    </Router>
  );
}
