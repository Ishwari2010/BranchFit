from extensions import db

class Question(db.Model):
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    domain = db.Column(db.String(50))
