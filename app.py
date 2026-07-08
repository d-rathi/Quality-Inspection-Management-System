from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "qims_secret_key"


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTRATION ----------------

@app.route("/registration")
def registration():
    return render_template("registration.html")


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        if password != confirmPassword:
            return "Passwords do not match"

        conn = sqlite3.connect("qims.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users(fullname, email, username, password)
                VALUES (?, ?, ?, ?)
                """,
                (fullname, email, username, password)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("qims.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# ---------------- USERS ----------------

@app.route("/users")
def users():

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    conn.close()

    return str(data)


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
 
# ---------------- INSPECTION ----------------

@app.route("/inspection")
def inspection():
    return render_template("inspection.html") 

# ---------------- RECORDS ----------------

@app.route("/records")
def records():
    return "<h2>Inspection Records Page</h2>"


# ---------------- REPORT ----------------

@app.route("/report")
def report():
    return "<h2>Reports Page</h2>"


# ---------------- DEFECT LIBRARY ----------------

@app.route("/defects")
def defects():
    return "<h2>Defect Library Page</h2>"


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    return redirect(url_for("login"))
                    
# ---------------- MAIN ----------------

init_db()

if __name__ == "__main__":
    app.run(debug=True)