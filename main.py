import streamlit as st
from transformers import pipeline

# Set up HuggingFace summarizer (no API key needed for hosted model)
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def summarize_issue(title, body):
    prompt = f"Summarize the following GitHub issue:\n\nTitle: {title}\n\nBody: {body}"
    summary = summarizer(prompt, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>🤖 HyperCoder (Free Version)</h1>", unsafe_allow_html=True)

title = st.text_input("GitHub Issue Title", "Example: Bug in Login Function")
body = st.text_area("GitHub Issue Body", "Example: When clicking on login, the page crashes due to a null pointer...")

if st.button("Summarize Issue"):
    if title.strip() == "" and body.strip() == "":
        st.warning("Please enter a title or body to summarize.")
    else:
        summary = summarize_issue(title, body)
        st.success("📝 Summary:")
        st.write(summary)


st.markdown("""
<hr>
<p style='text-align: center; color: gray'>
Made with ❤️ by <b>Tejasri</b> · <a href='https://github.com/TejasriNarayanapurapu' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)
