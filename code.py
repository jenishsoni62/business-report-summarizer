import streamlit as st
from groq import Groq
import fitz
import os
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def summarize_report(text):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""You are a business analyst. Analyze this business report and provide:
1. Executive Summary
2. Key Financial Highlights
3. Important Business Insights
4. Risks and Challenges
5. Overall Assessment

Report:
{text[:5000]}"""
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

st.title("📊 Business Report Summarizer")
st.subheader("Upload a business or financial report to get AI-powered insights")

uploaded_file = st.file_uploader("Upload PDF Report", type="pdf")

if uploaded_file is not None:
    with st.spinner("Reading and analyzing report..."):
        text = extract_text_from_pdf(uploaded_file)
        summary = summarize_report(text)

    st.success("Analysis Complete!")
    st.markdown(summary)
