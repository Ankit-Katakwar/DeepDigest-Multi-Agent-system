from agents import critic_chain , report_chain , bulid_search_agent , scrap_agent
from rich import print

def run_research_pipeline(topic:str)-> dict:

    state = {}  
    
    print("\n"+"="*50)
    print("Step 1 - Search agent is working........")
    print("="*50)

    search_agent = bulid_search_agent()
    searchResult = search_agent.invoke({
        "messages":[("user",f"Find recent , reliable and detailed information about:{topic}")]
    })
    state["searchResult"]= searchResult["messages"][-1].content
    print("\n search result", state["searchResult"])

    print("\n"+"="*50)
    print("Step 2 - Scraping the detailed informatin from the sources.........")
    print("="*50)

    scrapAgent = scrap_agent()
    scrapResult = scrapAgent.invoke({
        "messages":[("user",
                     f"Based on the following search result about '{topic}',"
                     f"pick the most relavent URL and scrape it for more deeper content.\n\n"
                     f"Search result:\n{state['searchResult'][:800]}"
                     )]
    })

    state["scrapResult"]= scrapResult["messages"][-1].content

    print("\n Scrap result", state["scrapResult"])


    print("\n"+"="*50)
    print("Step 3 - Final report in making.........")
    print("="*50)

    cominedReport =(
        f"webResearch:{state["searchResult"]}\n\n"
        f"scrapeResearch : {state["scrapResult"]} "
    )

    report_result = report_chain.invoke(
        {"topic" : topic,
        "research":cominedReport }

    )
    state["finalReport"] = report_result

    print(f"\n\nThe final report is : \n{state["finalReport"]}\n\n")


    print("\n"+"="*50)
    print("Step 4 - Critic is reviewing.........")
    print("="*50)

    state["criticResult"] = critic_chain.invoke({
        "report":state["finalReport"]
    })

    print(f"\n\nThe Critic report is : \n{state["criticResult"]}\n\n")

    return state 




if __name__ == "__main__":
    topic = input("\n Enter a topic for deep research.")
    run_research_pipeline(topic)

