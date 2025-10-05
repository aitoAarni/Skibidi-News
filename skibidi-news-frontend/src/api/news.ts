import axios from "axios";
import { endpoints } from "./config";

export const fetchNewsSummary = async (): Promise<string> => {
  const res = await axios.get(endpoints.aggregateNews);
  return res.data.summary;
};
