export default function FreedomBackground() {
  const images = [
    { src: "/bhagat.jpg", alt: "Bhagat Singh portrait" },
    { src: "/revolution.jpg", alt: "Indian freedom revolution scene" },
    { src: "/savarkar.jpg", alt: "Vinayak Savarkar portrait" },
    { src: "/bharatmata.jpg", alt: "Bharat Mata illustration" },
    { src: "/quote.jpg", alt: "Inspirational freedom fighter quote" },
  ];

  return (
    <div className="relative w-full flex flex-col items-center mt-16">

      {/* 🖼 Horizontal Image Row */}
      <div className="flex gap-6 justify-center items-center flex-wrap mt-10">

        {images.map((img, i) => (
          <img
            key={i}
            src={img.src}
            alt={img.alt}
            loading="lazy"
            className="w-40 h-52 object-cover rounded-xl shadow-lg opacity-0 animate-fadeInUp"
            style={{
              animationDelay: `${i * 0.3}s`,
              animationFillMode: "forwards",
            }}
          />
        ))}

      </div>
    </div>
  );
}
