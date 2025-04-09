from app import create_app, db
from app.models import Category, Product, Sale
from datetime import datetime, timedelta
import random

app = create_app(with_routes=False)

CATEGORIES = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Camera", "Headphones"],
    "Clothing": ["T-shirt", "Jeans", "Jacket", "Sneakers", "Hat"],
    "Books": ["Novel", "Biography", "Science Book", "Fantasy Book", "History Book"]
}


def data_migration():
    with app.app_context():
        Sale.query.delete()
        Product.query.delete()
        Category.query.delete()
        db.session.commit()

        categories = {}
        for category_name, products in CATEGORIES.items():
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

            categories[category_name] = category

            for product_name in products:
                random_price = round(random.uniform(10, 500), 2)
                product = Product(name=product_name, category_id=category.id, price=random_price)
                db.session.add(product)

        db.session.commit()
        print("Категории и продукты добавлены.")

        products = Product.query.all()
        for product in products:
            for _ in range(random.randint(10, 30)):
                days_ago = random.randint(0, 180)
                sale_date = datetime.now() - timedelta(days=days_ago)
                quantity = random.randint(1, 5)

                sale = Sale(
                    product_id=product.id,
                    quantity=quantity,
                    date=sale_date.date()
                )
                db.session.add(sale)

        db.session.commit()
        print("Продажи добавлены.")


if __name__ == "__main__":
    data_migration()
