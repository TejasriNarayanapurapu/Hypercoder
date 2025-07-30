import streamlit as st
from openai import OpenAI
from github_reader import get_github_issue

st.set_page_config(page_title="HyperCoder", page_icon="🤖")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 HyperCoder</h1>", unsafe_allow_html=True)

# Load API keys from Streamlit secrets or environment variables
openai_key = st.secrets.get("OPENAI_API_KEY", "")
github_token = st.secrets.get("GITHUB_TOKEN", "")

if not openai_key:
    st.error("OpenAI API key not found! Please add it to your Streamlit secrets as OPENAI_API_KEY.")
    st.stop()

if not github_token:
    st.warning("GitHub token not found. You can still fetch public issues but rate limits apply.")

client = OpenAI(api_key=openai_key)

def summarize_issue(title, body):
    prompt = f"Summarize the following GitHub issue:\n\nTitle: {title}\n\nBody: {body}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing issue: {e}"

with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

if st.button("Fetch and Summarize Issue"):
    issue = get_github_issue(owner, repo, issue_number, github_token)

    if issue and isinstance(issue, dict) and 'title' in issue and 'body' in issue:
        st.subheader("🔍 GitHub Issue Content")
        st.write(f"**Title:** {issue['title']}")
        st.write(f"**Body:** {issue['body'][:1000]}...")

        st.subheader("🧠 AI Summary")
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
