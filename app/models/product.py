from app import db
from sqlalchemy import func


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    sales = db.relationship('Sale', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"
