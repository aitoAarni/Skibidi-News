import { motion } from "framer-motion";
import { useState } from "react";
import axios from "axios";

export default function NewsPanel() {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    setLoading(true);
    const res = await axios.get(
      "http://localhost:8000/mcp-news-aggr/aggregate_news"
    );
    setSummary(res.data.summary);
    setLoading(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-md p-6"
    >
      <h3 className="text-lg font-semibold mb-3">🗞️ Latest Summarized News</h3>
      <button
        onClick={handleFetch}
        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
      >
        {loading ? "Loading..." : "Fetch News"}
      </button>
      {summary && (
        <p className="mt-4 text-slate-700 leading-relaxed">{summary}</p>
      )}
    </motion.div>
  );
}
