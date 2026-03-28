import { useEffect, useState, lazy, Suspense } from "react";
import Navbar from "../components/landing/Navbar";
import FooterSection from "../components/landing/FooterSection";

// 🔥 Lazy load chart (huge performance win)
const ScatterChartComp = lazy(() =>
  import("recharts").then((mod) => ({
    default: () => {
      const { ScatterChart, Scatter, XAxis, YAxis, Tooltip } = mod;
      return (props: any) => (
        <ScatterChart width={500} height={300}>
          <XAxis dataKey="x" />
          <YAxis dataKey="y" />
          <Tooltip cursor={{ strokeDasharray: "3 3" }} />
          <Scatter data={props.data} />
        </ScatterChart>
      );
    },
  }))
);

type EvaluationData = {
  retrieval: { accuracy: number };
  generation: { avg_similarity: number };
  latency: { avg_latency: number };
  embedding: { x: number; y: number }[];
};

export default function Evaluation() {
  const [data, setData] = useState<EvaluationData | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchEvaluation = async () => {
    setLoading(true);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/evaluation`
      );

      if (!res.ok) throw new Error("API failed");

      const json = await res.json();
      setData(json.evaluation);
    } catch (err) {
      console.error("Error fetching evaluation:", err);
    }

    setLoading(false);
  };

  useEffect(() => {
    fetchEvaluation();
  }, []);

  return (
    <main
      aria-label="AI model evaluation dashboard for NCERT RAG system"
      className="min-h-screen text-white"
    >

      {/* Navbar */}
      <Navbar />

      <div className="pt-24 px-6 md:px-10">

        {/* Heading (SEO optimized) */}
        <h1 className="text-3xl font-bold mb-6 animate-fadeIn">
          📊 AI Evaluation Dashboard
        </h1>

        {loading && (
          <p className="text-gray-400 animate-pulse">
            Running AI evaluation...
          </p>
        )}

        {!data && !loading && (
          <p className="text-gray-400">
            No evaluation data available from backend
          </p>
        )}

        {data && (
          <div className="space-y-10 animate-fadeInUp">

            {/* Retrieval */}
            <div className="bg-white/5 p-6 rounded-xl">
              <h2 className="text-xl mb-2">
                🔍 Retrieval Accuracy (RAG System)
              </h2>
              <p>{data.retrieval.accuracy}</p>
            </div>

            {/* Generation */}
            <div className="bg-white/5 p-6 rounded-xl">
              <h2 className="text-xl mb-2">
                🤖 AI Answer Quality
              </h2>
              <p>{data.generation.avg_similarity}</p>
            </div>

            {/* Latency */}
            <div className="bg-white/5 p-6 rounded-xl">
              <h2 className="text-xl mb-2">
                ⏱ AI Response Latency
              </h2>
              <p>{data.latency.avg_latency.toFixed(2)} sec</p>
            </div>

            {/* Chart */}
            <div className="bg-white/5 p-6 rounded-xl">
              <h2 className="text-xl mb-4">
                🧠 Embedding Space Visualization
              </h2>

              <Suspense fallback={<p>Loading chart...</p>}>
                <ScatterChartComp data={data.embedding} />
              </Suspense>
            </div>

          </div>
        )}
      </div>

      {/* Footer */}
      <FooterSection />
    </main>
  );
}
