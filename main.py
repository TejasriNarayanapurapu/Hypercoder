import streamlit as st
import requests
from github_reader import get_github_issue  # Make sure this is implemented properly

# Hugging Face Token (Make sure this is a summarization-capable model token)
hf_token = "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"  # Replace with your token

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤗 HuggingFace-Powered HyperCoder</h1>", unsafe_allow_html=True)
st.write("🔑 HuggingFace Key Prefix:", hf_token[:10] + "…")

# Hugging Face summarization function
def summarize_issue(title, body):
    input_text = f"Title: {title}\n\nBody: {body}"
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"❌ HuggingFace Error: {response.status_code} - {response.json()}"
    
    try:
        summary = response.json()[0]["summary_text"]
        return summary
    except Exception as e:
        return f"❌ Parsing Error: {e} | Raw: {response.json()}"

# Sidebar
with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

# Main Action
if st.button("Fetch and Summarize Issue"):
    github_token = ""  # Optional: You can add a token if needed
    issue = get_github_issue(owner, repo, issue_number, github_token)

    if issue and isinstance(issue, dict) and 'title' in issue and 'body' in issue:
        st.subheader("🔍 GitHub Issue Content")
        st.write(f"**Title:** {issue['title']}")
        st.write(f"**Body:** {issue['body'][:1000]}...")

        st.subheader("🧠 AI Summary")
        summary = summarize_issue(issue['title'], issue['body'])
        st.success(summary)
    else:
        st.error("❌ Issue not found or invalid structure returned.")
        st.json(issue)  # Debug output

# Footer
st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)

