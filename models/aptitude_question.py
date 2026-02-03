from extensions import db

class AptitudeQuestion(db.Model):
    __tablename__ = "aptitude_questions"

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    question_index = db.Column(db.Integer, unique=True, nullable=False)
