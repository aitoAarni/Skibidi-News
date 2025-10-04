import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

export default function AudioPanel({ text }: { text: string }) {
  const [audioUrl, setAudioUrl] = useState("");

  const handleGenerate = async () => {
    const res = await axios.post(
      "http://localhost:8002/text-to-audio/synthesize",
      { text },
      {
        responseType: "arraybuffer",
      }
    );
    const blob = new Blob([res.data], { type: "audio/mpeg" });
    setAudioUrl(URL.createObjectURL(blob));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-md p-6"
    >
      <h3 className="text-lg font-semibold mb-3">🔊 Audio Studio</h3>
      <button
        onClick={handleGenerate}
        className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition"
      >
        Generate Audio
      </button>
      {audioUrl && <audio controls src={audioUrl} className="w-full mt-4" />}
    </motion.div>
  );
}
