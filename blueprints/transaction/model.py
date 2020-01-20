from blueprints import db
from flask_restful import fields
import datetime

class Trasactions(db.Model):
    __tablename__ = "Transaction"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_user = db.Column(db.Integer, db.ForeignKey("User.id", ondelete = 'CASCADE'), nullable = False)
    payment = db.Column(db.String(255), nullable = False, default = "")
    shipping = db.Column(db.Integer, nullable = False, default = 0)
    total_price = db.Column(db.Integer, nullable = False, default = 0)
    paid_price = db.Column(db.Integer, nullable = False, default = 0)
    paid_off = db.Column(db.Boolean, nullable = False, default = False)

    response_fields = {
        'id' : fields.Integer,
        'id_user' : fields.Integer,
        'payment' : fields.String,
        'shipping' : fields.Integer,
        'total_price' : fields.Integer,
        'paid_price' : fields.Integer,
        'paid_off' : fields.Boolean
    }

    def __init__(self, id_user, payment, shipping):
        self.id_user = id_user
        self.payment = payment
        self.shipping = shipping

    def __repr__(self):
        return '<Transaction %r>' %self.id

class Transactiondetails(db.Model):
    __tablename__ = "Transactiondetail"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_transaction = db.Column(db.Integer, db.ForeignKey("Transaction.id", ondelete = 'CASCADE'), nullable = False)
    id_cart = db.Column(db.Integer, db.ForeignKey("Cart.id", ondelete = 'CASCADE'), nullable = False)


    response_fields = {
        'id' : fields.Integer,
        'id_transaction' : fields.Integer,
        'id_cart' : fields.Integer
    }

    def __init__(self, id_transaction, id_cart):
        self.id_transaction = id_transaction
        self.id_cart = id_cart

    def __repr__(self):
        return '<Transactiondetail %r>' %self.id