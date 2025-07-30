import streamlit as st
from config import get_openai_key, get_github_token
from github_reader import get_github_issue

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 HyperCoder</h1>", unsafe_allow_html=True)

openai_key = get_openai_key()
github_token = get_github_token()

st.write("OpenAI API Key loaded:", "✅" if openai_key else "❌")
st.write("GitHub Token loaded:", "✅" if github_token else "❌")

# Example usage (you should replace with real logic)
import openai

def summarize_issue(title, body, openai_key):
    openai.api_key = openai_key
    prompt = f"Summarize the following GitHub issue:\n\nTitle: {title}\n\nBody: {body}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# For demo: show a dummy GitHub issue fetch (stub)
with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

if st.button("Fetch Issue"):
    issue = get_github_issue(owner, repo, issue_num, github_token)
    st.json(issue)
    
st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)

