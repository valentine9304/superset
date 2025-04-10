from app import db
from app.models import Product


class ProductRepository:
    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def create(data):
        product = Product(
            name=data["name"],
            category_id=data["category_id"],
            price=data["price"]
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update(product, data):
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.category_id = data.get('category_id', product.category_id)
        db.session.commit()

    @staticmethod
    def delete(product):
        db.session.delete(product)
        db.session.commit()
