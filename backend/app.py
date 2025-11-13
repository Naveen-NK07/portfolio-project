from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route("/api/review", methods=["POST"])
def add_review():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "INSERT INTO reviews (name, email, message, rating) VALUES (%s, %s, %s, %s)",
        (data["name"], data["email"], data["message"], data["rating"]),
    )
    conn.commit()
    cur.close()
    conn.close()
    send_email(data)
    return jsonify({"success": True})

@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM reviews ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

def send_email(data):
    try:
        EMAIL = os.getenv("EMAIL_USER")
        PASS = os.getenv("EMAIL_PASS")
        if not EMAIL or not PASS:
            return
        msg = EmailMessage()
        msg["Subject"] = f"New Review from {data['name']}"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg.set_content(f"""
Name: {data['name']}
Email: {data['email']}
Rating: {data['rating']}
Message:
{data['message']}
""")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASS)
            server.send_message(msg)
            print("Email sent")
    except Exception as e:
        print("Email error:", e)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
