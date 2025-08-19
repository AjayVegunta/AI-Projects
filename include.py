# Databricks notebook source
# MAGIC %pip install --upgrade --quiet  langchain langchain-community langchainhub langchain-openai langchain-databricks langchain-chroma
# MAGIC
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

OPENAI_API_KEY='6bDf4n0xOq8QA'

# COMMAND ----------

import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
