// src/components/landing/StorySection.tsx

export default function StorySection() {
  return (
    <section
      id="story"
      className="py-24 px-6 text-center max-w-4xl mx-auto animate-fadeInUp"
    >

      {/* Heading */}
      <h2 className="text-3xl md:text-4xl font-bold animate-fadeIn">
        From Freedom Fighters to Future Learners
      </h2>

      {/* SEO Optimized Paragraph */}
      <p
        className="mt-6 text-gray-400 animate-fadeInUp"
        style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}
      >
        The same spirit that once drove <strong>India’s freedom fighters</strong>
        now fuels a new revolution in <strong>education and learning</strong>.
        With the rise of <strong>AI-powered education platforms</strong> and
        <strong> NCERT-based learning systems</strong>, students can access
        high-quality knowledge anytime, anywhere. This shift represents the
        future of <strong>digital education in India</strong>, where intelligent
        tutoring systems empower learners to grow faster and smarter.
      </p>

    </section>
  );
}
