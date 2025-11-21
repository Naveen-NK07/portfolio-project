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
        1,
        name,
        email,
        message,
        rating,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

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
