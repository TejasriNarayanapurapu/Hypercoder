import streamlit as st
from openai import OpenAI
from github_reader import get_github_issue

# Hardcoded OpenAI key for testing — replace with your friend's actual key here
# WARNING: Do NOT commit or share this key publicly
openai_key = "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"

client = OpenAI(api_key=openai_key)


st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 HyperCoder</h1>", unsafe_allow_html=True)

# Debug print to confirm which key is loaded (show only prefix for safety)
st.write("Using OpenAI key prefix:", openai_key[:6] + "…")

# Initialize OpenAI client with the key
client = OpenAI(api_key=openai_key)

# Summarization function using OpenAI SDK
def summarize_issue(title, body):
    prompt = f"Summarize the following GitHub issue:\n\nTitle: {title}\n\nBody: {body}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        err_msg = str(e)
        if "insufficient_quota" in err_msg or "429" in err_msg:
            return "⚠️ API quota exceeded. Please check your OpenAI billing and quota."
        return f"Error summarizing issue: {err_msg}"

# Sidebar inputs for GitHub repo and issue
with st.sidebar:
    st.header("🛠️ Repo Configuration")
    owner = st.text_input("GitHub Repo Owner", value="octocat")
    repo = st.text_input("GitHub Repo Name", value="Hello-World")
    issue_number = st.number_input("Issue Number", min_value=1, value=1)

    # You can add GitHub token input here if needed
    # github_token = st.text_input("GitHub Token", type="password")

# Main action
if st.button("Fetch and Summarize Issue"):
    # Call your function to fetch GitHub issue (ensure this works)
    github_token = ""  # Or load from config/environment if needed
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
