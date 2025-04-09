from flask_restx import Api
from . import products, sales


def register_routes(app):
    api = Api(app, version='1.0', title='My API', description='Simple API')
    api.add_namespace(products.ns, path='/api/products')
    api.add_namespace(sales.ns, path='/api/sales')
