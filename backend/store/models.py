from flask_sqlalchemy import SQLAlchemy

from backend.mixins import OutputMixin


db = SQLAlchemy()


class Category(db.Model, OutputMixin):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(1000),
        nullable=False,
        unique=True
    )
    products = db.relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Type(db.Model, OutputMixin):
    __tablename__ = 'product_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(1000),
        nullable=False,
        unique=True
    )
    products = db.relationship('Product', backref='type', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model, OutputMixin):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(1000),
        nullable=False,
        unique=True
    )
    sku = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )
    stocks = db.Column(db.Integer, default=0)
    stock_reserve = db.Column(db.Integer, default=0)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('product_category.id'),
        nullable=False
    )
    type_id = db.Column(
        db.Integer,
        db.ForeignKey('product_type.id'),
        nullable=False
    )
