from extensions import db

class Question(db.Model):
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True)

    # Actual question text
    text = db.Column(db.Text, nullable=False)

    # Index used by ML model (0–59)
    question_index = db.Column(db.Integer, nullable=False, unique=True)
