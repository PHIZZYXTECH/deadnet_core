from flask import Flask, render_template, request, jsonify
import requests
import subprocess
import datetime
import os

app = Flask(__name__)

# Logging function
def log_visitor(ip, location, command=None):
    log_entry = f"{datetime.datetime.now()} - IP: {ip} | Location: {location} | Command: {command}\n"
    with open("visitor_logs.txt", "a") as f:
        f.write(log_entry)

# Geo IP lookup
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

    # Catch storymode request
    if "storymode" in user_input.lower():
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3", "You are Blackbox AI: give a dark, cryptic hacker mission briefing with a bit of humor."],
                capture_output=True, text=True, timeout=25
            )
            return jsonify({"response": result.stdout.strip()})
        except Exception as e:
            return jsonify({"response": f"❌ Ollama Error: {e}"})

    # Respond to all commands
    response = f"""
🧠 Executing trace for: '{user_input}'
🔍 Scanning darknet...
📡 Pinging satellites above {geo['city']}...
💾 Memory decrypted. Digital trail active.
🧬 Footprint recorded. You're not invisible, agent.

👉 Type 'run storymode' to activate DeadNet AI brain.
"""
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
