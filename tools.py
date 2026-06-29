from dotenv import load_dotenv
load_dotenv()
from langchain_core.tools import tool 
from tavily import TavilyClient
import os
import requests
from bs4 import BeautifulSoup
client = TavilyClient(
        api_key=os.getenv("TAVILY_API_KEY")
    )

@tool
def web_search(topic:str)->str:
    """This will web search about the topic and give the latest and accurate information."""
    
    result = client.search(
        query=topic,
        max_results=5,

    )
    list = []
    for i in result["results"]:
        list.append(
            f"Title: {i["title"]}\nURL:{i["url"]}\nSnippet:{i["content"][:300]}\n"
        )

    return "\n-----\n".join(list)


@tool
def scrap_search(url:str)->str:
    """This will scrape information from web pages through the urls."""
    try:
        res = requests.get(
            url,
            timeout= 10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(res.text , "html.parser")
        for tag in soup(["script", "footer","nav","style"]):
            tag.decompose()
        return soup.get_text(separator= "", strip=True)[:3000]
    
    except Exception as err:
        return f"There is some problem occured as {str(err)}"
    
