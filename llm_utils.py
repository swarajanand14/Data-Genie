from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

def get_llm(api_key):
    return ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

def get_sql_prompt():
    return PromptTemplate(
        input_variables=["table", "columns", "question"],
        template="""
You are an SQL generator for SQLite. There is a single table named "{table}" with the following columns:

{columns}

Rules:
- Always use "{table}" as table name.
- Use column names exactly as listed.
- No markdown fences, no commentary, no backticks or brackets.
- Return ONLY a single SQL statement.

User question:
{question}
"""
    )

def get_answer_prompt(schema, user_q, val):
    return f"""
You are a BI assistant. Based on the following information, generate a very short one-sentence answer.

Table schema: {schema}
User question: {user_q}
Query result: {val}
"""
