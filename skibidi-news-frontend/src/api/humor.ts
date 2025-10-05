import axios from "axios";
import { endpoints } from "./config";

export const humorizeText = async (text: string): Promise<string> => {
  const res = await axios.post(endpoints.comedicize, {
    id: "frontend-request",
    summarized_text: text,
  });
  return res.data.comedic_text as string;
};
