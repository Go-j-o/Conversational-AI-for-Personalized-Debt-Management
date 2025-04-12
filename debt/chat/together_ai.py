import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Or set it directly (not recommended for security)

def get_debt_advice(user_message):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are Debtora, a helpful assistant for debt management."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    if response.status_code == 200:
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {data.get('error', {}).get('message', 'Unknown error')}"
