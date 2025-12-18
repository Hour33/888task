from flask import Flask, request, render_template, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

ALERT_EMAIL = os.environ.get("ALERT_EMAIL")
EMAIL_PASS = os.environ.get("ALERT_EMAIL_APP_PASS")

@app.route("/")
def home():
    return "Server running"

@app.route("/safety")
def safety():
    return render_template("safety.html")

@app.route("/alert", methods=["POST"])
def alert():
    data = request.json

    msg = EmailMessage()
    msg["Subject"] = "⚠️ Possible Scam Form Detected"
    msg["From"] = ALERT_EMAIL
    msg["To"] = "leewandee11@gmail.com"
    msg.set_content(f"""
Site: {data.get('site')}
Time: {data.get('time')}
Preview: {data.get('preview')}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(ALERT_EMAIL, EMAIL_PASS)
        smtp.send_message(msg)

    return jsonify({"status": "sent"})
