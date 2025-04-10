from sqlalchemy import func

from app import db
from .product import Product


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=func.current_date())
    discount = db.Column(db.Float, nullable=True)

    total_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Sale {self.product.name} on {self.date}>"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        product = Product.query.get(self.product_id)

        if product:
            discount_amount = (self.discount or 0) * product.price * self.quantity
            self.total_price = round((product.price * self.quantity) - discount_amount, 2)
        else:
            self.total_price = 0.0
