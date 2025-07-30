import streamlit as st
from github_reader import get_github_issue
from transformers import pipeline

st.set_page_config(page_title="HyperCoder", layout="centered")
st.title("🚀 HyperCoder: GitHub Issue Summarizer")

# Initialize summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

with st.form("fetch_form"):
    owner = st.text_input("🔹 GitHub Owner", value="openai")
    repo = st.text_input("📦 Repository Name", value="openai-python")
    issue_number = st.text_input("🐛 Issue Number", value="1")
    submit = st.form_submit_button("Fetch Issue and Summarize")

if submit:
    st.info("⏳ Fetching issue...")
    issue = get_github_issue(owner, repo, issue_number)

    if issue:
        title = issue.get("title", "No Title")
        body = issue.get("body", "No Description")

        st.subheader("📌 Issue Title")
        st.write(title)

        st.subheader("📝 Issue Description")
        st.write(body)

        if len(body.strip()) > 20:
            st.subheader("🧠 AI Summary")
            try:
                summary = summarizer(body, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
                st.success(summary)
            except Exception as e:
                st.error(f"Summarization failed: {str(e)}")
        else:
            st.warning("Issue body too short to summarize.")
    else:
        st.error("❌ Could not fetch issue. Check if repo/issue exists.")
