import streamlit as st
from config import get_openai_key, get_github_token
from github_reader import get_github_issue, get_readme

st.title("🔐 HyperCoder Access")

openai_key = get_openai_key()
github_token = get_github_token()

st.write("OpenAI API Key loaded:", "✅" if openai_key else "❌")
st.write("GitHub Token loaded:", "✅" if github_token else "❌")

# Example usage (you should replace with real logic)
st.write("This is a demo app. Replace with your HyperCoder logic.")

# For demo: show a dummy GitHub issue fetch (stub)
issue = get_github_issue("owner", "repo", 1, github_token)
st.write("Sample GitHub issue data:", issue)
