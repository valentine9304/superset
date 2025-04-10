from flask import request
from flask_restx import Namespace, Resource, fields

from app.utils.cache import cache_result
from app.repositories.sales import SaleRepository
from app.validators.sales import SaleDateSchema

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
        data = {
            "start_date": request.args.get('start_date'),
            "end_date": request.args.get('end_date')
        }
        schema = SaleDateSchema()
        errors = schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        start_date = SaleDateSchema.parse_date(data['start_date'])
        end_date = SaleDateSchema.parse_date(data['end_date'])

        total_sales = SaleRepository.get_total_sales(start_date, end_date)
        return {'total_sales': round(total_sales, 2) if total_sales else 0}


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
        data = {
            "start_date": request.args.get('start_date'),
            "end_date": request.args.get('end_date')
        }
        schema = SaleDateSchema()
        errors = schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        limit = request.args.get('limit', default=5, type=int)
        start_date = SaleDateSchema.parse_date(data['start_date'])
        end_date = SaleDateSchema.parse_date(data['end_date'])

        top_products = SaleRepository.get_top_products(start_date, end_date, limit)
        return [
            {
                "product_name": product.name,
                "total_sold": product.total_sold,
                "total_price": round(product.total_price, 2),
            }
            for product in top_products
        ]
