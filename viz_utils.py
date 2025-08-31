import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import io

def show_results(result_df, llm, schema, user_q):
    if result_df.shape == (1, 1):
        val = result_df.iloc[0, 0]
        from llm_utils import get_answer_prompt
        answer_prompt = get_answer_prompt(schema, user_q, val)
        answer = llm.invoke(answer_prompt).content.strip()
        st.success(answer)

    elif result_df.shape[1] == 2:
        col_x, col_y = result_df.columns[0], result_df.columns[1]
        if "date" in col_x.lower():
            try:
                result_df[col_x] = pd.to_datetime(result_df[col_x])
            except Exception:
                pass

        st.subheader("📊 Result")
        col1, col2 = st.columns(2)  # Create two columns for side-by-side layout

        with col1:
            st.write("### Table")
            st.dataframe(result_df)

            # Add a download button for the table
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Table as CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )

        with col2:
            st.write("### Chart")
            fig, ax = plt.subplots(figsize=(5, 3))
            if pd.api.types.is_datetime64_any_dtype(result_df[col_x]) or "date" in col_x.lower():
                result_df.sort_values(col_x).plot(x=col_x, y=col_y, kind="line", marker="o", ax=ax)
                ax.set_title(f"{col_y} over {col_x}")
            elif result_df[col_x].nunique() <= 8:
                result_df.set_index(col_x)[col_y].plot(kind="pie", autopct="%1.1f%%", ax=ax)
                ax.set_ylabel("")
                ax.set_title(f"Distribution of {col_y} by {col_x}")
            else:
                result_df.plot(x=col_x, y=col_y, kind="bar", ax=ax)
                ax.set_title(f"{col_y} by {col_x}")
            st.pyplot(fig)
    else:
        st.subheader("📋 Result (table)")
        st.dataframe(result_df)

        # Add a download button for the table
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Table as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv"
        )