import { useState, useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

type ChatWindowProps = {
  selectedClass: number;
};

type Message = {
  sender: "user" | "ai";
  text: string;
};

export default function ChatWindow({ selectedClass }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "ai",
      text: `👋 Great! You selected Class ${selectedClass}. Ask me anything.`,
    },
  ]);

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isThinking, setIsThinking] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // 🔥 Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping, isThinking]);

  // ✅ Optimized typing effect (less re-renders)
  const typeEffect = async (fullText: string) => {
    setIsTyping(true);

    let index = 0;

    return new Promise<void>((resolve) => {
      const interval = setInterval(() => {
        index++;

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            sender: "ai",
            text: fullText.slice(0, index),
          };
          return updated;
        });

        if (index >= fullText.length) {
          clearInterval(interval);
          setIsTyping(false);
          resolve();
        }
      }, 16); // smoother + less CPU
    });
  };

  const sendMessage = async () => {
    if (!input.trim() || isTyping) return;

    const userMsg: Message = { sender: "user", text: input };

    setMessages((prev) => [
      ...prev,
      userMsg,
      { sender: "ai", text: "" },
    ]);

    const userQuestion = input;
    setInput("");
    setIsThinking(true);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: userQuestion,
            class_id: selectedClass,
            subject: "science",
          }),
        }
      );

      if (!res.ok) throw new Error("API failed");

      const data = await res.json();
      setIsThinking(false);

      await typeEffect(data.answer);

    } catch (err) {
      console.error(err);
      setIsThinking(false);

      await typeEffect("⚠️ Something went wrong. Please try again.");
    }
  };

  return (
    <div
      aria-label="AI chat window for NCERT learning assistant"
      className="w-full h-full flex flex-col justify-between px-4 md:px-20"
    >

      {/* CHAT */}
      <div className="flex-1 overflow-y-auto pt-6 space-y-4">

        {messages.map((msg, i) => (
          <div
            key={i}
            className="animate-fadeInUp"
          >
            <MessageBubble {...msg} />
          </div>
        ))}

        {/* Thinking indicator */}
        {isThinking && (
          <div className="bg-white/10 px-4 py-2 rounded-xl w-fit">
            <span className="flex gap-1">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </span>
          </div>
        )}

        {/* Typing cursor */}
        {isTyping && (
          <div className="text-white text-sm opacity-70 px-2">
            <span className="animate-pulse">▍</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* INPUT */}
      <div className="pb-6">
        <div className="flex items-center gap-3
                        bg-white/10 backdrop-blur-xl
                        rounded-full px-5 py-3
                        border border-white/10">

          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask NCERT questions with AI tutor..."
            aria-label="Type your question"
            className="flex-1 bg-transparent outline-none text-white placeholder-gray-400"
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />

          <button
            onClick={sendMessage}
            disabled={isTyping}
            aria-label="Send message"
            className={`px-5 py-2 rounded-full transition-transform duration-300
              ${isTyping
                ? "bg-gray-500 cursor-not-allowed"
                : "bg-orange-500 hover:bg-orange-600 hover:scale-105"}
            `}
          >
            Send
          </button>

        </div>
      </div>
    </div>
  );
}
