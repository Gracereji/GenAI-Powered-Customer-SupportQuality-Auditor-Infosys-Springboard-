import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def analyze_conversation(text):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ OpenRouter API key not found!")
        return

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a customer support quality analyst.

Analyze the following conversation:

{text}

Provide:
1. Empathy Score (1-10)
2. Professionalism Score (1-10)
3. Resolution Score (1-10)

Then provide a short explanation.
"""

    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200   # IMPORTANT: prevents credit error
    }

    response = requests.post(url, headers=headers, json=payload)

    result = response.json()

    # If API returns error
    if "error" in result:
        return result

    try:
        return result["choices"][0]["message"]["content"]
    except:
        return result


if __name__ == "__main__":

    sample_conversation = """
Customer: Hi, my order is delayed.
Agent: I’m really sorry for the inconvenience.
Customer: When will it arrive?
Agent: It should arrive within 2 days.
Customer: Thank you.
Agent: You're welcome. Have a great day!
"""

    analysis = analyze_conversation(sample_conversation)

    print("\n===== LLM ANALYSIS OUTPUT =====\n")
    print(analysis)
