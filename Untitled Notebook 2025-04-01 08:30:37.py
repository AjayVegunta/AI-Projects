# Databricks notebook source
# MAGIC %pip install --upgrade --quiet  langchain langchain-community langchainhub langchain-openai langchain-databricks 
# MAGIC
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

OPENAI_API_KEY='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'

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
