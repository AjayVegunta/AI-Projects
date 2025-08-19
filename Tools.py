# Databricks notebook source
# MAGIC %run "/Workspace/Users/ajay.vegunta@smoothstack.com/Gen-AI/Prompt/include"

# COMMAND ----------

from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# COMMAND ----------

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())