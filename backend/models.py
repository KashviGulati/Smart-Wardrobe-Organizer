from database import db

class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    last_worn = db.Column(db.String(50), nullable=True)
    occasion = db.Column(db.String(50), nullable=True)  # ✅ New column for occasion

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "color": self.color,
            "last_worn": self.last_worn,
            "occasion": self.occasion
        }
