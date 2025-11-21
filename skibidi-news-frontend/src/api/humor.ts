import { endpoints } from "./config";

/**
 * Calls your FastAPI server's /humorize_news endpoint.
 * This is the JavaScript equivalent of:
 * curl -X POST "http://127.0.0.1:8000/humorize_news" \
 * -H "Content-Type: application/json" \
 * -d '{"news": "A giant panda..."}'
 *
 * @param newsText The text string you want to humorize.
 * @returns The humorized string from the server.
 */
export const humorizeText = async (newsText: string) => {
  // const url = "http://127.0.0.1:8000/humorize_news";
  const url = endpoints.comedicize;

  // 1. Define the data payload
  // Your server's data_classes.py expects a 'News' object,
  // which has a 'news' field: `async def humorizer_route(news: News):`
  const payload = {
    news: newsText,
  };

  try {
    // 2. Make the POST request
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload), // Convert the JS object to a JSON string
    });

    // 3. Check if the response was successful
    if (!response.ok) {
      // If it's a 500 error, log the response text for more details
      const errorText = await response.text();
      console.error("Server responded with an error:", errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // 4. Parse the JSON response
    const data = await response.json();

    // Your server returns: {"huomrized_news": huomrized_text}
    // console.log("Successfully humorized text:", data.huomrized_news);
    return data.huomrized_news;
  } catch (error) {
    console.error("Error calling /humorize_news endpoint:", error);
    throw error;
  }
};

// --- Example of how to use it ---
// (async () => {
//   const originalText = "A giant panda was seen ordering a latte.";
//   const funnyText = await humorizeNewsOnServer(originalText);
//   if (funnyText) {
//     // Do something with the funnyText
//   }
// })();
