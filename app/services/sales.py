from app.repositories.sales import SaleRepository
from app.validators.sales import SaleDateSchema


class SaleService:
    def __init__(self, sale_repository: SaleRepository):
        self.sale_repository = sale_repository

    def get_total_sales(self, start_date, end_date):
        """Получить общую сумму продаж за указанный период"""
        return self.sale_repository.get_total_sales(start_date, end_date)

    def get_top_products(self, start_date, end_date, limit):
        """Получить топ-N самых продаваемых товаров за указанный период"""
        return self.sale_repository.get_top_products(start_date, end_date, limit)

    def validate_dates(self, start_date, end_date):
        """Проверка и парсинг дат с использованием SaleDateSchema"""
        schema = SaleDateSchema()
        data = {"start_date": start_date, "end_date": end_date}
        errors = schema.validate(data)
        if errors:
            return None, None, errors

        start_date = SaleDateSchema.parse_date(start_date)
        end_date = SaleDateSchema.parse_date(end_date)
        return start_date, end_date, None
