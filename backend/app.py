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
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ------------------------------------
# PERSONAL INFO
# ------------------------------------
@app.route("/api/personal-info", methods=["GET"])
def get_personal_info():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT full_name, email, phone, headline FROM personal_info WHERE id = 1")
    row = cur.fetchone()

    cur.close()
    conn.close()
    return jsonify(row)


# ------------------------------------
# EDUCATION
# ------------------------------------
@app.route("/api/education", methods=["GET"])
def get_education():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM education WHERE profile_id = 1 ORDER BY start_year DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(rows)


# ------------------------------------
# SKILLS
# ------------------------------------
@app.route("/api/skills", methods=["GET"])
def get_skills():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM skills WHERE profile_id = 1 ORDER BY id ASC")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(rows)


# ------------------------------------
# CERTIFICATES
# ------------------------------------
@app.route("/api/certificates", methods=["GET"])
def get_certificates():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM certificates WHERE profile_id = 1 ORDER BY id ASC")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(rows)


# ------------------------------------
# ADD REVIEW  (UPDATED WITH profile_id + created_at)
# ------------------------------------
@app.route("/api/reviews", methods=["POST"])
def add_review():
    try:
        data = request.get_json()

        name = data.get("name", "")
        email = data.get("email", "")
        rating = int(data.get("rating", 0))
        message = data.get("message") or data.get("comment") or ""

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            """
            INSERT INTO reviews (profile_id, name, email, message, rating, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (1, name, email, message, rating, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        conn.commit()
        cur.close()
        conn.close()

        # try sending email
        try:
            send_email(data)
        except Exception as e:
            print("Email error but review saved:", e)

        return jsonify({"success": True})

    except Exception as e:
        print("Backend Error:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# ------------------------------------
# GET REVIEWS
# ------------------------------------
@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM reviews WHERE profile_id = 1 ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(rows)


# ------------------------------------
# EMAIL FUNCTION (unchanged)
# ------------------------------------
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

    except Exception as e:
        print("Email error:", e)


@app.route("/", methods=["GET"])
def home():
    return "Backend Running!"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
