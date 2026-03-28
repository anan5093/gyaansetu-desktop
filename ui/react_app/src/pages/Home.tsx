import { lazy, Suspense } from "react";
import Navbar from "../components/landing/Navbar";
import Footer from "../components/landing/FooterSection";

// 🔥 Lazy load all heavy sections
const HeroSection = lazy(() => import("../components/landing/HeroSection"));
const StorySection = lazy(() => import("../components/landing/StorySection"));
const FreedomBackground = lazy(() => import("../components/landing/FreedomBackground"));
const FeaturesSection = lazy(() => import("../components/landing/FeaturesSection"));
const AIGoodSection = lazy(() => import("../components/landing/AIGoodSection"));
const VisionSection = lazy(() => import("../components/landing/VisionSection"));
const AboutSection = lazy(() => import("../components/landing/AboutSection"));

export default function Home() {
  return (
    <main
      aria-label="AI-powered NCERT learning platform homepage"
      className="relative min-h-screen overflow-hidden"
    >

      {/* 🌐 Navbar */}
      <Navbar />

      {/* 🔥 Hero (load first for LCP) */}
      <Suspense fallback={<div className="h-screen flex items-center justify-center text-white">Loading...</div>}>
        <HeroSection />
      </Suspense>

      {/* Below-the-fold sections (lazy) */}
      <Suspense fallback={<div className="text-center text-gray-400 py-10">Loading sections...</div>}>

        {/* 📖 Story */}
        <StorySection />

        {/* 🇮🇳 Freedom */}
        <FreedomBackground />

        {/* ⚡ Features */}
        <FeaturesSection />

        {/* 🤖 AI for Good */}
        <AIGoodSection />

        {/* 🎯 Vision */}
        <VisionSection />

        {/* 📘 About */}
        <AboutSection />

      </Suspense>

      {/* 🔻 Footer */}
      <Footer />

    </main>
  );
}
