from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initializes the database with the Flask app."""
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
