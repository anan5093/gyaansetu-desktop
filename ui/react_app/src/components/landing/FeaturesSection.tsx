const features = [
  {
    title: "NCERT Curriculum Content",
    desc: "Learn directly from NCERT-based structured content designed for school students and exam preparation.",
  },
  {
    title: "FAISS Vector Database",
    desc: "Fast semantic search using FAISS vector store enables accurate retrieval of relevant NCERT concepts.",
  },
  {
    title: "OpenRouter LLM Integration",
    desc: "Advanced AI models power intelligent explanations and contextual answers for student queries.",
  },
  {
    title: "Smart Chunking System",
    desc: "Content is intelligently chunked for efficient retrieval and precise AI-generated responses.",
  },
  {
    title: "Real-time AI Retrieval",
    desc: "Get instant answers using retrieval-augmented generation (RAG) for accurate and contextual learning.",
  },
  {
    title: "Class-wise Learning Support",
    desc: "Ask questions based on your class and subject for personalized NCERT learning experience.",
  },
];

export default function FeaturesSection() {
  return (
    <section
      id="features"
      className="min-h-screen px-6 md:px-16 py-20"
    >
      {/* Heading */}
      <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-gradient-animated animate-fadeIn">
        AI-Powered NCERT Learning Features
      </h2>

      {/* SEO Paragraph */}
      <p className="text-gray-400 text-center max-w-3xl mx-auto mb-12 animate-fadeInUp">
        GyaanSetu combines <strong>AI-powered learning</strong>, 
        <strong> retrieval-augmented generation (RAG)</strong>, and 
        <strong> NCERT-based content</strong> to deliver accurate, fast, 
        and personalized answers for students. This intelligent system 
        ensures better understanding, improved exam preparation, and 
        efficient concept mastery.
      </p>

      {/* Feature Grid */}
      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">

        {features.map((feature, i) => (
          <div
            key={i}
            className="p-6 rounded-xl bg-white shadow-md 
                       animate-fadeInUp transition-transform duration-300 
                       hover:scale-105"
            style={{
              animationDelay: `${i * 0.15}s`,
              animationFillMode: "forwards",
            }}
          >
            {/* Icon */}
            <div className="text-orange-500 text-3xl mb-4">📘</div>

            {/* Title */}
            <h3 className="text-xl font-semibold text-gray-900">
              {feature.title}
            </h3>

            {/* Description (SEO optimized) */}
            <p className="text-gray-600 mt-2 text-sm">
              {feature.desc}
            </p>
          </div>
        ))}

      </div>
    </section>
  );
}
