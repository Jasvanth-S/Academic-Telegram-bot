from openai import OpenAI
from config import HF_TOKEN

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

def generate_ai_reply(user_input: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a smart academic assistant. Answer briefly."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ AI Error: {e}"
