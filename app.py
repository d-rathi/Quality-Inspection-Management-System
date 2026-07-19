from flask import Flask, render_template, request, redirect, url_for,session,request
import sqlite3
from datetime import datetime

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
           session["username"] = user[3]      # username
           session["fullname"] = user[1]      # full name

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

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    # Total Inspections
    cursor.execute("SELECT COUNT(*) FROM inspection")
    total = cursor.fetchone()[0]

    # Passed Tires
    cursor.execute("SELECT COUNT(*) FROM inspection WHERE inspection_status='Pass'")
    passed = cursor.fetchone()[0]

    # Failed Tires
    cursor.execute("SELECT COUNT(*) FROM inspection WHERE inspection_status='Fail'")
    failed = cursor.fetchone()[0]

    # Pending Inspections
    cursor.execute("SELECT COUNT(*) FROM inspection WHERE final_decision=''")
    pending = cursor.fetchone()[0]

    # Quality Rate
    if total > 0:
        quality_rate = round((passed / total) * 100, 2)
    else:
        quality_rate = 0

    # ---------------- Pagination ----------------

    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    # Total Records
    cursor.execute("SELECT COUNT(*) FROM inspection")
    total_records = cursor.fetchone()[0]

    total_pages = (total_records + per_page - 1) // per_page

    # Current Page Records
    cursor.execute("""
        SELECT
            inspection_id,
            article_number,
            tire_size,
            inspection_status,
            inspector_name,
            inspection_date
        FROM inspection
        ORDER BY inspection_id DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset))

    recent_inspections = cursor.fetchall()

    # Last 7 Inspections
    cursor.execute("""
        SELECT inspection_date, COUNT(*)
        FROM inspection
        GROUP BY inspection_date
        ORDER BY inspection_date ASC
        LIMIT 7
    """)

    graph_data = cursor.fetchall()

    graph_labels = []
    graph_values = []

    for row in graph_data:
        graph_labels.append(row[0])
        graph_values.append(row[1])

    # Pass Count
    cursor.execute("""
        SELECT COUNT(*)
        FROM inspection
        WHERE inspection_status='Pass'
    """)
    pass_count = cursor.fetchone()[0]

    # Fail Count
    cursor.execute("""
        SELECT COUNT(*)
        FROM inspection
        WHERE inspection_status='Fail'
    """)
    fail_count = cursor.fetchone()[0]

    conn.close()

    username = session.get("username", "Admin")

    return render_template(

        "dashboard.html",

        username=username,

        total=total,

        passed=passed,

        failed=failed,

        pending=pending,

        quality_rate=quality_rate,

        recent_inspections=recent_inspections,

        pass_count=pass_count,

        fail_count=fail_count,

        graph_labels=graph_labels,

        graph_values=graph_values,

        page=page,

        total_pages=total_pages

    )
# ---------------- INSPECTION ----------------
@app.route("/inspection", methods=["GET", "POST"])
def inspection():

    if request.method == "POST":

        tire_id = request.form["tire_id"]
        article_number = request.form["article_number"]
        tire_size = request.form["tire_size"]
        pattern_name = request.form["pattern_name"]
        batch_number = request.form["batch_number"]
        inspector_name = request.form["inspector_name"]
        inspection_date = request.form["inspection_date"]
        shift = request.form["shift"]
        machine_name = request.form["machine_name"]
        inspection_status = request.form["inspection_status"]
        remarks = request.form["remarks"]
        final_decision = request.form["final_decision"]

        conn = sqlite3.connect("qims.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO inspection(
            tire_id,
            article_number,
            tire_size,
            pattern_name,
            batch_number,
            inspector_name,
            inspection_date,
            shift,
            machine_name,
            inspection_status,
            remarks,
            final_decision
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            tire_id,
            article_number,
            tire_size,
            pattern_name,
            batch_number,
            inspector_name,
            inspection_date,
            shift,
            machine_name,
            inspection_status,
            remarks,
            final_decision
        ))

        # Save inspection
        conn.commit()

        # Get inspection ID
        inspection_id = cursor.lastrowid

        conn.close()

        # If Fail -> Open Raise Defect page
        if inspection_status == "Fail":

            return redirect(url_for(
                "defect",
                inspection_id=inspection_id,
                tire_id=tire_id,
                article_number=article_number,
                raised_by=inspector_name,
                defect_date=inspection_date
            ))

        # If Pass -> Dashboard
        return redirect(url_for("dashboard"))

    return render_template("inspection.html")

# ---------------- INSPECTION DATA ----------------

@app.route("/inspection-data")
def inspection_data():

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inspection")

    data = cursor.fetchall()

    conn.close()

    return str(data)


@app.route("/defect-data")
def defect_data():

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM defects")

    data = cursor.fetchall()

    conn.close()

    return str(data)
# ---------------- CLEAR DEFECTS ----------------

@app.route("/clear-defects")
def clear_defects():

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM defects")

    conn.commit()
    conn.close()

    return "Defects table cleared and ID reset."

# ---------------- INSPECTION RECORDS ----------------

@app.route("/records")
def records():

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    # Summary Cards

    cursor.execute("SELECT COUNT(*) FROM inspection")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inspection WHERE inspection_status='Pass'")
    passed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inspection WHERE inspection_status='Fail'")
    failed = cursor.fetchone()[0]

    # Inspection Records

    cursor.execute("""
        SELECT
            inspection_id,
            tire_id,
            article_number,
            tire_size,
            pattern_name,
            inspection_status,
            inspector_name,
            inspection_date
        FROM inspection
        ORDER BY inspection_id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "records.html",
        records=records,
        total=total,
        passed=passed,
        failed=failed
    )


