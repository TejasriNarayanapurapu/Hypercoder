import streamlit as st
import requests
from github_reader import get_github_issue

# Load tokens from Streamlit secrets if available; else empty string
HF_TOKEN = st.secrets["HF_TOKEN"] if "HF_TOKEN" in st.secrets else ""
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤗 HuggingFace-Powered HyperCoder</h1>", unsafe_allow_html=True)
st.write("🔑 HuggingFace Key Prefix:", (HF_TOKEN[:10] + "…") if HF_TOKEN else "No token loaded")

def summarize_issue(title, body):
    input_text = f"Title: {title}\n\nBody: {body}"
    API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return f"❌ HuggingFace Error: {response.status_code} - {response.json()}"
    try:
        summary = response.json()[0]["summary_text"]
        return summary
    except Exception as e:
        return f"❌ Parsing Error: {e} | Raw Response: {response.json()}"

with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

if st.button("Fetch and Summarize Issue"):
    issue = get_github_issue(owner, repo, issue_number, GITHUB_TOKEN)
    if issue and isinstance(issue, dict) and 'title' in issue and 'body' in issue:
        st.subheader("🔍 GitHub Issue Content")
        st.write(f"**Title:** {issue['title']}")
        st.write(f"**Body:** {issue['body'][:1000]}...")

        st.subheader("🧠 AI Summary")

        # If body is too short, skip summarization or give fallback
        if len(issue['body'].strip()) < 20:
            summary = "Issue body is very short; not enough content to summarize."
        else:
            summary = summarize_issue(issue['title'], issue['body'])

        st.success(summary)
    else:
        st.error("❌ Issue not found or invalid data")
        st.json(issue)


st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)
