from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import mysql.connector

app = FastAPI()

# DB connection function
def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="2005",   # your MySQL password
        database="testdb"  # your schema name
    )

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# ---------------- LOGIN ----------------
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        return RedirectResponse(url="/#welcome", status_code=302)
    else:
        return HTMLResponse(
            "<h2 style='color:red;text-align:center;'>❌ Invalid username or password</h2>"
        )

# ---------------- IDEA SUBMISSION ----------------
@app.post("/submit_idea")
def submit_idea(name: str = Form(...), roll_number: str = Form(...), idea: str = Form(...)):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO hackathon_ideas (name, roll_number, idea) VALUES (%s, %s, %s)",
        (name, roll_number, idea)
    )
    db.commit()
    cursor.close()
    db.close()

    return HTMLResponse("""
    <html>
    <body style="background:black; color:white; text-align:center; font-family:Arial;">
      <h1>✅ Thank you for submitting your idea!</h1>
      <h2>Your idea is stored in database 🎉</h2>
      <p><a href="/" style="color:yellow;">Back to Home</a></p>
    </body>
    </html>
    """)
