from flask import request, abort
from flask_restx import Namespace, Resource, fields

from app.repositories import ProductRepository
from app.validators import ProductSchema
from app.services import ProductService
from app.utils.cache import cache_result, clear_cache_by_prefix, clear_cache_key


product_service = ProductService(ProductRepository(), ProductSchema())
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
        return product_service.get_all_products()

    @ns.expect(product_model)
    def post(self):
        """Создать новый продукт"""
        data = request.json
        product, errors = product_service.create_product(data)
        if errors:
            return {'errors': errors}, 400
        clear_cache_by_prefix('all_products_cache')
        return {'message': 'Product created successfully'}, 201

@ns.route('/<int:id>')
class ProductResource(Resource):
    @ns.marshal_with(product_model)
    @cache_result('product_cache')
    def get(self, id):
        """Получить продукт по ID"""
        product = product_service.get_by_id(id)
        if not product:
            abort(404, description="Product with the given ID does not exist.")
        return product

    @ns.expect(product_model)
    def put(self, id):
        """Обновить продукт по ID"""
        data = request.json
        product, errors = product_service.update_product(id, data)
        if errors:
            return errors, 400
        clear_cache_by_prefix('all_products_cache')
        clear_cache_key('product_cache', str(id))
        return {'message': 'Product updated successfully'}

    def delete(self, id):
        """Удалить продукт по ID"""
        product, errors = product_service.delete_product(id)
        if errors:
            return errors, 400
        clear_cache_by_prefix('all_products_cache')
        clear_cache_key('product_cache', str(id))
        return {'message': 'Product deleted successfully'}
