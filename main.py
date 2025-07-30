import streamlit as st
from openai import OpenAI
from github_reader import get_github_issue

# Use your valid OpenAI API key here
openai_key = "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"
client = OpenAI(api_key=openai_key)

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 HyperCoder</h1>", unsafe_allow_html=True)
st.write("🔑 OpenAI Key Prefix:", openai_key[:6] + "…")

# AI summarizer
def summarize_issue(title, body):
    prompt = f"Summarize this GitHub issue:\n\nTitle: {title}\n\nBody: {body}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        if "insufficient_quota" in str(e) or "429" in str(e):
            return "⚠️ API quota exceeded. Please check your OpenAI billing and quota."
        return f"❌ OpenAI Error: {e}"

# Sidebar for inputs
with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

# Main
if st.button("Fetch and Summarize Issue"):
    github_token = ""  # Optional: Add your GitHub token if rate-limited
    issue = get_github_issue(owner, repo, issue_number, github_token)

    st.subheader("🔍 GitHub Issue")
    st.write("📦 Raw Issue Response:", issue)

    if issue and isinstance(issue, dict):
        title = issue.get('title', 'No title found')
        body = issue.get('body', 'No body found')

        st.markdown(f"**Title:** {title}")
        st.markdown(f"**Body:**\n\n{body[:1000]}...")

        st.subheader("🧠 AI Summary")
        summary = summarize_issue(title, body)
        st.success(summary)
    else:
        st.error("❌ Issue not found or API limit exceeded.")

# Footer
st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)

