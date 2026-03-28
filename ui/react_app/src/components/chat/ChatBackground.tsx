export default function ChatBackground() {
  return (
    <div
      aria-hidden="true"
      className="absolute inset-0 -z-10 overflow-hidden"
    >

      {/* Base Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#0f172a] via-[#1e293b] to-[#7c2d12]" />

      {/* Orange Glow (Top Right) */}
      <div
        className="absolute top-0 right-0 w-[350px] h-[350px] 
                   bg-orange-500/15 blur-2xl rounded-full 
                   will-change-transform"
      />

      {/* Blue Glow (Bottom Left) */}
      <div
        className="absolute bottom-0 left-0 w-[350px] h-[350px] 
                   bg-blue-500/15 blur-2xl rounded-full 
                   will-change-transform"
      />

    </div>
  );
}
