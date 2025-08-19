# Databricks notebook source
# MAGIC %run "/Workspace/Users/ajay.vegunta@smoothstack.com/Gen-AI/Prompt/include"

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from langchain_databricks import DatabricksEmbeddings

embedding=DatabricksEmbeddings(endpoint="databricks-gte-large-en")
text=input("enter the text")
response=embedding.embed_query(text)
print(response)

# COMMAND ----------

import numpy as np

# COMMAND ----------

from langchain_databricks import DatabricksEmbeddings

embedding=DatabricksEmbeddings(endpoint="databricks-bge-large-en")


text1=input("enter the text:")
text2=input("enter the text:")

response1=embedding.embed_query(text1)
response2=embedding.embed_query(text2)


similarity = np.dot(response1, response2)

print(similarity*100,"%")