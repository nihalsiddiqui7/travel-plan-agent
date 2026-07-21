from tavily import TavilyClient
from dotenv import load_dotenv
import os


load_dotenv()



tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query: str):
    """
    Search for travel-related information using the Tavily API.

    Args:
        query (str): The search query."""

    response = tavily_client.search(query,max_results=5)

    cleaned_response = []

    for i,r in enumerate(response["results"]):
        title = r.get("title", "Unknown Title")
        url = r.get("url", "No URL")
        snippet = r.get("content", "No Snippet").strip()

        if len(snippet) > 300:
            snippet = snippet[:300] + "..."

        cleaned_response.append(f"{i+1}. {title}\nURL: {url}\nSnippet: {snippet}\n")

    return "\n".join(cleaned_response)


# if __name__ == "__main__":
#     query = input("Enter your travel-related search query: ")
#     results = tavily_search(query)
#     print("\nSearch Results:\n")
#     print(results)

