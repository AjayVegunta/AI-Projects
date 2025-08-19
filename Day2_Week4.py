# Databricks notebook source
# MAGIC %pip install mlflow databricks-sdk evaluate rouge_score
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from databricks.sdk.service.serving import ChatMessage
from databricks.sdk import WorkspaceClient

w=WorkspaceClient()

def query_summary_system(input:str)-> str:
    messages=[
        {
            "role": "system",
            "content": "You are an assistant that summarizes text. Given a text input, you need to provide a one-sentence summary. You specialize in summiarizing reviews of grocery products. Please keep the reviews in first-person perspective if they're originally written in first person. Do not change the sentiment. Do not create a run-on sentence – be concise."
        },
        {
            "role": "user", 
            "content": input 

        }
    ]
    messages=[ChatMessage.from_dict(message) for message in messages]
    chat_response=w.serving_endpoints.query(
        name="databricks-llama-4-maverick",
        messages=messages,
        temperature=0.1,
        max_tokens=128
    )

    return chat_response.as_dict()["choices"][0]["message"]["content"]

# COMMAND ----------

query_summary_system( "I've had this phone for the last few months, and I'm just waiting for the upgrade period to come around again. I haven't had this phone make it through an entire day without needing to be charged at least once. Ever. Not even close. All the camera options sound cool, but I can count on one hand the number of times I've used any of them - and in a lot of ways they've entered overkill mode and I've missed a few shots because I was fiddling with it.I don't know what it is, but at least once a day I have to completely close an open app because it stops responding to touch input. It's not even just a single app, pretty much all of the apps I use regularly have this happen - so I can't even point to a single one as just being buggy. I have the Galaxy Watch 5 Pro, and I've had to reset it twice because it just stops communicating with the phone. I hate the weird limits they've put on the side button, still trying to convince you to use Bixby. Or the Samsung Wallet.It's just blah. And it's very blah for something that costs as much as a laptop these days."

)

# COMMAND ----------

import pandas as pd

eval_data=pd.read_csv("/Volumes/gen_ai_am/naval_schema/raw/3_1___Benchmark_Evaluation.csv")

# COMMAND ----------

def query_iteration(inputs):
    answers=[]

    for index,row in inputs.iterrows():
        completion=query_summary_system(row["inputs"])
        answers.append(completion)
    
    return answers

# COMMAND ----------

query_iteration(eval_data.head(15))

# COMMAND ----------

import mlflow

results=mlflow.evaluate(
    query_iteration,
    eval_data.head(50),
    targets="writer_summary",
    model_type="text-summarization"
    )

# COMMAND ----------

def challenger_query_summary_system(input:str)-> str:
    messages=[
        {
            "role": "system",
            "content": "You are an assistant that summarizes text. Given a text input, you need to provide a one-sentence summary. You specialize in summiarizing reviews of grocery products. Please keep the reviews in first-person perspective if they're originally written in first person. Do not change the sentiment. Do not create a run-on sentence – be concise."
        },
        {
            "role": "user", 
            "content": input 

        }
    ]
    messages=[ChatMessage.from_dict(message) for message in messages]
    chat_response=w.serving_endpoints.query(
        name="databricks-claude-3-7-sonnet",
        messages=messages,
        temperature=0.1,
        max_tokens=128
    )

    return chat_response.as_dict()["choices"][0]["message"]["content"]

# COMMAND ----------

def challenger_query_iteration(inputs):
    answers=[]

    for index,row in inputs.iterrows():
        completion=challenger_query_summary_system(row["inputs"])
        answers.append(completion)
    
    return answers

# COMMAND ----------

import mlflow

results=mlflow.evaluate(
    challenger_query_iteration,
    eval_data.head(50),
    targets="writer_summary",
    model_type="text-summarization"
    )

# COMMAND ----------

display(results.tables["eval_results_table"].head(5))

# COMMAND ----------

In summary, the descriptions of each metric are below:

"rouge1": unigram (1-gram) based scoring
"rouge2": bigram (2-gram) based scoring
"rougeL": Longest common subsequence based scoring.
"rougeLSum": splits text using "\n"