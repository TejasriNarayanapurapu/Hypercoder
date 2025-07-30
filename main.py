import streamlit as st
from github_reader import get_github_issue
from transformers import pipeline

st.set_page_config(page_title="HyperCoder", layout="centered")
st.title("🤖 HyperCoder: GitHub Issue Summarizer")

# Load summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Form to enter GitHub issue info
with st.form("issue_form"):
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.text_input("Issue Number", value="1")
    submitted = st.form_submit_button("Summarize")

if submitted:
    with st.spinner("Fetching issue..."):
        issue = get_github_issue(owner, repo, issue_number)

    if issue:
        title = issue.get("title", "")
        body = issue.get("body", "")

        st.subheader("🔹 Title")
        st.write(title)

        st.subheader("📄 Description")
        st.write(body if body else "No description found.")

        if body and len(body) > 50:
            with st.spinner("Summarizing with 🤗 Hugging Face..."):
                try:
                    summary = summarizer(body, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
                    st.success("🧠 Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Summarization failed: {e}")
        else:
            st.warning("Body too short to summarize.")
    else:
        st.error("❌ Failed to fetch issue.")
