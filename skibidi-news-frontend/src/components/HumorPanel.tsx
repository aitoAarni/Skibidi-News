import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

export default function HumorPanel({ summary }: { summary: string }) {
  const [humor, setHumor] = useState("");

  const handleHumorize = async () => {
    const res = await axios.post(
      "http://localhost:8001/mcp-humorizer/comedicize",
      {
        summarized_text: summary,
      }
    );
    setHumor(res.data.comedic_text);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-md p-6"
    >
      <h3 className="text-lg font-semibold mb-3">🤣 Comedic Version</h3>
      <button
        onClick={handleHumorize}
        className="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition"
      >
        Make It Funny
      </button>
      {humor && (
        <p className="mt-4 text-slate-800 italic border-l-4 border-pink-400 pl-4">
          {humor}
        </p>
      )}
    </motion.div>
  );
}
