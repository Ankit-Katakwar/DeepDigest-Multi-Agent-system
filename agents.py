from tools import web_search , scrap_search
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import StrOutputParser

llm = ChatMistralAI(
    model = "mistral-medium-latest"
    )

report_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert research writer. Write clean , structured and insightful reports"""
    ),
    (
        "human",
        """ Writer a detailed research report on the topic below.
        Topic :{topic}

        Reaearch Gathered:
        {research}

        Structure the report as:
        - Introduction 
        - Key finding(minimum 3 well-explained points)
        - Conclusion
        - Sources (List all the urls found in the research)

        be detailed, factual and professional.
        """
    ),
    
])

report_chain = report_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate([
    ("system","You are sharp and constructive research critic. Be honest and specific."),
    ("human","""
Review the reseach report below and evaluate it strictly.
     Report :{report}

     Respont in this exact formate:
    Score:X/10
     
     Strength: 
     -...
     -...
     Area to imporve:
     -...
     -...

    One line verdict:
     ...

""")
])

critic_chain = critic_prompt | llm | StrOutputParser()



def bulid_search_agent():
    return create_agent(
        model= llm , 
        tools=[web_search]
    )

def scrap_agent():
    return create_agent(
        model = llm,
        tools=[scrap_search]
    ) 

