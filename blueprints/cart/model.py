from blueprints import db
from flask_restful import fields
import datetime

class Carts(db.Model):
    __tablename__ = "Cart"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_user = db.Column(db.Integer, db.ForeignKey("User.id", ondelete = 'CASCADE'), nullable = False)
    id_seller = db.Column(db.Integer, db.ForeignKey("Seller.id", ondelete = 'CASCADE'), nullable = False)
    price_cart = db.Column(db.Integer, nullable = False, default = 0)
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())

    response_fields = {
        'id' : fields.Integer,
        'id_user' : fields.Integer,
        'id_seller' : fields.Integer, 
        'price_cart' : fields.Integer,
        'deleted' : fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_user, id_seller):
        self.id_user = id_user
        self.id_seller = id_seller

    def __repr__(self):
        return '<Cart %r>' %self.id

class Cartdetails(db.Model):
    __tablename__ = "Cartdetail"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_cart = db.Column(db.Integer, db.ForeignKey("Cart.id", ondelete = 'CASCADE'), nullable = False)
    id_product = db.Column(db.Integer, db.ForeignKey("Product.id", ondelete = 'CASCADE'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False, default = 1)
    deleted = db.Column(db.Boolean, nullable = False, default = False)

    response_fields = {
        'id' : fields.Integer,
        'id_cart' : fields.Integer,
        'id_product' : fields.Integer,
        'quantity' : fields.Integer,
        'deleted' : fields.Boolean
    }

    def __init__(self, id_cart, id_product):
        self.id_cart = id_cart
        self.id_product = id_product

    def __repr__(self):
        return '<Cartdetail %r>' %self.id