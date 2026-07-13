from flask import Flask, render_template, request, redirect, url_for, session, send_file
from career_info import career_info
from roadmap import roadmaps
import pickle
from pdf_generator import generate_pdf
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from ai_assistant import ask_ai
from resume_generator import generate_resume



app = Flask(__name__)
app.secret_key = "vidyagram_secret_key"


last_prediction = None
last_info = None
last_roadmap = None

# Load Trained Model
with open("career_model.pkl", "rb") as file:
    model = pickle.load(file)


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Email already exists."

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")
# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session["username"] = user[1]
            session["email"] = user[2]

            return redirect(url_for("dashboard"))

        return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT career,match_score,prediction_date
        FROM predictions
        WHERE email=?
        ORDER BY id DESC
        LIMIT 5
        """,
        (session["email"],)
    )

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        history=history
    )


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# ---------------- AI ASSISTANT ---------------- #

@app.route("/assistant", methods=["GET", "POST"])
def assistant():

    if "username" not in session:
        return redirect(url_for("login"))

    answer = ""
    question = ""

    if request.method == "POST":

        question = request.form["question"]

        try:
            answer = ask_ai(question)

            # Save AI chat to database
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO ai_history(email, question, answer)
            VALUES (?, ?, ?)
            """, (
                session["email"],
                question,
                answer
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            answer = str(e)

    return render_template(
        "assistant.html",
        question=question,
        answer=answer
    )

#--------------Table---------------#

def create_tables():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        career TEXT,
        match_score INTEGER,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        subject TEXT,
        score INTEGER,
        total INTEGER,
        quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        question TEXT,
        answer TEXT,
        chat_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


create_tables()



#-----------LearningHub----------------#
@app.route("/learning")
def learning():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "learning.html",
        username=session["username"]
    )

@app.route("/python")
def python_course():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "python.html",
        username=session["username"]
    )

@app.route("/web")
def web_course():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "web.html",
        username=session["username"]
    )

@app.route("/ml")
def ml_course():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "ml.html",
        username=session["username"]
    )

@app.route("/datascience")
def data_science():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "datascience.html",
        username=session["username"]
    )

# ---------------- INTERVIEW PREPARATION ---------------- #

@app.route("/interview")
def interview():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "interview.html",
        username=session["username"]
    )


# ---------------- RESUME TIPS ---------------- #

@app.route("/resume")
def resume():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "resume.html",
        username=session["username"]
    )


# ---------------- ENGLISH COMMUNICATION ---------------- #

@app.route("/english")
def english():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "english.html",
        username=session["username"]
    )


# ---------------- APTITUDE ---------------- #

@app.route("/aptitude")
def aptitude():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "aptitude.html",
        username=session["username"]
    )

# ---------------- QUIZ DATA ---------------- #

quiz_data = {

    "Python": [
        {
            "question": "Which keyword is used to create a function in Python?",
            "options": ["func", "def", "function", "create"],
            "answer": "def"
        },
        {
            "question": "Python file extension is?",
            "options": [".java", ".py", ".html", ".css"],
            "answer": ".py"
        }
    ],

    "Web Development": [
        {
            "question": "HTML stands for?",
            "options": [
                "Hyper Text Markup Language",
                "High Text Machine Language",
                "Hyper Tool Language",
                "None"
            ],
            "answer": "Hyper Text Markup Language"
        },
        {
            "question": "CSS is used for?",
            "options": [
                "Database",
                "Styling Web Pages",
                "Programming",
                "Server"
            ],
            "answer": "Styling Web Pages"
        }
    ],

    "Machine Learning": [
        {
            "question": "Which library is used for Machine Learning in Python?",
            "options": [
                "Scikit-learn",
                "HTML",
                "React",
                "Bootstrap"
            ],
            "answer": "Scikit-learn"
        },
        {
            "question": "ML learns from?",
            "options": [
                "Data",
                "Images only",
                "HTML",
                "CSS"
            ],
            "answer": "Data"
        }
    ]

}

# ---------------- QUIZ ---------------- #

@app.route("/quiz")
def quiz():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "quiz.html",
        username=session["username"],
        subjects=quiz_data.keys()
    )


