import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [active, setActive] = useState("hero");

  // Apple navbar states
  const [showNav, setShowNav] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const [scrolled, setScrolled] = useState(false);

  // Mobile menu
  const [menuOpen, setMenuOpen] = useState(false);

  const sections = ["hero", "features", "about", "vision"];

  // Active section tracking
  useEffect(() => {
    if (location.pathname !== "/") return;

    const observers: IntersectionObserver[] = [];

    sections.forEach((id) => {
      const el = document.getElementById(id);
      if (!el) return;

      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) setActive(id);
        },
        { threshold: 0.6 }
      );

      observer.observe(el);
      observers.push(observer);
    });

    return () => observers.forEach((obs) => obs.disconnect());
  }, [location.pathname]);

  // Scroll behavior
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

  // Navigation
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
      className={`fixed top-0 w-full z-50 transition-all duration-500
      ${showNav ? "translate-y-0" : "-translate-y-full"}
      backdrop-blur-2xl bg-black/30 border-b border-white/10
      ${scrolled ? "shadow-lg shadow-black/30" : ""}`}
    >
      <div className="flex justify-between items-center px-4 md:px-10 py-3 text-white">

        {/* Logo */}
        <button
          onClick={() => navigate("/")}
          className="font-semibold text-lg"
        >
          ✨ <span className="text-orange-500">NCERT</span> Companion
        </button>

        {/* Desktop Nav */}
        <div className="hidden md:flex gap-6 items-center">
          {sections.map((sec) => (
            <button
              key={sec}
              onClick={() => goToSection(sec)}
              className={active === sec ? "text-orange-400" : ""}
            >
              {sec}
            </button>
          ))}

          <button onClick={() => navigate("/evaluation")}>
            Evaluation
          </button>

          <button
            onClick={() => navigate("/chat")}
            className="bg-orange-500 px-4 py-2 rounded-full"
          >
            Start Chat
          </button>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden text-2xl"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden flex flex-col items-center gap-5 py-6 bg-black/95 text-white">
          {sections.map((sec) => (
            <button
              key={sec}
              onClick={() => {
                goToSection(sec);
                setMenuOpen(false);
              }}
            >
              {sec}
            </button>
          ))}

          <button onClick={() => navigate("/evaluation")}>
            Evaluation
          </button>

          <button
            onClick={() => navigate("/chat")}
            className="bg-orange-500 px-6 py-2 rounded-full"
          >
            Start Chat
          </button>
        </div>
      )}
    </nav>
  );
}
