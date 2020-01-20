from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app, admin_required, user_required
from blueprints.user.model import Users
from blueprints.cart.model import Carts, Cartdetails
from blueprints.transaction.model import Trasactions, Transactiondetails

from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy

Bp_transaction = Blueprint('transaction',__name__)
api = Api(Bp_transaction)

class AddTransaction(Resource):
    def options(self,id=None):
        return{'status':'ok'} , 200
        
    @jwt_required
    @user_required
    def post(self):
        parser = reqparse.RequestParser()
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('payment', location = 'json', required = True)

        args = parser.parse_args()
        qry_trans = Trasactions.query.filter_by(id_user = claims['id']).filter_by(paid_off = False).first()
        if qry_trans is None:
            print("masuk True")
            if args['payment'] == 'OVO':
                transaction = Trasactions(claims['id'], args['payment'], 2000)
            elif args['payment'] == 'GoPay':
                transaction = Trasactions(claims['id'], args['payment'], 2500)
            elif args['payment'] == 'LinkAja':
                transaction = Trasactions(claims['id'], args['payment'], 5000)
            db.session.add(transaction)
            db.session.commit()

            qry_cart = Carts.query.filter_by(deleted = False).filter_by(id_user = claims['id'])
        
            total_price = 0
            for each_cart in qry_cart:
                total_price += each_cart.price_cart
                transaction__detail = Transactiondetails(transaction.id,each_cart.id)
                db.session.add(transaction__detail)
                db.session.commit()
            transaction.total_price = total_price
            transaction.paid_price = total_price + transaction.shipping
            qry_trans.total_price = transaction.total_price
            qry_trans.paid_price = transaction.paid_price
            qry_trans.shipping = transaction.shipping
            db.session.commit()
            print(transaction.shipping)
            print(total_price)


        else:
            print("masuk FALSE")
            qry_trans.payment = args['payment']
            db.session.commit()
            if args['payment'] == 'OVO':
                transaction = Trasactions(claims['id'], args['payment'],2000)
            elif args['payment'] == 'GoPay':
                transaction = Trasactions(claims['id'], args['payment'],2500)
            elif args['payment'] == 'LinkAja':
                transaction = Trasactions(claims['id'], args['payment'],5000)            
            qry_cart = Carts.query.filter_by(deleted = False).filter_by(id_user = claims['id'])
        
            total_price = 0
            for each_cart in qry_cart:
                total_price += each_cart.price_cart
            transaction.total_price = total_price
            transaction.paid_price = total_price + transaction.shipping
            qry_trans.total_price = transaction.total_price
            qry_trans.paid_price = transaction.paid_price
            qry_trans.shipping = transaction.shipping
            db.session.commit()

            print(transaction.shipping)
            print(total_price)
            print(transaction.paid_price)
            print(transaction.total_price)

            



        return {'message' : "add product success !!!"},200,{'Content-Type': 'application/json'}

class TransactionSuccses(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @user_required
    def put(self):
        claims = get_jwt_claims()
        qry_transaction = Trasactions.query.filter_by(paid_off = False).filter_by(id_user = claims['id']).first()
        qry_cart = Carts.query.filter_by(deleted = False).filter_by(id_user = claims['id']).all()
        parser = reqparse.RequestParser()

        args = parser.parse_args()

        qry_transaction.paid_off = True

        for each_cart in qry_cart:
            qry_cartdetail = Cartdetails.query.filter_by(deleted = False).filter_by(id_cart=each_cart.id).all()
            for each_cart_detail in qry_cartdetail:
                each_cart_detail.deleted = True
            each_cart.deleted = True

        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error in Database!'}, 400
        return {'message': 'Transaction Succses!'}, 200

class ShowTransaction(Resource):

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

        qry = Trasactions.query        
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.paid_off:
                rows.append(marshal(row, Trasactions.response_fields))
        return rows, 200


api.add_resource(AddTransaction,'/user/cart/transaction')
api.add_resource(TransactionSuccses,'/user/cart/checkout')
api.add_resource(ShowTransaction,'/user/transaction')