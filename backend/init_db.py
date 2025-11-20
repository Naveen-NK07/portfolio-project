from db_config import get_connection

conn = get_connection()
cur = conn.cursor()

# personal_info
cur.execute("""
CREATE TABLE IF NOT EXISTS personal_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    headline TEXT
);
""")

# education
cur.execute("""
CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    institution TEXT,
    degree TEXT,
    start_year TEXT,
    end_year TEXT,
    grade TEXT
);
""")

# skills
cur.execute("""
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    skill_name TEXT,
    proficiency TEXT
);
""")

# certificates
cur.execute("""
CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    certificate_name TEXT,
    issuer TEXT,
    issue_year TEXT
);
""")

# reviews
cur.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    name TEXT,
    email TEXT,
    message TEXT,
    rating INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);
""")

# Insert personal info if empty
cur.execute("SELECT COUNT(*) as c FROM personal_info")
if cur.fetchone()["c"] == 0:
    cur.execute("""
    INSERT INTO personal_info (full_name, email, phone, headline)
    VALUES (?, ?, ?, ?)
    """, ("Naveen Kumar P", "naveenparthipan07@gmail.com", "9514713372",
          "Aspiring Software Developer"))

# Insert education
cur.execute("SELECT COUNT(*) as c FROM education")
if cur.fetchone()["c"] == 0:
    cur.executemany("""
    INSERT INTO education (profile_id, institution, degree, start_year, end_year, grade)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, "Dhanalakshmi College Of Engineering", "B.E CSE", "2021", "2025", "8.06"),
        (1, "Sri Vishwa Vidyalaya Matric Hr Sec School", "HSC (12th)", "2020", "2021", "81%"),
        (1, "Sri Vishwa Vidyalaya Matric Hr Sec School", "SSLC (10th)", "2018", "2019", "76%")
    ])

# Insert skills
cur.execute("SELECT COUNT(*) as c FROM skills")
if cur.fetchone()["c"] == 0:
    cur.executemany("""
    INSERT INTO skills (profile_id, skill_name, proficiency)
    VALUES (?, ?, ?)
    """, [
        (1, "Java", "Intermediate"),
        (1, "Python", "Intermediate"),
        (1, "HTML", "Intermediate"),
        (1, "CSS", "Intermediate"),
        (1, "JavaScript", "Beginner"),
        (1, "Excel", "Intermediate"),
        (1, "PowerPoint", "Intermediate"),
        (1, "Word", "Intermediate")
    ])

# Insert certificates
cur.execute("SELECT COUNT(*) as c FROM certificates")
if cur.fetchone()["c"] == 0:
    cur.executemany("""
    INSERT INTO certificates (profile_id, certificate_name, issuer, issue_year)
    VALUES (?, ?, ?, ?)
    """, [
        (1, "AWS Cloud Foundations", "AWS Academy", "2023"),
        (1, "TCS ION Young Professional", "TCS", "2023"),
        (1, "Human Resources Skills Workshop", "HR Dept", "2023")
    ])

conn.commit()
conn.close()

print("Database initialized with full data!")
