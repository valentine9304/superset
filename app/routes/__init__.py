from . import products, sales


def register_routes(app):
    app.register_blueprint(products.bp)
    app.register_blueprint(sales.bp)