@app.route("/start_quiz/<subject>")
def start_quiz(subject):

    if "username" not in session:
        return redirect(url_for("login"))

    questions = quiz_data.get(subject)

    return render_template(
        "questions.html",
        username=session["username"],
        subject=subject,
        questions=questions
    )


@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():

    if "username" not in session:
        return redirect(url_for("login"))

    subject = request.form["subject"]

    questions = quiz_data.get(subject)

    score = 0

    for i, q in enumerate(questions):

        answer = request.form.get(f"q{i}")

        if answer == q["answer"]:
            score += 1

    # Save quiz result to database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO quiz_results(email, subject, score, total)
    VALUES (?, ?, ?, ?)
    """, (
        session["email"],
        subject,
        score,
        len(questions)
    ))

    conn.commit()
    conn.close()

    return render_template(
        "quiz_result.html",
        username=session["username"],
        subject=subject,
        score=score,
        total=len(questions)
    )

#----------------user Profile--------------------#

@app.route("/profile")
def profile():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Total Predictions
    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE email=?
    """, (session["email"],))
    total_predictions = cursor.fetchone()[0]

    # Total Quiz Attempts
    cursor.execute("""
    SELECT COUNT(*)
    FROM quiz_results
    WHERE email=?
    """, (session["email"],))
    total_quizzes = cursor.fetchone()[0]

    # Best Quiz Score
    cursor.execute("""
    SELECT MAX(score)
    FROM quiz_results
    WHERE email=?
    """, (session["email"],))
    best_score = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        "profile.html",
        username=session["username"],
        email=session["email"],
        total_predictions=total_predictions,
        total_quizzes=total_quizzes,
        best_score=best_score
    )

    #---------------Generator resume--------------------#
@app.route("/generate_resume", methods=["POST"])
def generate_resume_pdf():

    if "username" not in session:
        return redirect(url_for("login"))

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    education = request.form["education"]
    skills = request.form["skills"]
    projects = request.form["projects"]

    filename = generate_resume(
        name,
        email,
        phone,
        education,
        skills,
        projects
    )

    return send_file(
    filename,
    as_attachment=True
)

# ---------------- PROGRESS TRACKER ---------------- #

@app.route("/progress")
def progress():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subject, score, total, quiz_date
    FROM quiz_results
    WHERE email=?
    ORDER BY id DESC
    """,
    (session["email"],))

    quiz_history = cursor.fetchall()


    cursor.execute("""
    SELECT career, match_score, prediction_date
    FROM predictions
    WHERE email=?
    ORDER BY id DESC
    """,
    (session["email"],))

    prediction_history = cursor.fetchall()


    conn.close()


    return render_template(
        "progress.html",
        username=session["username"],
        quiz_history=quiz_history,
        prediction_history=prediction_history
    )


#-----------Resume builder-----------------#
@app.route("/resume_builder")
def resume_builder():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("resume_builder.html")

# ---------------- PREDICT ---------------- #

@app.route("/predict", methods=["POST"])
def predict():

    if "username" not in session:
        return redirect(url_for("login"))

    global last_prediction, last_info, last_roadmap

    tenth = float(request.form["tenth"])
    inter = float(request.form["inter"])
    programming = float(request.form["programming"])
    communication = float(request.form["communication"])

    data = [[tenth, inter, programming, communication]]

    prediction = str(model.predict(data)[0]).strip()

    try:
        probabilities = model.predict_proba(data)[0]
        match_score = round(max(probabilities) * 100)
    except Exception:
        match_score = 100

    info = career_info.get(prediction)
    roadmap = roadmaps.get(prediction, [])

    last_prediction = prediction
    last_info = info
    last_roadmap = roadmap

    # Save prediction to database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions(email, career, match_score)
    VALUES (?, ?, ?)
    """, (session["email"], prediction, match_score))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        prediction=prediction,
        info=info,
        roadmap=roadmap,
        match_score=match_score
    )
    
# ---------------- DOWNLOAD PDF ---------------- #

@app.route("/download")
def download():

    if "username" not in session:
        return redirect(url_for("login"))

    global last_prediction, last_info, last_roadmap

    if last_prediction is None:
        return "No prediction available."

    filename = generate_pdf(
        last_prediction,
        last_info,
        last_roadmap
    )

    return send_file(
        filename,
        as_attachment=True
    )


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)