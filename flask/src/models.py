from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, TEXT, INTEGER
from marshmallow_sqlalchemy import ModelSchema

db = SQLAlchemy()
ma = Marshmallow()


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_m = db.Column(db.Integer, nullable=False)
    price_l = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    deleted = db.Column(db.Integer, nullable=False)


class ItemSchema(ModelSchema):
    class Meta:
        model = Item


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(1), nullable=False)
    # item_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, ForeignKey("items.id"))
    order_id = db.Column(db.Integer, ForeignKey("orders.id"), nullable=False)


class OrderItemSchema(ModelSchema):
    class Meta:
        model = OrderItem


class OrderTopping(db.Model):
    __tablename__ = 'order_toppings'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_item_id = db.Column(db.Integer, ForeignKey("order_items.id"), nullable=False)
    topping_id = db.Column(db.Integer, ForeignKey("toppings.id"), nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    destination_name = db.Column(db.String(100), nullable=False)
    destination_email = db.Column(db.String(100), nullable=False)
    destination_zipcode = db.Column(db.String(7), nullable=False)
    destination_address = db.Column(db.String(200), nullable=False)
    destination_tel = db.Column(db.String(15), nullable=False)
    delivery_time = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))

    order_items = db.relationship("OrderItem", backref='order')


class OrderSchema(ModelSchema):
    class Meta:
        model = Order

    order_items = fields.Nested(OrderItemSchema, many=True)


class Topping(db.Model):
    __tablename__ = 'toppings'

    id = db.Column(INTEGER(), primary_key=True, nullable=False)
    name = db.Column(TEXT(), nullable=False)
    price_m = db.Column(INTEGER(), nullable=False)
    price_l = db.Column(INTEGER(), nullable=False)


class UserUtil(db.Model):
    __tablename__ = 'user_utils'

    id = db.Column(INTEGER(), primary_key=True, nullable=False)
    token = db.Column(TEXT(), nullable=False)
    created_at = db.Column(DATETIME(), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    zipcode = db.Column(db.String(7), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(1), nullable=False)
