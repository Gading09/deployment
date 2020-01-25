from blueprints import db
from flask_restful import fields
import datetime
# coba
class Sellers(db.Model):
    __tablename__ = "Seller"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(30), unique = True, nullable = False, default = "")
    password = db.Column(db.String(255), nullable = False, default = "")
    shop_name = db.Column(db.String(255), nullable = False, default = "")
    fullname_owner = db.Column(db.String(255), nullable = False, default = "")
    number_phone = db.Column(db.Integer, nullable = False, default = 0)
    address = db.Column(db.String(255), nullable = False, default = "")
    email = db.Column(db.String(255), nullable = False, default = "")
    gender = db.Column(db.String(12), nullable = False, default = "")
    city = db.Column(db.String(255), nullable = False, default = "")
    role = db.Column(db.String(12), nullable = False, default = "")
    image = db.Column(db.String(255), nullable = False, default = "")
    company = db.Column(db.Boolean, nullable = False, default = False)
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())

    response_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'shop_name' : fields.String,
        'fullname_owner' : fields.String,
        'number_phone' : fields.Integer,
        'address' : fields.String,
        'email' : fields.String,
        'gender' : fields.String,
        'city' : fields.String,
        'role' : fields.String,
        'image' : fields.String,
        'company' : fields.Boolean, 
        'deleted': fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'role' : fields.String,
        'status_del' : fields.Boolean
    }

    def __init__(self, username, password, shop_name, fullname_owner, email, address, number_phone, role):
        self.username = username
        self.password = password
        self.shop_name = shop_name
        self.fullname_owner = fullname_owner
        self.email = email
        self.address = address
        self.number_phone = number_phone
        self.role = role

    def __repr__(self):
        return '<Seller %r>' %self.id