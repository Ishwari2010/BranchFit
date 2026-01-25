from extensions import db

class Answer(db.Model):
    __tablename__ = "answers"

    answer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    answer = db.Column(db.String(50))
