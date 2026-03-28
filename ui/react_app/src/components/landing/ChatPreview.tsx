import { useEffect, useRef, useState } from "react";

type Message = {
  role: "user" | "ai";
  text: string;
};

const messages: Message[] = [
  { role: "user", text: "What is force?" },
  { role: "ai", text: "Force is a push or pull acting on an object." },
  { role: "user", text: "Give example" },
  { role: "ai", text: "Pushing a door or pulling a rope are examples of force." }
];

export default function ChatPreview() {
  const [visibleMessages, setVisibleMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    let i = 0;
    let timeout: ReturnType<typeof setTimeout>;

    const runChat = () => {
      if (i >= messages.length) {
        i = 0;
        setVisibleMessages([]);
      }

      const msg = messages[i];

      if (msg.role === "user") {
        setVisibleMessages((prev) => [...prev, msg]);
        i++;
        timeout = setTimeout(runChat, 1000);
      } else {
        setIsTyping(true);

        timeout = setTimeout(() => {
          setIsTyping(false);
          setVisibleMessages((prev) => [...prev, msg]);
          i++;
          timeout = setTimeout(runChat, 1200);
        }, 700);
      }
    };

    runChat();
    return () => clearTimeout(timeout);
  }, []);

  // ✅ Scroll inside chat box
  useEffect(() => {
    containerRef.current?.scrollTo({
      top: containerRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [visibleMessages, isTyping]);

  return (
    <div
      ref={containerRef}
      aria-label="AI chat preview demonstrating NCERT learning assistant"
      className="w-80 h-96 bg-white rounded-xl shadow-xl p-4 flex flex-col gap-3 overflow-y-auto"
    >
      {visibleMessages.map((msg, index) => (
        <div
          key={index}
          className={`max-w-[80%] px-3 py-2 rounded-lg text-sm animate-fadeInUp ${
            msg.role === "user"
              ? "bg-orange-500 text-white self-end"
              : "bg-gray-100 text-gray-800 self-start"
          }`}
          style={{
            animationDelay: `${index * 0.05}s`,
            animationFillMode: "forwards",
          }}
        >
          {msg.text}
        </div>
      ))}

      {/* 🤖 Typing indicator */}
      {isTyping && (
        <div className="text-xs text-gray-400 animate-fadeIn">
          AI tutor is generating an answer...
        </div>
      )}
    </div>
  );
}
