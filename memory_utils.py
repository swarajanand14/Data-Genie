import streamlit as st

def get_memory():
    """Retrieve the memory object from Streamlit session state."""
    if "memory" not in st.session_state:
        st.session_state.memory = []
    return st.session_state.memory

def add_to_memory(question, sql, result, answer):
    """Add a new interaction to memory."""
    memory = get_memory()
    memory.append({
        "question": question,
        "sql": sql,
        "result": result,
        "answer": answer
    })
    # Keep only the last 10 interactions
    if len(memory) > 10:
        memory.pop(0)

def clear_memory():
    """Clear the memory."""
    st.session_state.memory = []