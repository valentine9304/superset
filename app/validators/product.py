from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from app.models import Category


class ProductSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=lambda p: p > 0)
    category_id = fields.Int(required=True)

    @validates_schema
    def validate_category(self, data, **kwargs):
        category = Category.query.get(data.get('category_id'))
        if not category:
            raise ValidationError('Category ID does not exist.', field_name='category_id')
