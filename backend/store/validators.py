from cerberus import Validator

from backend.store.models import Category, Type


class ProductValidator(Validator):
    def _check_with_category_exist(self, field, value):
        if not Category.query.get(value):
            self._error(field, f"Category with id={value} not exist")

    def _check_with_type_exist(self, field, value):
        if not Type.query.get(value):
            self._error(field, f"Type with id={value} not exist")


CATEGORY_SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
    }
}

CREATE_PRODUCT_SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'sku': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'stocks': {
        'type': 'integer',
        'coerce': int,
        'min': 0,
    },
    'category_id': {
        'type': 'integer',
        'coerce': int,
        'required': True,
        'check_with': 'category_exist',
    },
    'type_id': {
        'type': 'integer',
        'coerce': int,
        'required': True,
        'check_with': 'type_exist',
    },
}


UPDATE_PRODUCT_SCHEMA = {
    'name': {
        'type': 'string',
        'empty': False,
    },
    'sku': {
        'type': 'string',
        'empty': False,
    },
    'stocks': {
        'type': 'integer',
        'coerce': int,
        'min': 0,
    },
    'category_id': {
        'type': 'integer',
        'coerce': int,
        'check_with': 'category_exist',
    },
    'type_id': {
        'type': 'integer',
        'coerce': int,
        'check_with': 'type_exist',
    },
}

RESERVE_PRODUCT_SCHEMA = {
    'stock_reserve': {
        'type': 'integer',
        'coerce': int,
        'required': True,
        'min': 1,
    },
}

BULK_UPDATE_PRODUCT_SCHEMA = {
    'ids': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'integer',
            'coerce': int,
            'required': True,
            'min': 1,
        }
    },
    'fields': {
        'type': 'dict',
        'required': True,
        'schema': UPDATE_PRODUCT_SCHEMA
    }
}

category_validator = type_validator = Validator(CATEGORY_SCHEMA)
create_product_validator = ProductValidator(CREATE_PRODUCT_SCHEMA)
update_product_validator = ProductValidator(UPDATE_PRODUCT_SCHEMA)
reserve_product_validator = ProductValidator(RESERVE_PRODUCT_SCHEMA)
bulk_update_product_validator = ProductValidator(BULK_UPDATE_PRODUCT_SCHEMA)
