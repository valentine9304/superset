from app.repositories.product import ProductRepository
from app.validators.product import ProductSchema


class ProductService:
    def __init__(self, product_repository: ProductRepository, product_schema: ProductSchema):
        self.product_repository = product_repository
        self.product_schema = product_schema

    def get_all_products(self):
        """Получить список всех продуктов"""
        return self.product_repository.get_all()

    def get_by_id(self, id):
        """Получить продукт по ID"""
        return self.product_repository.get_by_id(id)

    def create_product(self, data):
        """Создать новый продукт"""
        errors = self.product_schema.validate(data)
        if errors:
            return None, errors
        return self.product_repository.create(data), None

    def update_product(self, id, data):
        """Обновить продукт"""
        product = self.product_repository.get_by_id(id)
        if not product:
            return None, {'error': 'Product not found'}

        errors = self.product_schema.validate(data)
        if errors:
            return None, errors
        return self.product_repository.update(product, data), None

    def delete_product(self, id):
        """Удалить продукт"""
        product = self.product_repository.get_by_id(id)
        if not product:
            return None, {'error': 'Product not found'}
        return self.product_repository.delete(product), None
