from flask import Flask
from routes import app_routes
from database import init_db

app = Flask(__name__)
app.config.from_object("config.Config")

# Initialize database
init_db(app)

# Register Routes
app.register_blueprint(app_routes)

if __name__ == "__main__":
    app.run(debug=True)
