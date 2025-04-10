from marshmallow import Schema, fields, validates_schema, ValidationError
from datetime import datetime


class SaleDateSchema(Schema):
    start_date = fields.Str(required=True)
    end_date = fields.Str(required=True)

    @staticmethod
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%d.%m.%Y')
        except ValueError:
            raise ValidationError('Date format must be DD.MM.YYYY')

    @validates_schema
    def validate_dates(self, data, **kwargs):
        start_date = self.parse_date(data.get('start_date'))
        end_date = self.parse_date(data.get('end_date'))

        if start_date > end_date:
            raise ValidationError('Start date cannot be after end date.')

        if end_date > datetime.today():
            raise ValidationError('End date cannot be later than today.')
