export default function Footer() {
  return (
    <footer
      aria-label="Website footer"
      className="fixed bottom-0 left-0 w-full z-50
                 backdrop-blur-2xl
                 bg-gradient-to-r from-black/40 via-black/20 to-black/40
                 border-t border-white/10"
    >
      <div
        className="flex flex-col md:flex-row items-center justify-between
                   gap-3 md:gap-0
                   px-4 md:px-10 py-3
                   text-xs sm:text-sm text-gray-400
                   text-center md:text-left"
      >

        {/* Left */}
        <p className="opacity-80 hover:opacity-100 transition leading-relaxed max-w-full">
          © 2026 NCERT Companion — AI-powered learning platform
        </p>

        {/* Center */}
        <p className="leading-relaxed px-2 md:px-4">
          Built with ❤️ using <strong>AI-powered education</strong> by{" "}
          <span className="text-white font-medium hover:text-orange-400 transition">
            Anand Raj
          </span>
        </p>

        {/* Right */}
        <div className="flex items-center gap-3 md:gap-4">

          {/* GitHub */}
          <a
            href="https://github.com/anan5093"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Visit Anand Raj GitHub profile"
            className="group"
          >
            <img
              src="/github_3291695.png"
              alt="GitHub profile link"
              loading="lazy"
              className="w-6 h-6 md:w-8 md:h-8
                         transition-transform duration-300
                         group-hover:scale-110 group-hover:rotate-6
                         opacity-80 group-hover:opacity-100"
            />
          </a>

          {/* LinkedIn */}
          <a
            href="https://www.linkedin.com/in/anand-raj-006a41217/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Visit Anand Raj LinkedIn profile"
            className="group"
          >
            <img
              src="/linkedin_3670129.png"
              alt="LinkedIn profile link"
              loading="lazy"
              className="w-6 h-6 md:w-8 md:h-8
                         transition-transform duration-300
                         group-hover:scale-110 group-hover:-rotate-6
                         opacity-80 group-hover:opacity-100"
            />
          </a>

        </div>

      </div>
    </footer>
  );
}
