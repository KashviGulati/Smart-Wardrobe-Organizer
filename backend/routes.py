from flask import Blueprint, request, jsonify
from database import db
from models import ClothingItem

app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/", methods=["GET"])
def home():
    return "Welcome to the smart closet organizer API!"

# Add clothing item
@app_routes.route("/add-clothing", methods=["POST"])
def add_clothing():
    data = request.json
    new_item = ClothingItem(
        name=data["name"],
        category=data["category"],
        color=data["color"],
        last_worn=data.get("last_worn")
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Clothing item added successfully"}), 201

# Get all clothing items
@app_routes.route("/get-clothing", methods=["GET"])
def get_clothing():
    items = ClothingItem.query.all()
    return jsonify([item.to_dict() for item in items])
