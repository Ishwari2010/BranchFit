from flask import Flask, render_template, request, redirect, url_for, flash
import flask
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask import session
from models import branch
from models.student_profile import StudentProfile
from models.question import Question
from models.branch_question import BranchQuestion
from models.user import User
from models.aptitude_question import AptitudeQuestion

import joblib
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "branch_predictor_model.pkl")

model = joblib.load(MODEL_PATH)





app = Flask(__name__)
app.secret_key = "branchfit_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.frifsubjsxdfflflpaap:Ishwarishinde@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


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
        session["role"] = user.role


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

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.phone = request.form.get("phone")
        user.bio = request.form.get("bio")

        file = request.files.get("profile_image")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            user.profile_image = f"uploads/{filename}"

        db.session.commit()
        flash("Profile updated!")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)



@app.route("/admin/questions", methods=["GET", "POST"])
def manage_questions():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        question_text = request.form["question_text"]
        question_index = request.form["question_index"]

        new_question = AptitudeQuestion(
            question_text=question_text,
            question_index=question_index
        )

        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for("manage_questions"))

    questions = AptitudeQuestion.query.order_by(AptitudeQuestion.question_index).all()
    return render_template("manage_questions.html", questions=questions)



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin/branch-questions", methods=["GET", "POST"])
def manage_branch_questions():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))


    if request.method == "POST":
        branch = request.form["branch"]
        text = request.form["text"]

        new_question = BranchQuestion(
            branch=branch,
            text=text,
            scale_1_label=request.form["scale_1_label"],
            scale_2_label=request.form["scale_2_label"],
            scale_3_label=request.form["scale_3_label"],
            scale_4_label=request.form["scale_4_label"],
            scale_5_label=request.form["scale_5_label"],
        )

        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for("manage_branch_questions", branch=branch))


        # Get selected branch from URL (default = CS)
    selected_branch = request.args.get("branch", "CS")

    # Show only questions of that branch
    questions = BranchQuestion.query.filter_by(branch=selected_branch).all()

    return render_template(
        "admin_branch_questions.html",
        questions=questions,
        selected_branch=selected_branch
    )

        
        


@app.route("/admin/branch-question/edit/<int:id>", methods=["GET", "POST"])
def edit_branch_question(id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    question = BranchQuestion.query.get_or_404(id)

    if request.method == "POST":
        question.branch = request.form["branch"]
        question.text = request.form["text"]
        question.scale_1_label = request.form["scale_1_label"]
        question.scale_2_label = request.form["scale_2_label"]
        question.scale_3_label = request.form["scale_3_label"]
        question.scale_4_label = request.form["scale_4_label"]
        question.scale_5_label = request.form["scale_5_label"]

        db.session.commit()

        # 🔥 Get branch from form (correct)
        branch = request.form["branch"]
        return redirect(url_for("manage_branch_questions", branch=branch))

    return render_template("edit_branch_question.html", question=question)


@app.route("/admin/branch-question/delete/<int:id>")
def delete_branch_question(id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    branch = request.args.get("branch")  # keep current branch in URL

    question = BranchQuestion.query.get_or_404(id)  # get ONLY this question
    db.session.delete(question)  # delete only this row
    db.session.commit()

    return redirect(url_for("manage_branch_questions", branch=branch))


@app.route("/branch-test/cs", methods=["GET", "POST"])
def cs_branch_test():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    questions = BranchQuestion.query.filter_by(branch="CS").all()

    if request.method == "POST":
        total_score = 0

        for q in questions:
            score = int(request.form.get(f"q{q.question_id}"))
            total_score += score

        avg_score = total_score / len(questions)
        cs_test_percent = (avg_score / 5) * 100

        session["cs_test_percent"] = cs_test_percent
        return redirect(url_for("cs_test_result"))

    return render_template("branch_test.html", questions=questions, branch="CS")

@app.route("/branch-test/cs/result")
def cs_test_result():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    test_percent = session.get("cs_test_percent")

    if test_percent >= 70:
        result = "Strong Aptitude – You show strong suitability for Computer Science."
    elif test_percent >= 50:
        result = "Moderate Aptitude – You can pursue CS with effort."
    else:
        result = "Low Aptitude – CS may not strongly align with your strengths."

    return render_template("branch_result.html",
                           test_percent=test_percent,
                           affinity_percent=None,
                           result=result)

@app.route("/branch-test/it", methods=["GET", "POST"])
def it_branch_test():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    questions = BranchQuestion.query.filter_by(branch="IT").all()

    if request.method == "POST":
        total_score = sum(int(request.form.get(f"q{q.question_id}", 0)) for q in questions)
        avg_score = total_score / len(questions)
        percent = (avg_score / 5) * 100
        session["it_test_percent"] = percent
        return redirect(url_for("it_test_result"))

    return render_template("branch_test.html", questions=questions, branch="IT")

@app.route("/branch-test/it/result")
def it_test_result():
    percent = session.get("it_test_percent", 0)

    if percent >= 70:
        result = "Strong Aptitude for IT."
    elif percent >= 50:
        result = "Moderate Aptitude for IT."
    else:
        result = "Low Aptitude for IT."

    return render_template("branch_result.html",
                           test_percent=percent,
                           result=result)



from flask import session

@app.route("/common_test", methods=["GET", "POST"])
def common_test():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # First question
    if "current_index" not in session:
        session["current_index"] = 0
        session["answers"] = {}

    # Save previous answer
    if request.method == "POST":
        for key, value in request.form.items():
            session["answers"][key] = value

        session["current_index"] += 1

    # If all 60 questions answered → predict
    all_questions = Question.query.order_by(Question.question_id).all()

    if session["current_index"] >= len(all_questions):
        prediction = predict_branch(session["answers"])
        session.clear()
        return render_template("branch_result.html", prediction=prediction)


    # Get all questions ordered
    all_questions = Question.query.order_by(Question.question_id).all()

    # Pick the current question
    question = all_questions[session["current_index"]]



    return render_template(
        "branch_test.html",
        questions=[question],
        test_type="adaptive"
    )





import joblib
import os

MODEL_PATH = os.path.join(BASE_DIR, "branch_predictor_model.pkl")
model = joblib.load(MODEL_PATH)


def predict_branch(answer_dict):
    # Start with neutral values for all 60 questions
    feature_vector = [3] * 60

    for q_name, value in answer_dict.items():
        q_id = int(q_name.replace("q", ""))
        question = AptitudeQuestion.query.get(q_id)


        if question:
            feature_vector[question.question_index] = int(value)

    prediction = model.predict([feature_vector])[0]
    return prediction



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    
