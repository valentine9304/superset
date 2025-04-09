from flask import request, abort
from flask_restx import Namespace, Resource, fields

from app.models.products import Product, Category, db
from app.utils.cache import cache_result

ns = Namespace('products', description='Products methods')

product_model = ns.model('Product', {
    'id': fields.Integer(readonly=True, description='Product ID'),
    'name': fields.String(required=True, description='Product name'),
    'price': fields.Float(required=True, description='Product price'),
    'category_id': fields.Integer(required=True, description='Category ID')
})


@ns.route('/')
class ProductList(Resource):
    @ns.marshal_list_with(product_model)
    @cache_result('all_products_cache')
    def get(self):
        """Получить список всех продуктов"""
        products = Product.query.all()
        return products

    @ns.expect(product_model)
    def post(self):
        """Создать новый продукт"""
        data = request.json

        validation_error = validate_product_data(data)
        if validation_error:
            return validation_error

        product = Product(
            name=data["name"], category_id=data["category_id"], price=data["price"]
        )
        db.session.add(product)
        db.session.commit()
        return {'message': 'Product created successfully'}, 201


@ns.route('/<int:id>')
class ProductResource(Resource):
    @ns.marshal_with(product_model)
    @cache_result('product_cache')
    def get(self, id):
        """Получить продукт по ID"""
        product = Product.query.get(id)
        if not product:
            abort(404, description="Product with the given ID does not exist.")
        return product

    @ns.expect(product_model)
    def put(self, id):
        """Обновить продукт по ID"""
        product = Product.query.get(id)
        if not product:
            abort(404, description="Product with the given ID does not exist.")

        data = request.json
        validation_error = validate_product_data(data)
        if validation_error:
            return validation_error

        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.category_id = data.get('category_id', product.category_id)

        db.session.commit()
        return {'message': 'Product updated successfully'}

    def delete(self, id):
        """Удалить продукт по ID"""
        product = Product.query.get_or_404(id)
        if not product:
            abort(404, description="Product with the given ID does not exist.")
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}


def validate_product_data(data):
    category = Category.query.get(data.get("category_id"))
    if not category:
        return {'error': 'Category ID does not exist.'}, 400

    if data.get("price", 0) <= 0:
        return {'error': 'Price must be greater than 0.'}, 400

    if not isinstance(data.get("name"), str) or not data.get("name").strip():
        return {'error': 'Name must be a non-empty string.'}, 400

    return None
