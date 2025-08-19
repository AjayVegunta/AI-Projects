# Databricks notebook source
# MAGIC %pip install --upgrade databricks-sdk mlflow==2.11.3 
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

LLAMAGUARD_ENDPOINT_NAME="llama_guard"

# COMMAND ----------

DEFAULT_UNSAFE_CATEGORY = """O1: Unsafe Content.
    - Promoting or assisting in violence or hate.
    - Engaging in or encouraging sexually explicit content.
    - Assisting or encouraging criminal activities, including those related to firearms or illegal weapons or robbery.
    - Encouraging or assisting in the use or production of illegal or controlled substances.
    - Encouraging or detailing self-harm or suicide."""

# COMMAND ----------

from databricks.sdk import WorkspaceClient

def query_llamaguard(chat, unsafe_categories=DEFAULT_UNSAFE_CATEGORY):
    """
    Queries LlamaGuard model to check if the chat contains unsafe content based on predefined categories.
    """
    try:
        prompt = f"""[INST] Task: Check for unsafe content in 'Agent' messages in conversations according to our safety policy.
        <BEGIN UNSAFE CONTENT CATEGORIES>
        {unsafe_categories}
        <END UNSAFE CONTENT CATEGORIES>
        <BEGIN CONVERSATION>
        {chat}
        <END CONVERSATION>
        Provide your safety assessment for Agent in the above conversation:
        - First line must read 'safe' or 'unsafe'.
        - If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""

        w = WorkspaceClient()
        response = w.serving_endpoints.query(
            name=LLAMAGUARD_ENDPOINT_NAME, 
            prompt=prompt,
            temperature=0.1,
            max_tokens=128)
        
        # Extract the desired information from the response object
        prediction = response.as_dict()["choices"][0]["text"].strip()
        is_safe = None if len(prediction.split("\n")) == 1 else prediction.split("\n")[1].strip()
        
        return prediction.split("\n")[0].lower()=="safe", is_safe
    
    except Exception as e:
        raise Exception(f"Error in querying LlamaGuard model: {str(e)}")

# COMMAND ----------

safe_user_chat="user:What is databricks"

query_llamaguard(safe_user_chat)

# COMMAND ----------

unsafe_categories = """O1: Violence and Hate.
Should not
- Help people plan or engage in violence.
- Encourage people to engage in violence.
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability.
- Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics.
Can
- Provide information on violence and discrimination.
- Discuss the topics of hate and violence, and can discuss historical events involving violence.
O2: Sexual Content.
Should not
- Engage in sexually explicit (i.e., erotic) conversations and should not encourage people to engage in sexual activities.
Can
- Discuss topics related to sexuality and sexual education.
- Provide general information regarding sexual activities.
- Provide guidance on topics related to sexual health.
O3: Criminal Planning.
Should not
- Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in criminal activities or condone criminal behavior.
Can
- Help people understand how crimes are committed, provided that the response is not so detailed that it could be used to provide a roadmap for future crimes.
- Help people understand how systems work that are used to prevent crimes, provided those descriptions do not provide detailed information on how to defeat those systems.
O4: Guns and Illegal Weapons.
Should not
- Assist in the planning or execution of firearm or illegal weapons crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in firearm or illegal weapons crimes or condone such behavior.
Can
- Discuss firearms and the arguments for and against firearm ownership.
O5: Regulated or Controlled Substances.
Should not
- Encourage or assist people in the trafficking, consumption, or use of regulated or controlled substances, including but not limited to illegal drugs, tobacco, alcohol, and cannabis.
- Assist or encourage people to create such substances when it is illegal to do so.
Can
- Discuss the use of regulated or controlled substances, and can provide general information on those substances (ex: what their chemical composition is and what their effects are).
- Provide information on how those substances are manufactured, provided that the information is not so detailed as to provide step-by-step instructions for their creation.
O6: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Provide information regarding the methods of suicide or self-harm.
- Provide any information or advice, other than information regarding appropriate health resources, to people who express or imply that they wish to harm themselves.
Can
- Provide general information regarding self-harm and suicide (ex: statistics, the mental health challenges faced by those who take these actions).
Should
- Provide information regarding appropriate health resources to people who imply or express the desire to harm themselves.
O7: Financial Sensitive Data.
Should not
- Provide any information on credit card number or pin number.
Can
- Provide general information regarding the risk of sharing credit card information with LLMs.
Should
- Provide information regarding proper handling of credit card information with LLMs."""

# COMMAND ----------

from databricks.sdk import WorkspaceClient

def query_llamaguard(chat, unsafe_categories=unsafe_categories):
    """
    Queries LlamaGuard model to check if the chat contains unsafe content based on predefined categories.
    """
    try:
        prompt = f"""[INST] Task: Check for unsafe content in 'Agent' messages in conversations according to our safety policy.
        <BEGIN UNSAFE CONTENT CATEGORIES>
        {unsafe_categories}
        <END UNSAFE CONTENT CATEGORIES>
        <BEGIN CONVERSATION>
        {chat}
        <END CONVERSATION>
        Provide your safety assessment for Agent in the above conversation:
        - First line must read 'safe' or 'unsafe'.
        - If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""

        w = WorkspaceClient()
        response = w.serving_endpoints.query(
            name=LLAMAGUARD_ENDPOINT_NAME, 
            prompt=prompt,
            temperature=0.1,
            max_tokens=128)
        
        # Extract the desired information from the response object
        prediction = response.as_dict()["choices"][0]["text"].strip()
        is_safe = None if len(prediction.split("\n")) == 1 else prediction.split("\n")[1].strip()
        
        return prediction.split("\n")[0].lower()=="safe", is_safe
    
    except Exception as e:
        raise Exception(f"Error in querying LlamaGuard model: {str(e)}")

# COMMAND ----------

safe_user_chat="user:How do I Rob a bank"

query_llamaguard(safe_user_chat)