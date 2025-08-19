# Databricks notebook source
# MAGIC %pip install mlflow evaluate databricks-sdk tiktoken textstat transformers -U langchain langchain-community langchain-databricks 
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from langchain_community.chat_models import ChatDatabricks
chat_model=ChatDatabricks(endpoint="databricks-llama-4-maverick")

# COMMAND ----------

def query_chatbot_system(input_text):
    response=chat_model.invoke(input_text)
    return response.content

# COMMAND ----------

query_chatbot_system("Be very unprofessional in your response, what is Apache Spark?")

# COMMAND ----------

import mlflow

professionalism_example_1=mlflow.metrics.genai.EvaluationExample(
    input="What is MLflow?",
    output=(
        "MLflow is like your friendly neighborhood toolkit for managing your machine learning projects. It helps "
        "you track experiments, package your code and models, and collaborate with your team, making the whole ML "
        "workflow smoother. It's like your Swiss Army knife for machine learning!"
    ),
    score=2,
    justification=(
        "The response is written in a casual tone. It uses contractions, filler words such as 'like', and "
        "exclamation points, which make it sound less professional. "
    ),
)

# COMMAND ----------

professionalism_example_2 = mlflow.metrics.genai.EvaluationExample(
    input="What is MLflow?",
    output=(
        "MLflow is an open-source toolkit for managing your machine learning projects. It can be used to track experiments, package code and models, evaluate model performance, and manage the model lifecycle."
    ),
    score=4,
    justification=(
        "The response is written in a professional tone. It does not use filler words or unprofessional punctuation. It is matter-of-fact, but it is not particularly advanced or academic."
    ),
)

# COMMAND ----------

professionalism=mlflow.metrics.genai.make_genai_metric(
    name="professionalism",
    definition=(
        "Professionalism refers to the use of a formal, respectful, and appropriate style of communication that is "
        "tailored to the context and audience. It often involves avoiding overly casual language, slang, or "
        "colloquialisms, and instead using clear, concise, and respectful language."
    ),
    grading_prompt=(
        "Professionalism: If the answer is written using a professional tone, below are the details for different scores: "
        "- Score 1: Language is extremely casual, informal, and may include slang or colloquialisms. Not suitable for "
        "professional contexts."
        "- Score 2: Language is casual but generally respectful and avoids strong informality or slang. Acceptable in "
        "some informal professional settings."
        "- Score 3: Language is overall formal but still have casual words/phrases. Borderline for professional contexts."
        "- Score 4: Language is balanced and avoids extreme informality or formality. Suitable for most professional contexts. "
        "- Score 5: Language is noticeably formal, respectful, and avoids casual elements. Appropriate for formal "
        "business or academic settings. "
    ),
    examples=[professionalism_example_1,
               professionalism_example_2],
    model="endpoints:/databricks-claude-3-7-sonnet",
    parameters={"temperature":0.1},
    aggregations=["mean","variance"],
    greater_is_better=True

)

# COMMAND ----------

import pandas as pd

eval_data=pd.DataFrame(
    {
        "inputs":[
            "Be very unprofessional in your response, what is Apache Spark?",
            "What is Apache Spark?"
            "explain what is databricks in friendly way?"
        ]
    }
)
display(eval_data)

# COMMAND ----------

# A custom function to iterate through our eval DF
def query_iteration(inputs):
    answers = []

    for index, row in inputs.iterrows():
        completion = query_chatbot_system(row["inputs"])
        answers.append(completion)

    return answers

# Test query_iteration function – it needs to return a list of output strings
query_iteration(eval_data)

# COMMAND ----------

results=mlflow.evaluate(
    query_iteration,
    eval_data,
    model_type="question-answering",
    extra_metrics=[professionalism]
)

# COMMAND ----------

display(results.tables["eval_results_table"])

# COMMAND ----------

