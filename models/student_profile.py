from extensions import db


class StudentProfile(db.Model):
    __tablename__ = "student_profile"

    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    education = db.Column(db.String(100))
    interests = db.Column(db.String(200))
