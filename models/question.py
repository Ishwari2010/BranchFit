from extensions import db


class Question(db.Model):
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
