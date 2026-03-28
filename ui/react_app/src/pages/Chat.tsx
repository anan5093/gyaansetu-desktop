import { useState, useEffect } from "react";
import ChatBackground from "../components/chat/ChatBackground";
import ClassSelector from "../components/chat/ClassSelector";
import ChatWindow from "../components/chat/ChatWindow";
import Navbar from "../components/landing/Navbar";

export default function Chat() {
  const [selectedClass, setSelectedClass] = useState<number | null>(null);
  const [showSelector, setShowSelector] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSelector(true);
    }, 400);

    return () => clearTimeout(timer);
  }, []);

  return (
    <main
      aria-label="AI chat interface for NCERT learning"
      className="relative min-h-screen text-white overflow-hidden flex flex-col"
    >

      {/* Background */}
      <ChatBackground />

      {/* Navbar */}
      <div className="relative z-20">
        <Navbar />
      </div>

      {/* Content */}
      <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-4 py-6">

        {/* Class Selector */}
        {!selectedClass && showSelector && (
          <div className="animate-fadeInUp">
            <ClassSelector onSelect={setSelectedClass} />
          </div>
        )}

        {/* Chat Window */}
        {selectedClass && (
          <div className="w-full max-w-5xl h-full flex flex-col animate-fadeIn">
            <ChatWindow selectedClass={selectedClass} />
          </div>
        )}

      </div>
    </main>
  );
}
