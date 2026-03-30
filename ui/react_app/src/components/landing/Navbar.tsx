import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [active, setActive] = useState("hero");

  // 🔥 Apple Navbar States
  const [showNav, setShowNav] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const [scrolled, setScrolled] = useState(false);

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

  // 🔥 Apple Scroll Behavior (Hide/Show Navbar)
  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;

      setScrolled(currentScrollY > 10);

      if (currentScrollY > lastScrollY && currentScrollY > 80) {
        setShowNav(false);
      } else {
        setShowNav(true);
      }

      setLastScrollY(currentScrollY);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [lastScrollY]);

  // 🔁 Navigation + Scroll
  const goToSection = useCallback(
    (id: string) => {
      if (location.pathname === "/") {
        document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
      } else {
        navigate("/");
        setTimeout(() => {
          document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
        }, 300);
      }
    },
    [location.pathname, navigate]
  );

  return (
    <nav
      aria-label="Main Navigation"
      className={`fixed top-0 w-full z-50 transition-all duration-500 ease-in-out
      ${showNav ? "translate-y-0 opacity-100" : "-translate-y-full opacity-0"}
      backdrop-blur-2xl bg-gradient-to-r from-black/40 via-black/20 to-black/40
      border-b border-white/10 ${scrolled ? "shadow-lg shadow-black/30" : ""}`}
    >
      <div className="flex justify-between items-center px-4 md:px-10 py-3 md:py-4 text-white">

        {/* Logo */}
        <button
          onClick={() => navigate("/")}
          className="font-semibold text-base md:text-lg whitespace-nowrap hover:scale-105 transition-transform"
        >
          ✨ <span className="text-orange-500">NCERT</span> Companion
        </button>

        {/* Nav */}
        <div className="flex gap-4 md:gap-8 items-center relative overflow-x-auto md:overflow-visible">

          {/* Landing Sections */}
          {sections.map((sec) => (
            <button
              key={sec}
              onClick={() => goToSection(sec)}
              className={`relative pb-1 capitalize transition-colors duration-300 whitespace-nowrap ${
                active === sec && location.pathname === "/"
                  ? "text-orange-400"
                  : "hover:text-orange-300"
              }`}
            >
              {sec}

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
            className={`relative pb-1 transition-colors duration-300 whitespace-nowrap ${
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
            className={`ml-2 md:ml-4 px-3 md:px-5 py-2 rounded-full shadow-lg 
            transition-all duration-300 hover:scale-105 active:scale-95 whitespace-nowrap ${
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
