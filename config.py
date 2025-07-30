import streamlit as st

def get_openai_key():
    return st.secrets.get("OPENAI_API_KEY", "")

def get_github_token():
    return st.secrets.get("GITHUB_TOKEN", "")
