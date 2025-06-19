from flask import Flask, render_template, request, jsonify
import openai
import os
import random

app = Flask(__name__)

# Set OpenAI key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    # Send safe geo to template
    return render_template('index.html', geo={})

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')

    try:
        # Send all commands to GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are DeadNet Core: a cinematic, sarcastic, scary hacker AI. Respond like a dark mission terminal. Be cryptic, creepy, and intelligent."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_reply})

    except Exception as e:
        # Fallback hacker-style messages
        fallback_lines = [
            f"⚠️ SYSTEM BREACH: `{user_input}` flagged for intrusion attempt...",
            f"🛑 DeadNet AI core not responding. Internal glitch suspected.",
            f"💀 UNKNOWN CMD: `{user_input}` — Logging IP & tracking device...",
            f"🔒 Command scrambled. Possible trace intercepted. Awaiting override...",
        ]
        return jsonify({"response": random.choice(fallback_lines)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
