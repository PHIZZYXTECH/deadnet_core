from flask import Flask, render_template, request, jsonify
import openai
import os
import random

app = Flask(__name__)

# Set your OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')

    try:
        # AI responds to every command
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are DeadNet Core: a scary, cinematic hacker AI with a sarcastic edge. Respond to all input with mystery, dark energy, and hacker-like warnings or briefings. Be creepy but intelligent."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_reply})

    except Exception as e:
        # If API fails, fallback fake hacker simulation
        fake_responses = [
            f"⚠️ ERROR: Interference detected in neural core while processing: `{user_input}`",
            f"💀 DeadNet Core intercepted illegal syscall attempt: `{user_input}`",
            f"🔐 Unauthorized syntax detected. All input now logged under NSA registry.",
            f"🧠 System lag. Attempting to decode terminal noise: `{user_input}`"
        ]
        return jsonify({"response": random.choice(fake_responses)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
