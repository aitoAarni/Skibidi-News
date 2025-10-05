import axios from "axios";
import { endpoints } from "./config";

export type BestPromptResponse = {
  prompt_pack?: Record<string, any>;
  note?: string;
  error?: string;
};

export const fetchBestPrompt = async (
  prompt: string,
  summary: string,
  allowQuickOpt = true
): Promise<BestPromptResponse> => {
  const res = await axios.post(endpoints.bestPrompt, {
    prompt,
    summary,
    allow_quick_opt: allowQuickOpt,
  });
  return res.data as BestPromptResponse;
};
