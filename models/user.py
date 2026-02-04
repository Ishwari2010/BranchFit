from extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    # NEW PROFILE FIELDS
    phone = db.Column(db.String(15))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(200))  # store image filename

    def __repr__(self):
        return f"<User {self.email}>"
