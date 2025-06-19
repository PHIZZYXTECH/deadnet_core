from flask import Flask, render_template, request, jsonify
import requests
import subprocess
import datetime
import os
import openai
import shutil

app = Flask(__name__)

# Set up OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Log visitor info
def log_visitor(ip, location, command=None):
    log = f"{datetime.datetime.now()} - IP: {ip} | Location: {location} | Command: {command}\n"
    with open("visitor_logs.txt", "a") as f:
        f.write(log)

# Get visitor IP + Geo info
def get_geo():
    try:
        res = requests.get("https://ipapi.co/json/").json()
        return {
            "ip": res.get("ip", "Unknown"),
            "city": res.get("city", "Unknown"),
            "region": res.get("region", ""),
            "country": res.get("country_name", ""),
            "lat": res.get("latitude", "0"),
            "lon": res.get("longitude", "0")
        }
    except:
        return {
            "ip": "Unknown",
            "city": "Unknown",
            "region": "",
            "country": "",
            "lat": "0",
            "lon": "0"
        }

@app.route("/")
def index():
    geo = get_geo()
    log_visitor(geo['ip'], f"{geo['city']}, {geo['country']}")
    return render_template("index.html", geo=geo)

@app.route("/command", methods=["POST"])
def command():
    user_input = request.json.get("command")
    geo = get_geo()
    log_visitor(geo['ip'], f"{geo['city']}, {geo['country']}", user_input)

    if "storymode" in user_input.lower():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are DeadNet Core AI: respond like a dark, cryptic hacker overlord. Give cinematic, slightly funny, mission-style responses with cyberpunk flair."},
                    {"role": "user", "content": "Engage storymode."}
                ]
            )
            return jsonify({"response": response["choices"][0]["message"]["content"]})
        except Exception as e:
            return jsonify({"response": f"⚠️ OpenAI Error: {str(e)}"})

    # Generic simulated hacker response
    response = f"""
🧠 Terminal > '{user_input}'
⚙️ Executing dark protocol...
📍 Location trace: {geo['city']}, {geo['country']} ({geo['ip']})
🛰️ Signal rerouted via encrypted satellite node.
🔓 Digital fingerprint stored and archived.

⚡ Hint: Type 'run storymode' to access the AI core.
"""
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
