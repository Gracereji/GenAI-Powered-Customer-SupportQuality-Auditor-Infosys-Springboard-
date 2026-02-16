import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()

def transcribe_audio(audio_path):
    api_key = os.getenv("DEEPGRAM_API_KEY")

    if not api_key:
        print("❌ Deepgram API key not found!")
        return

    url = "https://api.deepgram.com/v1/listen"

    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/m4a"
    }

    with open(audio_path, "rb") as audio:
        response = requests.post(url, headers=headers, data=audio)

    result = response.json()

    transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]

    return transcript


if __name__ == "__main__":
    result = transcribe_audio("sample_data/audio/sample_call.m4a")

    print("\n===== TRANSCRIPT OUTPUT =====\n")
    print(result)
