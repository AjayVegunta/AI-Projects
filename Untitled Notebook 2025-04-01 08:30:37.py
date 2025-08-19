# Databricks notebook source
# MAGIC %pip install --upgrade --quiet  langchain langchain-community langchainhub langchain-openai langchain-databricks 
# MAGIC
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

OPENAI_API_KEY='A'

# COMMAND ----------

import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# COMMAND ----------

from langchain_openai import ChatOpenAI

llm=ChatOpenAI(model="gpt-4o")
question=input("Enter a question")
response=llm.invoke(question)
print(response.content)

# COMMAND ----------

from langchain.chat_models import ChatDatabricks

llm = ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")
question=input("Enter a question")
response=llm.invoke(question)
print(response.content)
