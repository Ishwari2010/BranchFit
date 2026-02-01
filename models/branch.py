from extensions import db


class Branch(db.Model):
    __tablename__ = "branches"

    branch_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
