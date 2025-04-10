from flask import request, abort
from flask_restx import Namespace, Resource, fields

from app.utils.cache import cache_result, clear_cache_by_prefix, clear_cache_key
from app.repositories.product import ProductRepository
from app.validators.product import ProductSchema

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
        return ProductRepository.get_all()

    @ns.expect(product_model)
    def post(self):
        """Создать новый продукт"""
        data = request.json
        schema = ProductSchema()
        errors = schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        ProductRepository.create(data)
        clear_cache_by_prefix('all_products_cache')
        return {'message': 'Product created successfully'}, 201


@ns.route('/<int:id>')
class ProductResource(Resource):
    @ns.marshal_with(product_model)
    @cache_result('product_cache')
    def get(self, id):
        """Получить продукт по ID"""
        product = ProductRepository.get_by_id(id)
        if not product:
            abort(404, description="Product with the given ID does not exist.")
        return product

    @ns.expect(product_model)
    def put(self, id):
        """Обновить продукт по ID"""
        product = ProductRepository.get_by_id(id)
        if not product:
            abort(404, description="Product with the given ID does not exist.")

        data = request.json
        schema = ProductSchema()
        errors = schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        ProductRepository.update(product, data)

        clear_cache_key('product_cache', str(id))
        clear_cache_by_prefix('all_products_cache')

        return {'message': 'Product updated successfully'}

    def delete(self, id):
        """Удалить продукт по ID"""
        product = ProductRepository.get_by_id(id)
        if not product:
            abort(404, description="Product with the given ID does not exist.")

        ProductRepository.delete(product)

        clear_cache_key('product_cache', str(id))
        clear_cache_by_prefix('all_products_cache')

        return {'message': 'Product deleted successfully'}
