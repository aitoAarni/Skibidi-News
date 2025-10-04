import axios from "axios";

export const humorizeText = async (text) => {
  const res = await axios.post(
    "http://localhost:8001/mcp-humorizer/comedicize",
    {
      id: "frontend-request",
      summarized_text: text,
    }
  );
  return res.data.comedic_text;
};
