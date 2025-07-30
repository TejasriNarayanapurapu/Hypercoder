from huggingface_hub import InferenceClient
import streamlit as st
from github_reader import get_github_issue

hf_token = "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"

client = InferenceClient(token=hf_token)

def summarize_issue(title, body):
    input_text = f"Title: {title}\n\nBody: {body}"
    try:
        # This calls the public distilbart-cnn-12-6 summarization model
        output = client.text_summarization(inputs=input_text, model="sshleifer/distilbart-cnn-12-6")
        return output[0]['summary_text']
    except Exception as e:
        return f"Error from HuggingFace: {e}"

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤗 HuggingFace-Powered HyperCoder</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

if st.button("Fetch and Summarize Issue"):
    github_token = ""  # Add if you want GitHub auth
    issue = get_github_issue(owner, repo, issue_number, github_token)

    if issue and 'title' in issue and 'body' in issue:
        st.subheader("🔍 GitHub Issue Content")
        st.write(f"**Title:** {issue['title']}")
        st.write(f"**Body:** {issue['body'][:1000]}...")

        st.subheader("🧠 AI Summary")
        summary = summarize_issue(issue['title'], issue['body'])
        st.success(summary)
    else:
        st.error("❌ Issue not found or invalid data")

# Footer
st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)
