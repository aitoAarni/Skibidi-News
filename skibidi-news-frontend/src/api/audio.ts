import axios from "axios";
import { endpoints } from "./config";

export const synthesizeAudio = async (text: string): Promise<string> => {
  const res = await axios.post(
    endpoints.synthesize,
    { text },
    {
      responseType: "arraybuffer",
    }
  );
  const blob = new Blob([res.data], { type: "audio/mpeg" });
  return URL.createObjectURL(blob);
};
