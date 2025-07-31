import streamlit as st
from github_reader import get_github_issue

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

st.set_page_config(page_title="HyperCoder - Local Summarizer", layout="centered")
st.title("🤖 HyperCoder - Local Summarization (No API Needed)")

def summarize_text(text, num_sentences=3):
    if not text.strip():
        return "No content to summarize."
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

with st.sidebar:
    st.header("GitHub Issue Config")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)
    github_token = st.text_input("GitHub Token (optional)", type="password")

if st.button("Fetch Issue & Summarize"):
    with st.spinner("Fetching issue from GitHub..."):
        issue = get_github_issue(owner, repo, issue_number, github_token.strip())

    if not issue:
        st.error("❌ Issue not found or failed to fetch.")
    elif "error" in issue:
        st.error(f"❌ GitHub API Error: {issue['error']}")
        if "details" in issue:
            st.text(issue["details"])
    else:
        st.subheader("📄 GitHub Issue")
        st.markdown(f"**Title:** {issue.get('title', 'No title')}")
        body = issue.get("body", "")
        st.markdown(f"**Body (first 1000 chars):**\n\n{body[:1000]}{'...' if len(body) > 1000 else ''}")

        st.subheader("🧠 Local Summary")
        summary = summarize_text(body, num_sentences=4)
        st.write(summary)

st.markdown("""
---
<p style='text-align:center; color:gray; font-size:12px;'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)
