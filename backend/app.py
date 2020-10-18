import os

from flask import Flask, render_template

from backend.store.models import db
from backend.store.views import CategoryAPI, TypeAPI, ProductAPI


def register_api(app, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(
        url,
        defaults={pk: None},
        view_func=view_func,
        methods=['GET', ]
    )
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule(
        '%s<%s:%s>' % (url, pk_type, pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )
    app.add_url_rule(
        '%s<%s:%s>/<string:extra_action>' % (url, pk_type, pk),
        view_func=view_func,
        methods=['PUT']
    )
    app.add_url_rule(
        '%s<string:extra_action>' % (url, ),
        view_func=view_func,
        methods=['PUT']
    )


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(os.getenv('APP_SETTINGS'))

    db.init_app(flask_app)
    with flask_app.test_request_context():
        db.create_all()

    register_api(
        flask_app,
        CategoryAPI,
        'category_api',
        '/api/categories/'
    )

    register_api(
        flask_app,
        TypeAPI,
        'type_api',
        '/api/types/'
    )

    register_api(
        flask_app,
        ProductAPI,
        'product_api',
        '/api/products/'
    )

    @flask_app.route('/docs')
    def get_docs():
        return render_template('swaggerui.html')

    return flask_app
