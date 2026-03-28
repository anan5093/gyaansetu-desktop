export default function Footer() {
  return (
    <footer
      aria-label="Website footer"
      className="fixed bottom-0 left-0 w-full z-50
                 bg-black/30 backdrop-blur-xl
                 border-t border-white/10"
    >
      <div
        className="flex flex-col md:flex-row items-center justify-between
                   gap-2 md:gap-0
                   px-6 md:px-10 py-3
                   text-sm text-gray-400"
      >

        {/* Left */}
        <p className="opacity-80 hover:opacity-100 transition">
          © 2026 NCERT Companion — AI-powered learning platform
        </p>

        {/* Center (SEO optimized) */}
        <p className="text-center">
          Built with ❤️ using <strong>AI-powered education</strong> by{" "}
          <span className="text-white font-medium hover:text-orange-400 transition">
            Anand Raj
          </span>
        </p>

        {/* Right (Social Links) */}
        <div className="flex items-center gap-4">

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
              className="w-7 h-7 md:w-8 md:h-8
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
              className="w-7 h-7 md:w-8 md:h-8
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
