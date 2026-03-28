type MessageBubbleProps = {
  sender: "user" | "ai";
  text: string;
};

export default function MessageBubble({ sender, text }: MessageBubbleProps) {
  const isUser = sender === "user";

  return (
    <div
      role="status"
      aria-label={isUser ? "User message" : "AI response"}
      className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm 
                  animate-fadeInUp will-change-transform ${
        isUser
          ? "bg-orange-500 text-white ml-auto"
          : "bg-white/10 text-white border border-white/10"
      }`}
    >
      {text}
    </div>
  );
}
