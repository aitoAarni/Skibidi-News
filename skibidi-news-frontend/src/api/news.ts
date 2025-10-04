import axios from "axios";

export const fetchNewsSummary = async () => {
  const res = await axios.get(
    "http://localhost:8000/mcp-news-aggr/aggregate_news"
  );
  return res.data.summary;
};
