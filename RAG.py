# Databricks notebook source
# MAGIC %run "/Workspace/Users/ajay.vegunta@smoothstack.com/Gen-AI/Prompt/include"

# COMMAND ----------

from langchain_databricks import ChatDatabricks, DatabricksEmbeddings 
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# COMMAND ----------

#loading document
document=TextLoader("/Workspace/Users/ajay.vegunta@smoothstack.com/Gen-AI/Embedding/product-data.txt").load()

#chunking 
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=20)

chunks=text_splitter.split_documents(document)

embedding=DatabricksEmbeddings(endpoint="databricks-bge-large-en")
llm=ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")

vectore_store=Chroma.from_documents(chunks,embedding)

retreiver=vectore_store.as_retriever()

prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system",""" You are an assistance for anserwing questions. 
   Use the provided context to respond. If the answer isn't clear, acknowledge that you don't know. Limit your response to three concise sentences.{context} 
   """),
        ("human","{input}")
    ]
)

qa_chain=create_stuff_documents_chain(llm,prompt_template )

rag_chain=create_retrieval_chain(retreiver,qa_chain)


print("Chat with your Data")

question=input("enter your question:")

if question:
    response=rag_chain.invoke({"input":question})
    print(response['answer'])