from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy import func
from datetime import datetime

from app import db
from app.models import Sale, Product
from app.utils.cache import cache_result

ns = Namespace('sales', description='Sales methods')

sale_model = ns.model('Sale', {
    'product_id': fields.Integer(required=True, description='Product ID'),
    'quantity': fields.Integer(required=True, description='Quantity sold'),
    'date': fields.String(required=True, description='Sale date')
})


@ns.route('/total')
class SalesTotal(Resource):
    @ns.doc(
        params={
            "start_date": {
                "description": "Start date (DD.MM.YYYY)",
                "in": "query",
                "type": "string",
                "required": True,
            },
            "end_date": {
                "description": "End date (DD.MM.YYYY)",
                "in": "query",
                "type": "string",
                "required": True,
            },
        }
    )
    @cache_result('total_products_cache')
    def get(self):
        """Возвращает общую сумму продаж за указанный период c учётом скидок"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return {'error': 'Both start_date and end_date must be provided'}, 400

        start_date, end_date, error = parse_dates(start_date, end_date)
        if error:
            return error, 400

        total_sales = (
            db.session.query(
                func.sum(Sale.total_price).label("total_sales")
            )
            .join(Product)
            .filter(Sale.date >= start_date, Sale.date <= end_date)
            .scalar()
        )

        return {'total_sales': round(total_sales, 2) or 0}


@ns.route('/top-products')
class TopProducts(Resource):
    @ns.doc(
        params={
            "start_date": {
                "description": "Start date (DD.MM.YYYY)",
                "in": "query",
                "type": "string",
                "required": True,
            },
            "end_date": {
                "description": "End date (DD.MM.YYYY)",
                "in": "query",
                "type": "string",
                "required": True,
            },
            "limit": {
                "description": "Limit for top products (Optional)",
                "in": "query",
                "type": "integer",
                "required": False,
                "default": 5
            }
        }
    )
    @cache_result('top_products_cache')
    def get(self):
        """Возвращает топ-N самых продаваемых товаров за указанный период.
        Фильтрует по количеству продаж и показывает общую сумму по цене c учётом скидок."""
        start_date = request.args.get("start_date")
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', default=5, type=int)

        if not start_date or not end_date:
            return {'error': 'Both start_date and end_date must be provided'}, 400

        start_date, end_date, error = parse_dates(start_date, end_date)
        if error:
            return error, 400

        top_products = (
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

        return [
            {
                "product_name": product.name,
                "total_sold": product.total_sold,
                "total_price": round(product.total_price, 2),
            }
            for product in top_products
        ]


def parse_dates(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
        end_date = datetime.strptime(end_date_str, '%d.%m.%Y')
    except ValueError:
        return None, None, {'error': 'Invalid date format. Use DD.MM.YYYY.'}

    if start_date > end_date:
        return None, None, {'error': 'Start date cannot be later than end date.'}

    if end_date > datetime.today():
        return None, None, {'error': 'End date cannot be later than today.'}

    return start_date, end_date, None
