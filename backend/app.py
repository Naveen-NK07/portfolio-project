from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
from datetime import datetime
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ------------------------- PERSONAL INFO -------------------------
@app.route("/api/personal-info", methods=["GET"])
def personal_info():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM personal_info WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    return jsonify(dict(row) if row else {})

# ------------------------- EDUCATION -------------------------
@app.route("/api/education", methods=["GET"])
def get_education():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM education WHERE profile_id = 1")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ------------------------- SKILLS -------------------------
@app.route("/api/skills", methods=["GET"])
def get_skills():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM skills WHERE profile_id = 1")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ------------------------- CERTIFICATES -------------------------
@app.route("/api/certificates", methods=["GET"])
def get_certificates():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM certificates WHERE profile_id = 1")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ------------------------- ADD REVIEW -------------------------
@app.route("/api/review", methods=["POST"])
def add_review():
    data = request.get_json()

    name = data.get("name", "")
    email = data.get("email", "")
    rating = data.get("rating", "")
    message = data.get("message", data.get("comment", ""))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reviews (profile_id, name, email, message, rating, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        1,
        name,
        email,
        message,
        rating,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

    send_email(data)
    return jsonify({"success": True})

# ------------------------- GET REVIEWS -------------------------
@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ------------------------- EMAIL FUNCTION -------------------------
def send_email(data):
    try:
        EMAIL = os.getenv("EMAIL_USER")
        PASS = os.getenv("EMAIL_PASS")

        if not EMAIL or not PASS:
            print("❌ Missing email credentials in .env")
            return

        user_message = data.get("message", data.get("comment", ""))

        msg = EmailMessage()
        msg["Subject"] = f"New Review from {data['name']}"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        msg.set_content(f"""
You received a new review:

Name: {data['name']}
Email: {data['email']}
Rating: {data['rating']}
Message:
{user_message}
""")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASS)
            server.send_message(msg)

        print("📩 Email sent successfully!")

    except Exception as e:
        print("❌ Email sending failed:", e)

# ------------------------- HOME -------------------------
@app.route("/", methods=["GET"])
def home():
    return "SQLite Backend Running!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
