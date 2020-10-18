import json

from flask.views import MethodView
from flask import request
from flask import jsonify

from backend.store.models import db, Category, Type, Product
from backend.store.validators import (
    category_validator, type_validator, create_product_validator,
    update_product_validator, reserve_product_validator,
    bulk_update_product_validator
)
from backend.utils import parse_querystring


class MethodViewAPI(MethodView):
    EXTRA_ACTION_ARG = 'extra_action'

    model = None
    validator = None

    def __init__(self):
        super().__init__()
        if not self.validator:
            self.validator = self.get_validator()

    def get_validator(self):
        return None

    def _get_object(self, id):
        return self.model.query.get_or_404(id)

    def _get_list(self):
        return self.model.query.all()

    def _get_request_data(self):
        return request.get_data(as_text=True) or '{}'

    def get(self, id):
        if id is None:
            list = self._get_list()
            return jsonify([item.to_dict() for item in list])
        else:
            object = self._get_object(id)
            return jsonify(object.to_dict())

    def post(self):
        data = json.loads(self._get_request_data())
        if self.validator(data):
            object = self.model(**data)
            db.session.add(object)
            db.session.commit()
            return jsonify(object.to_dict()), 201
        else:
            return jsonify(self.validator.errors), 400

    def put(self, id):
        data = json.loads(self._get_request_data())
        if self.validator(data):
            object = self._get_object(id)
            self.model.query.filter(self.model.id == object.id).update(
                {**data}
            )
            db.session.commit()
            return jsonify(object.to_dict()), 201
        else:
            return jsonify(self.validator.errors), 400

    def delete(self, id):
        object = self._get_object(id)
        db.session.delete(object)
        db.session.commit()
        return jsonify('deleted')



class CategoryAPI(MethodViewAPI):
    model = Category
    validator = category_validator


class TypeAPI(MethodViewAPI):
    model = Type
    validator = type_validator


class ProductAPI(MethodViewAPI):
    model = Product

    def get_validator(self):
        if request.method == 'POST':
            return create_product_validator
        elif request.method == 'PUT':
            return update_product_validator

    def _get_filter_dict(self, filters):
        if 'category' in filters:
            category = Category.query.filter_by(
                name=filters['category']
            ).first()
            if category:
                filters.pop('category')
                filters['category_id'] = category.id
        if 'type' in filters:
            type = Type.query.filter_by(name=filters['type']).first()
            if type:
                filters.pop('type')
                filters['type_id'] = type.id
        return filters

    def _get_list(self):
        query_params = parse_querystring(request)
        if 'filters' in query_params:
            filters_dict = self._get_filter_dict(query_params['filters'])
            return self.model.query.filter_by(**filters_dict).all()
        return super()._get_list()

    def bulk_edit(self, *args, **kwargs):
        data = json.loads(self._get_request_data())
        if bulk_update_product_validator(data):
            self.model.query.filter(self.model.id.in_(data['ids'])).update(
                {**data['fields']},
                synchronize_session=False
            )
            db.session.commit()
            return jsonify(data['ids']), 200
        else:
            return jsonify(bulk_update_product_validator.errors), 400

    def reserve_product(self, id, *args, **kwargs):
        data = json.loads(self._get_request_data())
        if reserve_product_validator(data):
            object = self._get_object(id)
            if object.stocks >= data['stock_reserve']:
                self.model.query.filter(self.model.id == object.id).update(
                    {**data}
                )
                db.session.commit()
                return jsonify(object.to_dict()), 200
            else:
                return jsonify('Request reserving more than available'), 400
        else:
            return jsonify(reserve_product_validator.errors), 400

    def dispatch_request(self, *args, **kwargs):
        if self.EXTRA_ACTION_ARG in kwargs:
            extra_action = getattr(
                self, kwargs[self.EXTRA_ACTION_ARG].replace('-', '_').lower(),
                None
            )
            assert extra_action is not None, \
                "Unimplemented method %r" % kwargs[self.EXTRA_ACTION_ARG]
            return extra_action(*args, **kwargs)
        else:
            return super().dispatch_request(*args, **kwargs)
