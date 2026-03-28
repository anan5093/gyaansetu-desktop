type Props = {
  onSelect: (cls: number) => void;
};

export default function ClassSelector({ onSelect }: Props) {
  return (
    <section
      aria-label="Select your class for NCERT AI learning"
      className="animate-fadeInUp bg-white/10 backdrop-blur-md p-6 rounded-2xl text-center max-w-md"
    >

      {/* AI Message */}
      <p className="bg-gray-800 px-4 py-2 rounded-xl mb-4 inline-block">
        🤖 Hello! Which class are you studying in?
      </p>

      {/* Buttons */}
      <div className="flex gap-3 justify-center flex-wrap">

        {[9, 10, 11, 12].map((cls) => (
          <button
            key={cls}
            onClick={() => onSelect(cls)}
            aria-label={`Select Class ${cls}`}
            className="px-4 py-2 bg-orange-500 rounded-full 
                       transition-transform duration-300 
                       hover:bg-orange-600 hover:scale-105 active:scale-95"
          >
            Class {cls}
          </button>
        ))}

      </div>
    </section>
  );
}