@app.route("/defect", methods=["GET", "POST"])
def defect():

    if request.method == "POST":

        inspection_id = request.form["inspection_id"]
        tire_id = request.form["tire_id"]
        article_number = request.form["article_number"]
        defect_category = request.form["defect_category"]
        severity = request.form["severity"]
        defect_date = request.form["defect_date"]
        raised_by = request.form["raised_by"]
        defect_description = request.form["defect_description"]

        conn = sqlite3.connect("qims.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO defects(
            inspection_id,
            tire_id,
            article_number,
            defect_category,
            severity,
            defect_date,
            defect_description,
            raised_by
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,(
            inspection_id,
            tire_id,
            article_number,
            defect_category,
            severity,
            defect_date,
            defect_description,
            raised_by
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("tracker"))

    # ---------- GET DATA FROM URL ----------

    inspection_id = request.args.get("inspection_id", "")
    tire_id = request.args.get("tire_id", "")
    article_number = request.args.get("article_number", "")
    raised_by = request.args.get("raised_by", "")
    defect_date = request.args.get("defect_date", "")

    return render_template(
        "defect.html",
        inspection_id=inspection_id,
        tire_id=tire_id,
        article_number=article_number,
        raised_by=raised_by,
        defect_date=defect_date
    )
# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    # ==========================
    # Users Table
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT NOT NULL,

        email TEXT NOT NULL,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )
    """)

    # ==========================
    # Inspection Table
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inspection(

        inspection_id INTEGER PRIMARY KEY AUTOINCREMENT,

        tire_id TEXT NOT NULL,

        article_number TEXT NOT NULL,

        tire_size TEXT NOT NULL,

        pattern_name TEXT NOT NULL,

        batch_number TEXT NOT NULL,

        inspector_name TEXT NOT NULL,

        inspection_date TEXT NOT NULL,

        shift TEXT NOT NULL,

        machine_name TEXT NOT NULL,

        inspection_status TEXT NOT NULL,

        remarks TEXT,

        final_decision TEXT NOT NULL

    )
    """)

    # ==========================
    # Defect Table
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS defects(

        defect_id INTEGER PRIMARY KEY AUTOINCREMENT,

        inspection_id INTEGER,

        tire_id TEXT NOT NULL,

        article_number TEXT NOT NULL,

        defect_category TEXT NOT NULL,

        severity TEXT NOT NULL,

        defect_date TEXT NOT NULL,

        defect_description TEXT NOT NULL,

        raised_by TEXT NOT NULL,

        FOREIGN KEY(inspection_id)
        REFERENCES inspection(inspection_id)

    )
    """)

    conn.commit()
    conn.close()   

    @app.route("/defect-library")
    def defect_library():
        return render_template("defect_library.html")

        # ---------------- DEFECT TRACKER ----------------

@app.route("/tracker")
def tracker():

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            defect_id,
            tire_id,
            article_number,
            defect_category,
            severity,
            defect_date,
            raised_by,
            defect_description
        FROM defects
        ORDER BY defect_id DESC
    """)

    defects = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM defects")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM defects WHERE severity='High'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM defects WHERE severity='Medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM defects WHERE severity='Low'")
    low = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "tracker.html",
        defects=defects,
        total=total,
        high=high,
        medium=medium,
        low=low
    )
