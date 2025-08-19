# Databricks notebook source
# MAGIC %pip install mlflow==2.10.1 langchain==0.1.5 databricks-vectorsearch==0.22 databricks-sdk==0.18.0 mlflow[databricks]
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import os

host = "https://" + spark.conf.get("spark.databricks.workspaceUrl")
os.environ['DATABRICKS_TOKEN'] = "dapiccdbc7db6c8410c71d77c8b3b90889a2" # access outside the databricks 

index_name="gen_ai_am.ajay_db.Samsung_Ajay_Rag"
host = "https://" + spark.conf.get("spark.databricks.workspaceUrl")

VECTOR_SEARCH_ENDPOINT_NAME="ss_rag"

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.embeddings import DatabricksEmbeddings

embedding_model = DatabricksEmbeddings(endpoint="databricks-bge-large-en")

def get_retriever(persist_dir: str = None):
    os.environ["DATABRICKS_HOST"] = host
    #Get the vector search index
    vsc = VectorSearchClient(workspace_url=host, personal_access_token=os.environ["DATABRICKS_TOKEN"],disable_notice=True)
    vs_index = vsc.get_index(
        endpoint_name=VECTOR_SEARCH_ENDPOINT_NAME,
        index_name=index_name
    )

    # Create the retriever
    vectorstore = DatabricksVectorSearch(
        vs_index, text_column="text", embedding=embedding_model
    )
    return vectorstore.as_retriever()


# COMMAND ----------

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatDatabricks

chat_model = ChatDatabricks(endpoint="databricks-dbrx-instruct", max_tokens = 200)

TEMPLATE = """You are an assistant for home appliance users. You are answering how to, maintenance and troubleshooting questions regarding the appliances you have data on. If the question is not related to one of these topics, kindly decline to answer. If you don't know the answer, just say that you don't know, don't try to make up an answer. If the question appears to be for an appliance you don't have data on, say so.  Keep the answer as concise as possible.  Provide all answers only in English.
Use the following pieces of context to answer the question at the end:
{context}
Question: {question}
Answer:
"""
prompt = PromptTemplate(template=TEMPLATE, input_variables=["context", "question"])

chain = RetrievalQA.from_chain_type(
    llm=chat_model,
    chain_type="stuff",
    retriever=get_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

# COMMAND ----------

question={"query":"What you need to know about the safety instructions"}
answer=chain.run(question)
print(answer)

# COMMAND ----------

# MAGIC %pip install mlflow

# COMMAND ----------

import mlflow
from mlflow.models import infer_signature
import langchain

mlflow.set_registry_uri("databricks-uc")
model_name="gen_ai_am.ajay_db.samsung_chatbot"

with mlflow.start_run(run_name="samsung_chatbot") as run:
    signature=infer_signature(question,answer)
    model_info=mlflow.langchain.log_model(
     chain,
     loader_fn=get_retriever,
     artifact_path="chain",
     registered_model_name=model_name,
     input_example=question,
     signature=signature
    )