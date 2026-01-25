from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask import session
from models.student_profile import StudentProfile
from models.question import Question


import os

app = Flask(__name__)
app.secret_key = "branchfit_secret"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "system.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# IMPORT MODELS AFTER db INIT
from models.user import User

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        print("LOGIN ATTEMPT:", email)  # ADD THIS

        user = User.query.filter_by(email=email).first()

        print("USER FOUND:", user)  # ADD THIS

        if user and check_password_hash(user.password, password):
            print("PASSWORD MATCH")  # ADD THIS

            session.clear()
            session["user_id"] = user.user_id
            session["user_name"] = user.name
            session["role"] = user.role

            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))

        print("LOGIN FAILED")  # ADD THIS

    return render_template("login.html")







@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("login"))

        hashed_pw = generate_password_hash(password)

        user = User(
            name=name,
            email=email,
            password=hashed_pw,
            role = "student"


        )

        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.user_id
        session["user_name"] = user.name


        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user_name=session["user_name"]
    )

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        education = request.form["education"]
        interests = request.form["interests"]

        existing_profile = StudentProfile.query.filter_by(
            user_id=session["user_id"]
        ).first()

        if existing_profile:
            existing_profile.education = education
            existing_profile.interests = interests
        else:
            profile = StudentProfile(
                user_id=session["user_id"],
                education=education,
                interests=interests
            )
            db.session.add(profile)

        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("profile.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    return render_template(
        "admin_dashboard.html",
        user_name=session["user_name"]
    )

@app.route("/admin/questions", methods=["GET", "POST"])
def manage_questions():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        q = Question(
            text=request.form["question"],
            option_a=request.form["option_a"],
            option_b=request.form["option_b"],
            option_c=request.form["option_c"],
            option_d=request.form["option_d"]
        )
        db.session.add(q)
        db.session.commit()


    questions = Question.query.all()
    return render_template("manage_questions.html", questions=questions)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
