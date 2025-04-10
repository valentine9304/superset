from sqlalchemy import func

from app import db
from app.models import Sale, Product


class SaleRepository:
    @staticmethod
    def get_total_sales(start_date, end_date):
        return (
            db.session.query(func.sum(Sale.total_price))
            .join(Product)
            .filter(Sale.date >= start_date, Sale.date <= end_date)
            .scalar()
        )

    @staticmethod
    def get_top_products(start_date, end_date, limit):
        return (
            db.session.query(
                Product.name,
                func.sum(Sale.quantity).label("total_sold"),
                func.sum(Sale.total_price).label("total_price")
            )
            .join(Sale)
            .filter(Sale.date >= start_date, Sale.date <= end_date)
            .group_by(Product.id)
            .order_by(func.sum(Sale.quantity).desc())
            .limit(limit)
            .all()
        )