# ---------------- REPORT ----------------

@app.route("/report")
def report():

    conn = sqlite3.connect("qims.db")
    cursor = conn.cursor()

    selected_date = request.args.get("date", "")

    # ===============================
    # Summary Cards + Report Table
    # ===============================

    if selected_date:

        cursor.execute(
            "SELECT COUNT(*) FROM inspection WHERE inspection_date=?",
            (selected_date,)
        )
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM inspection
            WHERE inspection_status='Pass'
            AND inspection_date=?
        """, (selected_date,))
        passed = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM inspection
            WHERE inspection_status='Fail'
            AND inspection_date=?
        """, (selected_date,))
        failed = cursor.fetchone()[0]

        quality_rate = round((passed / total) * 100, 2) if total else 0

        cursor.execute("""
            SELECT
                inspection_id,
                tire_id,
                article_number,
                tire_size,
                inspector_name,
                inspection_status,
                inspection_date
            FROM inspection
            WHERE inspection_date=?
            ORDER BY inspection_id DESC
        """, (selected_date,))

    else:

        cursor.execute("SELECT COUNT(*) FROM inspection")
        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM inspection WHERE inspection_status='Pass'"
        )
        passed = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM inspection WHERE inspection_status='Fail'"
        )
        failed = cursor.fetchone()[0]

        quality_rate = round((passed / total) * 100, 2) if total else 0

        cursor.execute("""
            SELECT
                inspection_id,
                tire_id,
                article_number,
                tire_size,
                inspector_name,
                inspection_status,
                inspection_date
            FROM inspection
            ORDER BY inspection_id DESC
        """)

    report_data = cursor.fetchall()

    # ===============================
    # Inspection Trend
    # ===============================

    if selected_date:

        cursor.execute("""
            SELECT inspection_date, COUNT(*)
            FROM inspection
            WHERE inspection_date=?
            GROUP BY inspection_date
            ORDER BY inspection_date
        """, (selected_date,))

    else:

        cursor.execute("""
            SELECT inspection_date, COUNT(*)
            FROM inspection
            GROUP BY inspection_date
            ORDER BY inspection_date
        """)

    trend = cursor.fetchall()

    trend_labels = [row[0] for row in trend]
    trend_values = [row[1] for row in trend]

    # ===============================
    # Pass vs Reject Chart
    # ===============================

    pass_count = passed
    fail_count = failed

       # ===============================
    # Top 5 Defects
    # ===============================

    if selected_date:

        cursor.execute("""
            SELECT defect_category, COUNT(*)
            FROM defects
            WHERE defect_date=?
            GROUP BY defect_category
            ORDER BY COUNT(*) DESC
            LIMIT 5
        """, (selected_date,))

    else:

        cursor.execute("""
            SELECT defect_category, COUNT(*)
            FROM defects
            GROUP BY defect_category
            ORDER BY COUNT(*) DESC
            LIMIT 5
        """)

    defects = cursor.fetchall()

    defect_labels = [row[0] for row in defects]
    defect_values = [row[1] for row in defects]

    conn.close()

    return render_template(
        "report.html",
        username=session["username"],
        total=total,
        passed=passed,
        failed=failed,
        quality_rate=quality_rate,
        report_data=report_data,
        selected_date=selected_date,
        trend_labels=trend_labels,
        trend_values=trend_values,
        pass_count=pass_count,
        fail_count=fail_count,
        defect_labels=defect_labels,
        defect_values=defect_values,
    )
# ---------------- MAIN ----------------
init_db()

if __name__ == "__main__":
    app.run(debug=True)