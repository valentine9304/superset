from app import db
from sqlalchemy import func


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=func.current_date())

    def __repr__(self):
        return f"<Sale {self.product.name} on {self.date}>"
