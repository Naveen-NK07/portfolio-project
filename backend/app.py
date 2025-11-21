from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- EMAIL FUNCTION ----------------
def send_email(name, email, rating, message):
    EMAIL = os.getenv("EMAIL_USER")
    PASS = os.getenv("EMAIL_PASS")

    if not EMAIL or not PASS:
        print("❌ Email credentials missing")
        return

    msg = EmailMessage()
    msg["Subject"] = f"New Review from {name}"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    msg.set_content(
        f"""
New Review Received:

Name: {name}
Email: {email}
Rating: {rating}

Message:
{message}
"""
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL, PASS)
            smtp.send_message(msg)
        print("📩 Email sent successfully!")
    except Exception as e:
        print("❌ Email sending failed:", e)


# ---------------- PERSONAL INFO ----------------
@app.route("/api/personal-info", methods=["GET"])
def get_personal_info():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT full_name, email, phone, headline FROM personal_info WHERE id = 1")
    row = cur.fetchone()

    conn.close()
    return jsonify(dict(row) if row else {})


# ---------------- EDUCATION ----------------
@app.route("/api/education", methods=["GET"])
def get_education():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM education WHERE profile_id = 1 ORDER BY start_year DESC")
    rows = cur.fetchall()

    conn.close()
    return jsonify([dict(r) for r in rows])


# ---------------- SKILLS ----------------
@app.route("/api/skills", methods=["GET"])
def get_skills():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM skills WHERE profile_id = 1")
    rows = cur.fetchall()

    conn.close()
    return jsonify([dict(r) for r in rows])


# ---------------- CERTIFICATES ----------------
@app.route("/api/certificates", methods=["GET"])
def get_certificates():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM certificates WHERE profile_id = 1")
    rows = cur.fetchall()

    conn.close()
    return jsonify([dict(r) for r in rows])


# ---------------- ADD REVIEW ----------------
@app.route("/api/reviews", methods=["POST"])
def add_review():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    rating = data.get("rating")
    message = data.get("message")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reviews (profile_id, name, email, message, rating, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        1, name, email, message, rating,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    # Send email (won't break API)
    try:
        send_email(name, email, rating, message)
    except:
        pass

    return jsonify({"success": True})


# ---------------- GET REVIEWS ----------------
@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reviews WHERE profile_id = 1 ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/")
def home():
    return "Backend Running Successfully!"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
