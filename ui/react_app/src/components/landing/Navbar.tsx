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

      {/* Desktop Nav */}
      <div className="hidden md:flex gap-6 lg:gap-8 items-center">

        {sections.map((sec) => (
          <button
            key={sec}
            onClick={() => goToSection(sec)}
            className={`relative pb-1 capitalize ${
              active === sec && location.pathname === "/"
                ? "text-orange-400"
                : "hover:text-orange-300"
            }`}
          >
            {sec}
            <span
              className={`absolute left-0 bottom-0 h-[2px] bg-orange-400 transition-all ${
                active === sec && location.pathname === "/"
                  ? "w-full"
                  : "w-0"
              }`}
            />
          </button>
        ))}

        <button
          onClick={() => navigate("/evaluation")}
          className={`relative pb-1 ${
            location.pathname === "/evaluation"
              ? "text-orange-400"
              : "hover:text-orange-300"
          }`}
        >
          Evaluation
        </button>

        <button
          onClick={() => navigate("/chat")}
          className="ml-2 px-4 py-2 rounded-full bg-orange-500 hover:bg-orange-600"
        >
          Start Chat
        </button>
      </div>

      {/* Mobile Hamburger */}
      <button
        className="md:hidden text-2xl"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        ☰
      </button>
    </div>

    {/* Mobile Menu */}
    {menuOpen && (
      <div className="md:hidden bg-black/95 backdrop-blur-xl flex flex-col items-center gap-6 py-6 text-white">

        {sections.map((sec) => (
          <button
            key={sec}
            onClick={() => {
              goToSection(sec);
              setMenuOpen(false);
            }}
            className={`capitalize text-lg ${
              active === sec ? "text-orange-400" : ""
            }`}
          >
            {sec}
          </button>
        ))}

        <button
          onClick={() => {
            navigate("/evaluation");
            setMenuOpen(false);
          }}
        >
          Evaluation
        </button>

        <button
          onClick={() => {
            navigate("/chat");
            setMenuOpen(false);
          }}
          className="bg-orange-500 px-6 py-2 rounded-full"
        >
          Start Chat
        </button>
      </div>
    )}
  </nav>
);
