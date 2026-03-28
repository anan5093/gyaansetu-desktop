export default function AboutSection() {
  return (
    <section
      id="about"
      className="px-6 md:px-16 py-20 flex flex-col md:flex-row items-center gap-12 animate-fadeInUp"
    >

      {/* LEFT → IMAGE */}
      <div className="flex justify-center">
        <img
          src="/Anand-2.jpeg"
          alt="Anand Raj - AI developer and creator of NCERT RAG AI Tutor"
          loading="lazy"
          className="w-52 h-52 md:w-64 md:h-64 object-cover rounded-full shadow-xl border-4 border-orange-500"
        />
      </div>

      {/* RIGHT → TEXT */}
      <div className="max-w-xl">

        <h2 className="text-3xl md:text-4xl font-bold text-gradient-animated">
          About the Developer
        </h2>

        {/* SEO Optimized Paragraph */}
        <p className="text-gray-600 mt-6 leading-relaxed">
          Hi, I'm <span className="font-semibold text-black">Anand Raj</span>, a B.Tech Computer Science student at Galgotias University (2022–2026).
          I specialize in building <strong>AI-powered education systems</strong> and intelligent applications using modern technologies.
          This project is an <strong>NCERT RAG-based AI tutor</strong> designed to deliver <strong>accurate, context-aware answers</strong> using
          <strong> retrieval-augmented generation (RAG)</strong> and vector search.
          My work focuses on combining <strong>machine learning, system design, and scalable web applications</strong>
          to improve <strong>digital education and personalized learning</strong> for students across India.
        </p>

        {/* TECH TAGS */}
        <div className="flex flex-wrap gap-3 mt-6">

          <span className="px-3 py-1 border border-white/20 rounded-full text-sm hover:scale-105 transition">
            Python
          </span>

          <span className="px-3 py-1 border border-white/20 rounded-full text-sm hover:scale-105 transition">
            FastAPI
          </span>

          <span className="px-3 py-1 border border-white/20 rounded-full text-sm hover:scale-105 transition">
            FAISS Vector Search
          </span>

          <span className="px-3 py-1 border border-white/20 rounded-full text-sm hover:scale-105 transition">
            RAG Architecture
          </span>

          <span className="px-3 py-1 border border-white/20 rounded-full text-sm hover:scale-105 transition">
            React + Vite
          </span>

        </div>

      </div>

    </section>
  );
}
