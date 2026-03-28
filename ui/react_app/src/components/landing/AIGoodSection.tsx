// src/components/landing/AIGoodSection.tsx

export default function AIGoodSection() {
  return (
    <section
      id="ai-good"
      className="py-24 px-6 text-center animate-fadeInUp"
    >
      {/* Heading */}
      <h2 className="text-3xl md:text-4xl font-semibold">
        🌍 AI for Good — Education for All
      </h2>

      {/* Description (SEO Optimized) */}
      <p className="text-gray-400 mt-4 max-w-2xl mx-auto">
        GyaanSetu is an <strong>AI-powered education platform</strong> designed to
        transform <strong>NCERT learning</strong> for students across India.
        With <strong>personalized learning</strong>, <strong>instant doubt solving</strong>,
        and curriculum-based answers, students can master concepts faster and
        more effectively. This <strong>AI tutor for NCERT</strong> ensures that
        education is accessible anytime, anywhere — empowering every learner
        with high-quality knowledge.
      </p>

      {/* 🔥 Feature Grid */}
      <div className="mt-12 grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">

        {/* Feature 1 */}
        <div className="bg-white/5 p-6 rounded-xl backdrop-blur-md border border-white/10 
                        animate-fadeInUp transition-transform duration-300 hover:scale-105">
          <h3 className="text-lg font-semibold mb-2">
            📚 Curriculum Aligned Learning
          </h3>
          <p className="text-gray-400 text-sm">
            Our AI tutor provides answers strictly based on the <strong>NCERT curriculum</strong>,
            ensuring accurate, reliable, and exam-focused learning for students.
          </p>
        </div>

        {/* Feature 2 */}
        <div className="bg-white/5 p-6 rounded-xl backdrop-blur-md border border-white/10 
                        animate-fadeInUp transition-transform duration-300 hover:scale-105"
             style={{ animationDelay: "0.2s" }}>
          <h3 className="text-lg font-semibold mb-2">
            ⚡ Instant Doubt Solving with AI
          </h3>
          <p className="text-gray-400 text-sm">
            Get <strong>instant answers</strong> and detailed explanations using
            advanced <strong>AI-powered retrieval and reasoning</strong> tailored
            for school students.
          </p>
        </div>

        {/* Feature 3 */}
        <div className="bg-white/5 p-6 rounded-xl backdrop-blur-md border border-white/10 
                        animate-fadeInUp transition-transform duration-300 hover:scale-105"
             style={{ animationDelay: "0.4s" }}>
          <h3 className="text-lg font-semibold mb-2">
            🌐 Learn Anytime, Anywhere
          </h3>
          <p className="text-gray-400 text-sm">
            Access your <strong>AI learning assistant</strong> anytime without
            dependency on tutors, making <strong>digital education</strong>
            flexible, scalable, and accessible to all.
          </p>
        </div>

      </div>
    </section>
  );
}
