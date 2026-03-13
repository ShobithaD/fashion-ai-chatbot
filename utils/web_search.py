from tavily import TavilyClient
from config.config import TAVILY_API_KEY

client = TavilyClient(api_key="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")

def search_web(query):

    response = client.search(query=query,max_results=3)

    results=""

    for r in response["results"]:
        results+=r["content"]+"\n"

    return results