import { useNavigate } from "react-router-dom";
import ChatPreview from "./ChatPreview";

export default function HeroSection() {
  const navigate = useNavigate();

  return (
    <section id="hero" className="min-h-screen">
      <div className="flex flex-col md:flex-row items-center justify-between px-6 md:px-16 py-20 gap-12">

        {/* ================= LEFT ================= */}
        <div className="max-w-xl animate-slideLeft">

          {/* Badge */}
          <p className="bg-orange-100 text-orange-600 px-4 py-1 rounded-full inline-block mb-4 animate-fadeIn">
            ✨ AI-Powered Education Assistant
          </p>

          {/* Heading */}
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight animate-fadeInUp">
            NCERT Learning Companion
          </h1>

          {/* Description */}
          <p className="text-gray-600 mt-6 animate-fadeIn">
            Ask questions, get instant answers with context from NCERT books.
          </p>

          {/* Buttons */}
          <div className="flex gap-4 mt-8 animate-fadeInUp">

            <button
              onClick={() => navigate("/chat")}
              className="bg-orange-500 text-white px-6 py-3 rounded-full shadow-md 
                         transition-transform duration-300 hover:scale-105 active:scale-95"
            >
              Start Learning →
            </button>

            <button
              className="border border-orange-500 text-orange-500 px-6 py-3 rounded-full 
                         transition-transform duration-300 hover:scale-105 active:scale-95"
            >
              Learn More
            </button>

          </div>
        </div>

        {/* ================= RIGHT (CHAT PREVIEW) ================= */}
        <div className="hidden md:flex justify-center items-center animate-fadeIn">

          <div className="float">
            <ChatPreview />
          </div>

        </div>

      </div>
    </section>
  );
}
