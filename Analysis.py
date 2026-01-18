import subprocess
import sys
import os

# --- 1. BOOTSTRAP: AUTO-INSTALLER ---
def install_dependencies():
    packages = ["streamlit", "pandas", "google-genai", "openpyxl", "plotly", "xlsxwriter"]
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

# --- 2. IMPORTS ---
import streamlit as st
import pandas as pd
from google import genai
import io

# --- 3. PAGE CONFIG & UI ---
st.set_page_config(page_title="AI Sales Analyst", layout="wide")
st.title("📊 Multi-Excel AI Sales Analyst")

with st.sidebar:
    st.header("Setup")
    
    # Pre-filled API Key as requested
    default_key = "AIzaSyA9jG3pYtC81tbmS7Jbqt0k3nyjm5f2ang"
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    
    # Direct link to get a key
    st.markdown("[Get a new API Key here](https://aistudio.google.com/app/apikey)")
    
    st.divider()
    st.info("The system automatically manages libraries like xlsxwriter.")

# --- 4. DATA LOADING ---
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
    
    # --- 5. AI INTERFACE ---
    user_query = st.text_area("What should the AI do with this data?")

    if st.button("🚀 Run Analysis"):
        if not api_key:
            st.warning("Please provide an API key.")
        elif user_query:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are a Data Analyst. Dataframes: {context_info}
            Access via dictionary 'dfs'. Task: {user_query}
            Return ONLY Python code using st.write() or st.plotly_chart().
            """
            try:
                with st.spinner("AI analyzing..."):
                    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                    raw_code = response.text.replace('```python', '').replace('```', '').strip()
                
                exec_globals = {'dfs': dfs, 'pd': pd, 'st': st, 'io': io}
                exec(raw_code, exec_globals)
                
            except Exception as e:
                st.error(f"Execution Error: {e}")