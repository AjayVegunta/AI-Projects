# Databricks notebook source
# MAGIC %run "/Workspace/Users/naval.yemul@smoothstack.com/SS_GenAI_AM/Gen AI/include"

# COMMAND ----------

# MAGIC %pip install -qU duckduckgo-search langchain-community

# COMMAND ----------

from langchain_community.chat_models import ChatDatabricks
from langchain.prompts import PromptTemplate
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import YouTubeSearchTool
from langchain.agents import Tool,initialize_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools.ddg_search.tool import DuckDuckGoSearchResults

# COMMAND ----------

chat_model= ChatDatabricks(endpoint="databricks-llama-4-maverick")


#define tools
wiki_tools=Tool(
    name="Wikipedia",
    func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run,
    description="Search wikipedia for {topic} information"
)
search = DuckDuckGoSearchResults()

search.invoke("Obama")

tools=[wiki_tools,youtube_tool]


agent=initialize_agent(
    tools=tools,
    llm=chat_model,
    agent="zero-shot-react-description",
    verbose=True
)

print("Hello, I am a chatbot. Ask me anything about a movie")
type_movie=input("What type of movie are you interested in? ")
try:
    movie_type=f"suggest a {type_movie} movie in YouTube"
    if movie_type:
        response=agent.run({"input":movie_type})
        print(response)
except Exception as e:
    print("Error",e)

# COMMAND ----------

chat_model = ChatDatabricks(endpoint="databricks-llama-4-maverick")

wiki_tool = Tool(
    name="Wikipedia",
    func=WikipediaAPIWrapper().run,
    description="Search Wikipedia for general background information on a topic"
)

search_tool = Tool(
    name="DuckDuckGo",
    func=DuckDuckGoSearchResults().run,
    description="Search DuckDuckGo for current events or recent details about a topic"
)
tools = [wiki_tool, search_tool]


agent = initialize_agent(
    tools=tools,
    llm=chat_model,
    agent="zero-shot-react-description",
    verbose=True
)


print("Welcome to the Research Assistant!")
topic = input("Enter a topic you'd like to research: ")

try:
    query = f"Research and summarize information about: {topic}"
    response = agent.run(query)
    print("\n Research Summary:\n", response)

except Exception as e:
    print("Error:", e)

# COMMAND ----------

