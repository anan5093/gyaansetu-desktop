import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [active, setActive] = useState("hero");

  const sections = ["hero", "features", "about", "vision"];

  // 🔥 Scroll detection (ACTIVE NAV)
  useEffect(() => {
    if (location.pathname !== "/") return;

    const observers: IntersectionObserver[] = [];

    sections.forEach((id) => {
      const el = document.getElementById(id);
      if (!el) return;

      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setActive(id);
          }
        },
        { threshold: 0.6 }
      );

      observer.observe(el);
      observers.push(observer);
    });

    return () => observers.forEach((obs) => obs.disconnect());
  }, [location.pathname]);

  // 🔁 Navigation + Scroll (optimized)
  const goToSection = useCallback((id: string) => {
    if (location.pathname === "/") {
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
    } else {
      navigate("/");
      setTimeout(() => {
        document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
      }, 300);
    }
  }, [location.pathname, navigate]);

  return (
    <nav
      aria-label="Main Navigation"
      className="fixed top-0 w-full z-50 backdrop-blur-xl bg-black/30 border-b border-white/10"
    >
      <div className="flex justify-between items-center px-6 md:px-10 py-4 text-white">

        {/* Logo */}
        <button
          onClick={() => navigate("/")}
          className="font-semibold text-lg cursor-pointer hover:scale-105 transition-transform"
          aria-label="Go to homepage"
        >
          ✨ <span className="text-orange-500">NCERT</span> Companion
        </button>

        {/* Nav */}
        <div className="flex gap-6 md:gap-8 items-center relative">

          {/* Landing Sections */}
          {sections.map((sec) => (
            <button
              key={sec}
              onClick={() => goToSection(sec)}
              aria-label={`Go to ${sec} section`}
              className={`relative pb-1 capitalize transition-colors duration-300 ${
                active === sec && location.pathname === "/"
                  ? "text-orange-400"
                  : "hover:text-orange-300"
              }`}
            >
              {sec}

              {/* underline */}
              <span
                className={`absolute left-0 bottom-0 h-[2px] bg-orange-400 transition-all duration-300 ${
                  active === sec && location.pathname === "/"
                    ? "w-full"
                    : "w-0"
                }`}
              />
            </button>
          ))}

          {/* Evaluation Page */}
          <button
            onClick={() => navigate("/evaluation")}
            aria-label="Go to evaluation page"
            className={`relative pb-1 transition-colors duration-300 ${
              location.pathname === "/evaluation"
                ? "text-orange-400"
                : "hover:text-orange-300"
            }`}
          >
            Evaluation

            <span
              className={`absolute left-0 bottom-0 h-[2px] bg-orange-400 transition-all duration-300 ${
                location.pathname === "/evaluation" ? "w-full" : "w-0"
              }`}
            />
          </button>

          {/* Chat CTA */}
          <button
            onClick={() => navigate("/chat")}
            aria-label="Start chat"
            className={`ml-2 md:ml-4 px-4 md:px-5 py-2 rounded-full shadow-lg 
              transition-all duration-300 hover:scale-105 active:scale-95 ${
              location.pathname === "/chat"
                ? "bg-orange-600"
                : "bg-orange-500 hover:bg-orange-600"
            }`}
          >
            Start Chat
          </button>

        </div>
      </div>
    </nav>
  );
}
