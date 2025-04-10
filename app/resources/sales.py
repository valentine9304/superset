from flask import request
from flask_restx import Namespace, Resource, fields

from app.repositories import SaleRepository
from app.services import SaleService
from app.utils.cache import cache_result


sale_service = SaleService(SaleRepository())

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

        start_date, end_date, error = sale_service.validate_dates(start_date, end_date)
        if error:
            return {'errors': error}, 400

        total_sales = sale_service.get_total_sales(start_date, end_date)
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
        Фильтрует по количеству продаж и показывает общую сумму по цене с учётом скидок."""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        start_date, end_date, error = sale_service.validate_dates(start_date, end_date)
        if error:
            return {'errors': error}, 400

        limit = request.args.get('limit', default=5, type=int)

        top_products = sale_service.get_top_products(start_date, end_date, limit)
        return [
            {
                "product_name": product.name,
                "total_sold": product.total_sold,
                "total_price": round(product.total_price, 2),
            }
            for product in top_products
        ]
