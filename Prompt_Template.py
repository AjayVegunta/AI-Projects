# Databricks notebook source
# MAGIC %run "/Workspace/Users/ajay.vegunta@smoothstack.com/Gen-AI/Prompt/include"

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm=ChatOpenAI(model="gpt-4o")

prompt_template=PromptTemplate(
    input_variable=["country"],
    template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Answer the question: What is the traditional cuisine of {country}
    """)

response=llm.invoke(prompt_template.format(country="USA"))
print(response.content)

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatDatabricks


llm = ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")

prompt_template=PromptTemplate(
    input_variable=["country","no","language"],
    template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Avoid giving information about fictional places. If its fictional place just give output as 'I dont know'
    Answer the question: What is the traditional cuisine of {country}.
    no of para {no} and language {language}
    """)
country=input("Enter country: ")
no=int(input("Enter no of para: "))
language=input("Enter language: ")

response=llm.invoke(prompt_template.format(country=country,no=no,language=language))
print(response.content)

# COMMAND ----------

pip install streamlit

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatDatabricks
import streamlit as st


llm = ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")

prompt_template=PromptTemplate(
    input_variable=["country","no","language"],
    template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Avoid giving information about fictional places. If its fictional place just give output as 'I dont know'
    Answer the question: What is the traditional cuisine of {country}.
    no of para {no} and language {language}
    """)
st.title("Traditional Cuisine")
country=st.text_input("Enter country: ")
no=int(st.number_input("Enter no of para: "))
language=st.text_input("Enter language: ")
if country:
    response=llm.invoke(prompt_template.format(country=country,no=no,language=language))
    st.write(response.content)

# COMMAND ----------

!streamlit run /databricks/python_shell/scripts/db_ipykernel_launcher.py