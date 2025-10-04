import axios from "axios";

export const synthesizeAudio = async (text) => {
  const res = await axios.post(
    "http://localhost:8002/text-to-audio/synthesize",
    { text },
    {
      responseType: "arraybuffer",
    }
  );
  const blob = new Blob([res.data], { type: "audio/mpeg" });
  return URL.createObjectURL(blob);
};
