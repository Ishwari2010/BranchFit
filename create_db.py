from app import app
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

# Create all tables
with app.app_context():
    db.create_all()

    # Create admin if not exists
    if not User.query.filter_by(email="admin@branchfit.com").first():
        admin = User(
            name="System Admin",
            email="admin@branchfit.com",
            password=generate_password_hash("admin123"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully")

print("Database created successfully")
