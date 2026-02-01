from extensions import db


class BranchWeight(db.Model):
    __tablename__ = "branch_weights"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.branch_id"))
    weight = db.Column(db.Integer)
