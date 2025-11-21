/**
 * Fetches news from your FastAPI server's /news endpoint.
 * This is the JavaScript equivalent of:
 * curl "http://127.0.0.1:8000/news"
 */

import { endpoints } from "./config";

export type NewsSummaryResponse = {
  summary: string;
  category: string;
  availableCategories: string[];
};

export const fetchNewsSummary = async (
  category?: string
): Promise<NewsSummaryResponse> => {
  const url = new URL(endpoints.aggregateNews);
  if (category) {
    url.searchParams.set("category", category);
  }

  // console.log(url.toString());
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    // console.log("Successfully fetched news:", data);
    return {
      summary: data.summary ?? "",
      category: data.category ?? category ?? "world",
      availableCategories: data.available_categories ?? [],
    };
  } catch (error) {
    console.error("Error fetching news from /news endpoint:", error);
    throw error;
  }
};

// --- Example of how to use it ---
// (async () => {
//   const news = await fetchNewsFromServer();
//   if (news) {
//     // Do something with the news
//   }
// })();
