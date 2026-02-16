import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load API keys
load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Customer Support QA System", layout="centered")

st.title("🎧 AI Customer Support Call Intelligence System")
st.write("Upload a customer support call audio file to analyze quality and summary.")

uploaded_file = st.file_uploader("Upload Audio File (.m4a)", type=["m4a"])

if uploaded_file:

    st.info("🔄 Transcribing audio using Deepgram...")

    # Deepgram API
    dg_url = "https://api.deepgram.com/v1/listen"
    dg_headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/m4a"
    }

    dg_response = requests.post(dg_url, headers=dg_headers, data=uploaded_file)

    if dg_response.status_code != 200:
        st.error("Deepgram transcription failed.")
        st.stop()

    dg_result = dg_response.json()

    transcript = dg_result["results"]["channels"][0]["alternatives"][0]["transcript"]

    st.subheader("📝 Transcript")
    st.write(transcript)

    st.info("🤖 Analyzing conversation with AI...")

    # LLM Prompt
    prompt = f"""
You are an AI Customer Support Quality Analyst.

Analyze the following conversation:

{transcript}

Provide:

1. Short Summary (3-4 lines)
2. Main Customer Issue
3. Final Resolution Given
4. Overall Sentiment (Positive / Neutral / Negative)
5. Empathy Score (1-10)
6. Professionalism Score (1-10)
7. Resolution Effectiveness Score (1-10)

Give clear structured output.
"""

    or_url = "https://openrouter.ai/api/v1/chat/completions"

    or_headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }

    or_response = requests.post(or_url, headers=or_headers, json=payload)

    if or_response.status_code != 200:
        st.error("LLM analysis failed.")
        st.stop()

    analysis = or_response.json()["choices"][0]["message"]["content"]

    st.subheader("📊 AI Analysis Report")
    st.write(analysis)

    st.success("✅ Analysis Completed Successfully!")
