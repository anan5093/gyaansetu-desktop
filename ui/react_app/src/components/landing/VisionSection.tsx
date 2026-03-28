export default function VisionSection() {
  return (
    <section
      id="vision"
      className="min-h-screen px-6 md:px-16 py-20 animate-fadeInUp"
    >
      <div className="bg-gray-900 text-white p-8 md:p-12 rounded-xl">

        {/* Heading */}
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gradient-animated animate-fadeIn">
          AI Education Vision & Research Inspiration
        </h2>

        {/* Content */}
        <div
          className="mt-8 max-w-4xl mx-auto text-gray-300 space-y-6 text-center leading-relaxed animate-fadeInUp"
          style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}
        >

          <p>
            This project is inspired by real-world research in
            <strong> AI-powered tutoring systems</strong> and
            <strong> retrieval-augmented generation (RAG)</strong>,
            which are transforming modern <strong>digital education</strong>.
          </p>

          <p>
            Studies such as the <strong>NeuroBot Teaching Assistant</strong>
            show that students trust <strong>AI tutors</strong> more when
            responses are grounded in <strong>verified academic content</strong>,
            leading to more reliable and <strong>personalized learning experiences</strong>.
          </p>

          <p>
            Research also highlights that students primarily use
            <strong> AI learning platforms</strong> for
            <strong> exam preparation</strong> and
            <strong> concept clarification</strong>, making them powerful tools
            for <strong>just-in-time learning</strong>.
          </p>

          <p>
            Building on these insights, this project applies
            <strong> RAG-based AI techniques</strong> to the
            <strong> NCERT curriculum</strong>, delivering
            <strong> accurate, context-aware answers</strong> while maintaining
            alignment with official textbooks and educational standards.
          </p>

        </div>

      </div>
    </section>
  );
}
