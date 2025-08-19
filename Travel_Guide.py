# Databricks notebook source
# MAGIC %run "/Workspace/Users/ajay.vegunta@smoothstack.com/Gen-AI/Prompt/include"

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatDatabricks


llm = ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")

prompt_template=PromptTemplate(
    input_variable=["country","no","language"],
    template="""You are an expert in Travel related queries.
    You provide information about a country.
    Avoid giving information about fictional places. If its fictional place just give output as 'I dont know'
    Answer the question: What are the places to visit in {country}.
    divide the days to spend in{no} each place and what would be the your average budget{money}
    """)
country=input("Enter country: ")
no=int(input("Enter no of days: "))
money=int(input("Enter amount: "))
if country:
    response=llm.invoke(prompt_template.format(country=country,no=no,money=money))
    print(response.content)

# COMMAND ----------

# MAGIC %pip install databricks-langchain

# COMMAND ----------

from langchain_core.messages import HumanMessage, SystemMessage
from databricks_langchain import ChatDatabricks

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content="What is a mixture of experts model?"),
]

llm = ChatDatabricks(endpoint_name="databricks-claude-3-7-sonnet")
llm.invoke(messages)

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

w = WorkspaceClient()
response = w.serving_endpoints.query(
    name="databricks-meta-llama-3-3-70b-instruct",
    messages=[
        ChatMessage(
            role=ChatMessageRole.SYSTEM, content="You are a helpful assistant."
        ),
        ChatMessage(
            role=ChatMessageRole.USER, content="What is a mixture of experts model?"
        ),
    ],
    max_tokens=128,
)
print(f"RESPONSE:\n{response.choices[0].message.content}")

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm=ChatOpenAI(model="gpt-4o")

title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Answer exactly with one title.	"""
)

speech_prompt=PromptTemplate(
        input_variables=["title"],
        template="""You need to write a powerful speech of 250 words 
        for the following title:{title}
        """
)

first_chain=title_prompt | llm
second_chain=speech_prompt | llm
final_chain=first_chain | second_chain



response=final_chain.invoke({"topic":"AI"})
print(response.content)

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatDatabricks

llm1=ChatOpenAI(model="gpt-4o")
llm2= ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")


title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Answer exactly with one title.	"""
)

speech_prompt=PromptTemplate(
        input_variables=["title"],
        template="""You need to write a powerful speech of 250 words 
        for the following title:{title}
        """
)

first_chain=title_prompt | llm1 | StrOutputParser() | (lambda title:(print(title),title)[1])
second_chain=speech_prompt | llm2
final_chain=first_chain | second_chain


print("Speech Generator App")

topic=input("Enter the topic for the speech: ")

if topic:
    response=final_chain.invoke({"topic":topic})
    print(response.content)

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_databricks import ChatDatabricks

llm1=ChatDatabricks(endpoint="databricks-meta-llama-3-1-8b-instruct")
llm2=ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")


title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Answer exactly with one title.	"""
)

speech_prompt=PromptTemplate(
        input_variables=["title","emotion"],
        template="""You need to write a powerful {emotion} speech of 250 words 
        for the following title:{title}
        """
)

first_chain=title_prompt | llm1 | StrOutputParser() | (lambda title:(print(title),title)[1])
second_chain=speech_prompt | llm2
final_chain=first_chain | (lambda title:{"title":title,"emotion":emotion})|second_chain


print("Speech Generator App")

topic=input("Enter the topic for the speech: ")
emotion=input("Enter the emotion for the speech: ")

if topic:
    response=final_chain.invoke({"topic":topic})
    print(response.content)

# COMMAND ----------

# MAGIC %sql
# MAGIC Use 2 different LLMS. 
# MAGIC
# MAGIC Blog Post Generator:
# MAGIC   You are a professional blogger.
# MAGIC     Create an outline for a blog post on the following topic: {topic}
# MAGIC     The outline should include:
# MAGIC     - Introduction
# MAGIC     - 3 main points with subpoints
# MAGIC     - Conclusion
# MAGIC
# MAGIC
# MAGIC   You are a professional blogger.
# MAGIC     Write an engaging introduction paragraph based on the following
# MAGIC     outline:{outline}
# MAGIC     The introduction should hook the reader and provide a brief
# MAGIC     overview of the topic

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_databricks import ChatDatabricks

llm1=ChatDatabricks(endpoint="databricks-meta-llama-3-1-8b-instruct")
llm2=ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")


title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    You are an experienced blogger.
    You need to create an outline for a blog post on the following topic: {topic}
    the guidline should include the following sections: 10 main points with nummbers and conclusion	"""
)

speech_prompt=PromptTemplate(
        input_variables=["guideline"],
        template=""" Write an engaging paragraph based on the following
    guideline:{guideline} please follow guideline
    The introduction should hook the reader and provide a brief
    overview of the topic
        """
)

first_chain=title_prompt | llm1 
second_chain=speech_prompt | llm2
final_chain=first_chain |second_chain


print("Speech Generator App")

topic=input("Enter the topic for the blog: ")

if topic:
    response=final_chain.invoke({"topic":topic})
    print(response.content)

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_databricks import ChatDatabricks

llm1=ChatDatabricks(endpoint="databricks-meta-llama-3-1-8b-instruct")
llm2=ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")


title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Answer exactly with one title.	"""
)

speech_prompt=PromptTemplate(
        input_variables=["title","emotion"],
        template="""You need to write a powerful {emotion} speech of 250 words 
        for the following title:{title}
        """
)

first_chain=title_prompt | llm1 | StrOutputParser() | (lambda title:(print(title),title)[1])
second_chain=speech_prompt | llm2
final_chain=first_chain | (lambda title:{"title":title,"emotion":emotion})|second_chain


print("Speech Generator App")

topic=input("Enter the topic for the speech: ")
emotion=input("Enter the emotion for the speech: ")

chunks=[]
for chunk in final_chain.stream({"topic":topic,"emotion":emotion}):
    chunks.append(chunk)
    print(chunk.content, end="")