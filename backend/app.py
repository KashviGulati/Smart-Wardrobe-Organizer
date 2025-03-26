from flask import Flask
from flask_cors import CORS
from database import db, init_db
from config import SQLALCHEMY_DATABASE_URI
from routes import app_routes  # Import your routes

app = Flask(__name__, static_folder="static")

# Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Enable CORS (Fixes frontend connection issues)
CORS(app)

# Initialize Database
init_db(app)

# Register Blueprints
app.register_blueprint(app_routes)

# Root Route
@app.route("/", methods=["GET"])
def home():
    return "✅ Smart Closet Organizer API is running!"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
