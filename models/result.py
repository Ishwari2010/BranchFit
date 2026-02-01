from extensions import db


class Result(db.Model):
    __tablename__ = "results"

    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    recommended_branch = db.Column(db.String(100))
    score = db.Column(db.Float)
