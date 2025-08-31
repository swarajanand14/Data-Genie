import re

def sanitize_sql(raw_sql: str, table_name: str) -> str:
    if not raw_sql:
        return raw_sql
    s = raw_sql
    s = re.sub(r'```(?:sql)?', '', s, flags=re.IGNORECASE)
    s = s.replace('```', '').strip()
    s = re.sub(r'^\s*sql[:\s]*', '', s, flags=re.IGNORECASE)
    m = re.search(r'((?:with|select|insert|update|delete)\b.*)', s, flags=re.IGNORECASE | re.DOTALL)
    if m:
        s = m.group(1).strip()
    s = s.replace('`', '').replace('[', '').replace(']', '')
    s = re.sub(r'\byour_table_name\b', table_name, s, flags=re.IGNORECASE)
    s = re.sub(r'\byour_table\b', table_name, s, flags=re.IGNORECASE)
    s = re.sub(r'\btable_name\b', table_name, s, flags=re.IGNORECASE)
    return s.rstrip().rstrip(';')
