import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from data_loader import load_file, clean_and_rename, create_sqlite_table, get_schema_info
from sql_utils import sanitize_sql
from llm_utils import get_llm, get_sql_prompt
from viz_utils import show_results
from memory_utils import get_memory, add_to_memory, clear_memory
from chart_utils import customize_chart

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Conversational BI", layout="wide")
st.title("🤖 Data Genie")

# File upload
uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
if not uploaded_file:
    st.info("Upload a CSV or Excel file to get started.")
    st.stop()

# Load and clean the file
df = load_file(uploaded_file)
df, original_columns, cleaned_columns = clean_and_rename(df)

# Display preview of the cleaned data
st.subheader("Preview (cleaned column names)")
st.dataframe(df.head())

# Display column name mapping
with st.expander("Column name mapping (original → cleaned)"):
    for o, n in zip(original_columns, cleaned_columns):
        st.write(f"- `{o}` → `{n}`")

# Create SQLite table and get schema
conn = create_sqlite_table(df)
table_name = "data"
schema = get_schema_info(conn, table_name)

st.markdown("**Detected table schema (sent to the LLM):**")
st.code(f"Table: {table_name}\nColumns: {schema}", language="sql")

# Initialize LLM and prompt
llm = get_llm(OPENAI_API_KEY)
sql_prompt = get_sql_prompt()

# Sidebar: Conversation History and Clear Memory
with st.sidebar:
    st.header("Settings")
    
    # Display conversation history
    st.subheader("Conversation History")
    memory = get_memory()
    if memory:
        for i, interaction in enumerate(memory):
            st.write(f"**Q{i+1}:** {interaction['question']}")
            st.code(interaction['sql'], language="sql")
            st.dataframe(pd.DataFrame(interaction['result']))
            st.success(interaction['answer'])
    else:
        st.write("No conversation history available.")

    # Clear memory button
    if st.button("Clear Memory"):
        clear_memory()
        st.success("Memory cleared!")

# User input for natural language question
user_q = st.text_input("Ask a question about your data in plain English:")
if user_q:
    try:
        # Include conversation history in the prompt
        memory_context = "\n".join(
            [f"Q: {m['question']}\nA: {m['answer']}" for m in memory]
        )
        full_prompt = sql_prompt.format(
            table=table_name,
            columns=schema,
            question=f"{memory_context}\nQ: {user_q}"
        )

        # Generate SQL using LLM
        raw = llm.invoke(full_prompt).content.strip()
        sql = sanitize_sql(raw, table_name)
        st.markdown("### 🔍 Generated & sanitized SQL")
        st.code(sql, language="sql")

        # Execute SQL and display results
        result_df = pd.read_sql_query(sql, conn)
        show_results(result_df, llm, schema, user_q)

        # Add interaction to memory
        add_to_memory(user_q, sql, result_df.to_dict(), "Results displayed successfully.")

    except Exception as e:
        st.error(f"❌ SQL Execution Error: {e}")
        st.write("Raw LLM output (for debugging):")
        st.code(raw)