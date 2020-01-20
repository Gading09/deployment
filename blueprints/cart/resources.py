from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app, admin_required, user_required, agent_required
from blueprints.cart.model import Carts, Cartdetails
from blueprints.user.model import Users
from blueprints.product.model import Products
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy

Bp_cart = Blueprint('cart',__name__)
api = Api(Bp_cart)

class AddCartUser(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @user_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()

        parser.add_argument('id_product', location = 'json', required = True)
        args = parser.parse_args()

        qry_product = Products.query.get(args['id_product'])
        id_seller = qry_product.id_seller
        qry_cart = Carts.query.filter_by(deleted = False).filter_by(id_user = claims['id']).filter_by(id_seller = id_seller).first()
        if qry_cart is None:
            cart = Carts(claims["id"],id_seller)
            db.session.add(cart)
            db.session.commit()

            qry_cart = Carts.query.filter_by(deleted = False).filter_by(id_user = claims['id']).filter_by(id_seller = id_seller).first()
            cart_detail = Cartdetails(qry_cart.id,args['id_product'])
            db.session.add(cart_detail)
            db.session.commit()
            qry_cartdetail = Cartdetails.query.filter_by(id_cart = qry_cart.id).filter_by(id_product = args['id_product']).first()
        
        else:
            qry_cartdetail = Cartdetails.query.filter_by(id_cart = qry_cart.id).filter_by(id_product = args['id_product']).first()
            if qry_cartdetail is None:
                cart_detail = Cartdetails(qry_cart.id,args['id_product'])
                db.session.add(cart_detail)
                db.session.commit()
                qry_cartdetail = Cartdetails.query.filter_by(id_cart = qry_cart.id).filter_by(id_product = args['id_product']).first()
            else:
                qry_cartdetail.quantity += 1
                db.session.commit()

        qry_cart = Carts.query.filter_by(deleted = False).filter_by(id_user = claims["id"])
        for each_cart in qry_cart:
            price_cart = 0
            id_cart = each_cart.id
            qry_cart_detail = Cartdetails.query.filter_by(deleted = False).filter_by(id_cart = id_cart)
            for each_product in qry_cart_detail:
                qry_product = Products.query.get(each_product.id_product)
                price_cart += qry_product.price * each_product.quantity
            each_cart.price_cart = price_cart
            db.session.commit()

        # app.logger.debug('DEBUG : %s', cart)
        
        return {'message' : "add product success !!!"},200,{'Content-Type': 'application/json'}


class ShowCart(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200
    @jwt_required
    @user_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Carts.query        
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Carts.response_fields))
        return rows, 200
        
class ShowCartDetail(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200
    @jwt_required
    @user_required
    def get(self,id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 50)

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Cartdetails.query.filter_by(id_cart = id)
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                id_product = row.id_product
                qry_product = Products.query.get(id_product)
                marshal_product = marshal(qry_product, Products.response_fields)
                marshal_cartdetail = marshal(row, Cartdetails.response_fields)
                marshal_cartdetail['id_product'] = marshal_product
                rows.append(marshal_cartdetail)
        return rows, 200

api.add_resource(AddCartUser,'/user/cart')
api.add_resource(ShowCartDetail,'/cart/detail','/cart/detail/<int:id>')
api.add_resource(ShowCart,'/cart')