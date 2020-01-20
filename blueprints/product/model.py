from blueprints import db
from flask_restful import fields
import datetime

class Products(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_seller = db.Column(db.Integer, db.ForeignKey("Seller.id", ondelete = 'CASCADE'), nullable = False)
    name_product = db.Column(db.String(255), nullable = False, default = "")
    description = db.Column(db.String(255), nullable = False, default = "")
    rating = db.Column(db.Integer, nullable = False, default = 0)
    weight = db.Column(db.Integer, nullable = False, default = 0)
    price = db.Column(db.Integer, nullable = False, default = 0)
    reference = db.Column(db.String(16), nullable = False, default = "")
    stock = db.Column(db.Integer, nullable = False, default = 0)
    halal = db.Column(db.Boolean, nullable = False, default = False)
    taste = db.Column(db.String(16), nullable = False, default = "")
    sold = db.Column(db.Integer, nullable = False, default = 0)
    image = db.Column(db.String(255), nullable = False, default = "")
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())

    response_fields = {
        'id' : fields.Integer,
        'id_seller' : fields.Integer,
        'name_product' : fields.String,
        'description' : fields.String,
        'rating' : fields.Integer,
        'weight' : fields.Integer,
        'price' : fields.Integer,
        'reference' : fields.String,
        'stock' : fields.String,
        'halal' : fields.Boolean,
        'taste' : fields.String,
        'sold' : fields.Integer,
        'image' : fields.String,
        'deleted': fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }


    def __init__(self, id_seller, name_product , description, weight, price, reference, stock, halal, taste, image):
        self.id_seller = id_seller
        self.name_product = name_product
        self.description = description
        self.weight = weight
        self.price = price
        self.reference = reference
        self.stock = stock
        self.halal = halal
        self.taste = taste
        self.image = image

    def __repr__(self):
        return '<Product %r>' %self.id