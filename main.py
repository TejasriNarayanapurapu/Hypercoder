import streamlit as st
from config import get_openai_key, get_github_token
from github_reader import get_github_issue
import openai

st.title("🔐 HyperCoder Access")

openai_key = get_openai_key()
github_token = get_github_token()

st.write("OpenAI API Key loaded:", "✅" if openai_key else "❌")
st.write("GitHub Token loaded:", "✅" if github_token else "❌")

import openai

def summarize_issue(title, body, openai_key):
    openai.api_key = openai_key
    prompt = f"Summarize the following GitHub issue:\n\nTitle: {title}\n\nBody: {body}"
    
    response = openai.chat.completions.create(
        model= "gpt-3.5-turbo" 
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


owner = st.text_input("Enter GitHub owner (e.g., openai)")
repo = st.text_input("Enter repo (e.g., gpt-4)")
issue_num = st.number_input("Enter issue number", min_value=1, step=1)

if st.button("Fetch Issue"):
    issue = get_github_issue(owner, repo, issue_num, github_token)
    if "error" in issue:
        st.error(issue["error"])
        st.write(issue.get("details", ""))
    else:
        st.subheader("GitHub Issue")
        st.write(f"**Title:** {issue.get('title', 'No title')}")
        st.write(f"**Body:** {issue.get('body', '')}")

        if openai_key:
            st.subheader("AI Summary")
            summary = summarize_issue(issue.get('title', ''), issue.get('body', ''), openai_key)
            st.write(summary)
        else:
            st.info("OpenAI API key not loaded. Cannot generate summary.")



st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)
