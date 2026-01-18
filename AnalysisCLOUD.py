import streamlit as st
import pandas as pd
from google import genai
import io

# --- PAGE CONFIG & UI ---
st.set_page_config(page_title="AI Sales Analyst 2026", layout="wide")
st.title("📊 AI Sales Analyst")

with st.sidebar:
    st.header("Setup")
    # Pre-filled API Key
    default_key = "AIzaSyA9jG3pYtC81tbmS7Jbqt0k3nyjm5f2ang"
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    st.markdown("[Get a new API Key here](https://aistudio.google.com/app/apikey)")
    
    model_id = "gemini-3-flash-preview"
    
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            st.success("API Connected!")
        except Exception as e:
            st.error(f"Connection failed: {e}")

# --- DATA LOADING ---
uploaded_files = st.file_uploader("Upload Spreadsheets", type=['xlsx', 'csv'], accept_multiple_files=True)

if uploaded_files:
    dfs = {}
    context_info = ""
    for file in uploaded_files:
        try:
            df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
            dfs[file.name] = df
            context_info += f"File: {file.name}\nColumns: {list(df.columns)}\n\n"
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")

    st.success(f"✅ Loaded {len(dfs)} files.")
    
    user_query = st.text_area("What should the AI do with this data?")

    if st.button("🚀 Run Analysis"):
        if not api_key:
            st.warning("Please provide an API key.")
        elif user_query:
            prompt = f"Dataframes: {context_info}\nTask: {user_query}\nReturn ONLY Python code using st.write() or st.plotly_chart()."
            try:
                with st.spinner("AI analyzing..."):
                    response = client.models.generate_content(model=model_id, contents=prompt)
                    raw_code = response.text.replace('```python', '').replace('```', '').strip()
                
                # Executing the AI generated code
                exec(raw_code, {'dfs': dfs, 'pd': pd, 'st': st, 'io': io, 'px': None})
            except Exception as e:
                st.error(f"Analysis Error: {e}")
