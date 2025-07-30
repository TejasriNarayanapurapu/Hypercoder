import streamlit as st
from github_reader import get_github_issue
from transformers import pipeline

# Load summarization pipeline from Hugging Face
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

st.set_page_config(page_title="HyperCoder 🔧", layout="wide")
st.markdown("<h1 style='text-align: center;'>🚀 HyperCoder: GitHub Issue Summarizer</h1>", unsafe_allow_html=True)

# GitHub Issue Input Form
with st.form("issue_form"):
    owner = st.text_input("GitHub Repo Owner", value="openai")
    repo = st.text_input("Repository Name", value="openai-python")
    issue_number = st.text_input("Issue Number", value="1")
    submitted = st.form_submit_button("🔍 Fetch & Summarize")

if submitted:
    st.info("Fetching issue details...")
    issue = get_github_issue(owner, repo, issue_number)

    if issue:
        title = issue.get("title", "")
        body = issue.get("body", "")

        st.subheader("📌 Issue Title:")
        st.write(title)

        st.subheader("📝 Issue Body:")
        st.code(body, language="markdown")

        # Summarize the issue body
        if body.strip():
            st.subheader("🧠 AI Summary:")
            try:
                summary = summarizer(body, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
                st.success(summary)
            except Exception as e:
                st.error(f"Failed to summarize: {str(e)}")
        else:
            st.warning("No content to summarize in the issue body.")
    else:
        st.error("❌ Could not fetch issue. Check details or GitHub rate limits.")


st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)
