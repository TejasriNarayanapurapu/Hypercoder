import streamlit as st
from openai import OpenAI
from config import get_openai_key, get_github_token
from github_reader import get_github_issue

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 HyperCoder</h1>", unsafe_allow_html=True)

# Load API keys
openai_key = get_openai_key()
github_token = get_github_token()

st.write("OpenAI API Key loaded:", "✅" if openai_key else "❌")
st.write("GitHub Token loaded:", "✅" if github_token else "❌")

# Initialize OpenAI client with the new interface
client = OpenAI(api_key=openai_key)

# Summarization function using new OpenAI SDK
def summarize_issue(title, body):
    # Simple mock summary for testing without API calls
    return f"Mock summary: Issue titled '{title}' with body length {len(body)} characters."

# Sidebar inputs
with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

# Main action
if st.button("Fetch and Summarize Issue"):
    issue = get_github_issue(owner, repo, issue_number, github_token)

    if issue:
        st.subheader("🔍 GitHub Issue Content")
        st.write(f"**Title:** {issue['title']}")
        st.write(f"**Body:** {issue['body'][:1000]}...")

        st.subheader("🧠 AI Summary")
        summary = summarize_issue(issue['title'], issue['body'])
        st.success(summary)
    else:
        st.error("❌ Issue not found or an error occurred.")

# Footer
st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)

