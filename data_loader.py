import re
import pandas as pd
import sqlite3

def clean_column_name(col: str) -> str:
    cleaned = col.strip()
    cleaned = re.sub(r'[\s\-]+', '_', cleaned)
    cleaned = re.sub(r'[^\w]', '', cleaned)  
    cleaned = cleaned.lower()
    if re.match(r'^\d', cleaned):
        cleaned = 'c_' + cleaned
    return cleaned or "col"

def load_file(uploaded_file):
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, sheet_name=0)
    return df

def clean_and_rename(df):
    original_columns = list(df.columns)
    cleaned_columns = [clean_column_name(c) for c in original_columns]
    rename_map = dict(zip(original_columns, cleaned_columns))
    df.rename(columns=rename_map, inplace=True)
    return df, original_columns, cleaned_columns

def create_sqlite_table(df, table_name="data"):
    conn = sqlite3.connect(":memory:")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    return conn

def get_schema_info(conn, table_name="data"):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema_info = cursor.fetchall()
    cols_for_prompt = ", ".join([f"{col[1]} ({col[2]})" for col in schema_info])
    return cols_for_prompt
