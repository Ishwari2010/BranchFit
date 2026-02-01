from extensions import db


class BranchQuestion(db.Model):
    __tablename__ = "branch_questions"

    question_id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(50))
    text = db.Column(db.Text)

    scale_1_label = db.Column(db.String(50), default="Strongly Disagree")
    scale_2_label = db.Column(db.String(50), default="Disagree")
    scale_3_label = db.Column(db.String(50), default="Neutral")
    scale_4_label = db.Column(db.String(50), default="Agree")
    scale_5_label = db.Column(db.String(50), default="Strongly Agree")
