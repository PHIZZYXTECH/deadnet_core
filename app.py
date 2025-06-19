from flask import Flask, render_template, request, jsonify
import requests
import subprocess
import datetime
import os

app = Flask(__name__)

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
            result = subprocess.run(
                ["ollama", "run", "llama3", "You are DeadNet Core AI: respond with a dark, hacker-style mission briefing. Be mysterious, deep, but slightly funny."],
                capture_output=True,
                text=True,
                timeout=25
            )
            return jsonify({"response": result.stdout.strip()})
        except Exception as e:
            return jsonify({"response": f"❌ Ollama Error: {str(e)}"})

    # Generic response for all other commands
    response = f"""
🧠 Command received: '{user_input}'
🛰️ Initiating signal trace...
📡 Satellite lock acquired over {geo['city']}, {geo['country']}
💾 Decrypting terminal logs...
🔍 Shadow footprint embedded in darknet node.
🧬 Fingerprint stored. No anonymity here.

👉 Try 'run storymode' to engage BlackBox AI core.
"""
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
