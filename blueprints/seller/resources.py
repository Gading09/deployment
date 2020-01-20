from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app, admin_required, seller_required
from blueprints.seller.model import Sellers
from blueprints.cart.model import Carts,Cartdetails
from blueprints.product.model import Products
from blueprints.transaction.model import Transactiondetails
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy

Bp_seller = Blueprint('seller',__name__)
api = Api(Bp_seller)

# CRUD seller GET, DELETE, PUT (accessed by seller)
class SellerResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )
    @jwt_required
    @seller_required
    # showing seller profile (himself)
    def get(self):
        claims = get_jwt_claims()
        qry = Sellers.query.filter_by(id = claims['id']).first()
        if qry.deleted == False:
            return marshal(qry, Sellers.response_fields), 200
        return {'message' : 'NOT_FOUND'}, 404

    @jwt_required
    @seller_required
    # delete seller account (himself)
    def delete(self):
        claims = get_jwt_claims()
        qry = Sellers.query.filter_by(id = claims['id']).first()
        if qry.deleted:
            return {'message':'NOT_FOUND'}, 404

        qry.deleted = True
        db.session.commit()
        
        # cart = Carts.query.filter_by(id_seller = claims['id']).all()
        # if cart is not None:
        #     for each_cart in cart:
        #         db.session.delete(each_cart)
        #         db.session.commit()

        # cart_cartdetails = Cartdetails.query.filter(id_cart = cart.id).all()
        # if cart_cartdetails[0] is not None:
        #     for each_cart_cartdetails in cart_cartdetails:
        #         db.session.delete(each_cart_cartdetails)
        #         db.session.commit()
        
        # cart_transaction_detail = Transactiondetails.query.filter_by(id_cart = cart.id).all()
        # if cart_transaction_detail[0] is not None:
        #     for each_cart_transaction_detail in cart_transaction_detail:
        #         db.session.delete(each_cart_transaction_detail)
        #         db.session.commit()

        # product = Products.query.filter_by(id_seller = claims['id']).all()
        # if product[0] is not None:
        #     for each_transaction in product:
        #         db.session.delete(each_transaction)
        #         db.session.commit()

        # product_cart_details = Cartdetails.query.filterby(id_product = product.id).all()
        # if product_cart_details[0] is not None:
        #     for each_product_cart_details in product_cart_details:
        #         db.session.delete(each_product_cart_details)
        #         db.session.commit()
        return {"message": "Deleted"},200

    @jwt_required
    @seller_required
    # edit seller account (himself)
    def put(self):
        claims = get_jwt_claims()
        qry = Sellers.query.filter_by(id = claims['id']).first()
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json')
        parser.add_argument('password', location = 'json')
        parser.add_argument('shop_name', location = 'json')
        parser.add_argument('fullname_owner', location = 'json')
        parser.add_argument('number_phone', location = 'json')
        parser.add_argument('address', location = 'json')
        parser.add_argument('email', location = 'json')
        parser.add_argument('gender', location = 'json', help = "Invalid input", choices=('Male', 'Female'))
        parser.add_argument('city', location = 'json')
        parser.add_argument('image', location = 'json')
        parser.add_argument('company', location = 'json', type = inputs.boolean)

        args = parser.parse_args()

        if qry.deleted:
            return{'message' : 'NOT_FOUND'}, 404
        if args ['username'] is not None:
            qry.username = args['username']
        if args['password'] is not None:
            validation = self.policy.test(args['password'])
            if validation:
                errorList = []
                for item in validation:
                    split = str(item).split('(')
                    error, num = split[0], split[1][0]
                    errorList.append("{err}(minimum {num})".format(err=error, num=num))
                message = "Please check your password: " + ', '.join(x for x in errorList)
                return {'message': message}, 422, {'Content-Type': 'application/json'}
            encrypted = hashlib.md5(args['password'].encode()).hexdigest()
            qry.password = encrypted
        if args['shop_name'] is not None:
            qry.shop_name = args['shop_name']
        if args['fullname_owner'] is not None:
            qry.fullname_owner = args['fullname_owner']
        if args['number_phone'] is not None:
            qry.number_phone = args['number_phone']
        if args['address'] is not None:
            qry.address = args['address']
        if args['email'] is not None:
            qry.email = args['email']
        if args['gender'] is not None:
            qry.gender = args['gender']
        if args['city'] is not None:
            qry.city = args['city']
        if args['image'] is not None:
            qry.image = args['image']
        if args['company'] is not None:
            qry.company = args['company']

        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error in Database!'}, 400
        return marshal(qry, Sellers.response_fields), 200

#CRUD seller POST (accessed by seller)
class RegisterSellerResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200
    # to keep the password secret
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    # create seller account
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('shop_name', location = 'json', required = True)
        parser.add_argument('fullname_owner', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('address', location = 'json', required = True)
        parser.add_argument('number_phone', location = 'json', required = True)
        args = parser.parse_args()
        
        validation = self.policy.test(args['password'])
        if validation:
            errorList = []
            for item in validation:
                split = str(item).split('(')
                error, num = split[0], split[1][0]
                errorList.append("{err}(minimum {num})".format(err=error, num=num))
            message = "Please check your password: " + ', '.join(x for x in errorList)
            return {'message': message}, 422, {'Content-Type': 'application/json'}
        encrypted = hashlib.md5(args['password'].encode()).hexdigest()
        
        seller = Sellers(args['username'], encrypted, args['shop_name'], args['fullname_owner'], args['email'], args['address'], args['number_phone'], "seller")
        db.session.add(seller)
        db.session.commit()
        app.logger.debug('DEBUG : %s', seller)
        
        return {'message' : "registration success !!!"},200,{'Content-Type': 'application/json'}


#CRUD seller GET (accessed by admin)
class GetSellersAdmin(Resource):
    @jwt_required
    @admin_required
    # showing all agent account
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('id', location = 'args')
        parser.add_argument('shop_name', location = 'args')
        parser.add_argument('username', location = 'args')
        parser.add_argument('city', location = 'args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Sellers.query

        if args['id'] is not None:
            qry = qry.filter_by(id = args['id'])

        if args['shop_name'] is not None:
            qry = qry.filter_by(shop_name = args['shop_name'])

        if args['username'] is not None:
            qry = qry.filter_by(username = args['username'])
        
        if args['city'] is not None:
            qry = qry.filter_by(city = args['city'])
        
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Sellers.response_fields))
        return rows, 200

#CRUD seller DELETE (accessed by admin)
class DeleteSellersAdmin(Resource):
    @jwt_required
    @admin_required
    # delete agent account with filter by id or username
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args')
        parser.add_argument('username', location = 'args')

        args = parser.parse_args()

        if (args['id'] is not None) and (args['username'] is not None):
            return {'message':'Please, just enter one'}, 404
        
        elif args['id'] is not None:
            qry = Sellers.query.filter_by(id = args['id']).first()

        elif args['username'] is not None:
            qry = Sellers.query.filter_by(username = args['username']).first()

        if qry.deleted:
            return {'message':'NOT_FOUND'}, 404

        qry.deleted = True
        db.session.commit()
        
        # cart = Carts.query.filter_by(id_seller = args['id']).all()
        # if cart is not None:
        #     for each_cart in cart:
        #         db.session.delete(each_cart)
        #         db.session.commit()

        # cart_cartdetails = Cartdetails.query.filter(id_cart = cart.id).all()
        # if cart_cartdetails[0] is not None:
        #     for each_cart_cartdetails in cart_cartdetails:
        #         db.session.delete(each_cart_cartdetails)
        #         db.session.commit()
        
        # cart_transaction_detail = Transactiondetails.query.filter_by(id_cart = cart.id).all()
        # if cart_transaction_detail[0] is not None:
        #     for each_cart_transaction_detail in cart_transaction_detail:
        #         db.session.delete(each_cart_transaction_detail)
        #         db.session.commit()

        # product = Products.query.filter_by(id_seller = args['id']).all()
        # if product[0] is not None:
        #     for each_transaction in product:
        #         db.session.delete(each_transaction)
        #         db.session.commit()

        # product_cart_details = Cartdetails.query.filterby(id_product = product.id).all()
        # if product_cart_details[0] is not None:
        #     for each_product_cart_details in product_cart_details:
        #         db.session.delete(each_product_cart_details)
        #         db.session.commit()
        return {"message": "Deleted"},200

#CRUD seller PUT (accessed by admin)
class ActivatedSellerAdmin(Resource):
    @jwt_required
    @admin_required
    # Activate agent account with filter by id or username
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args')
        parser.add_argument('username', location = 'args')

        args = parser.parse_args()

        if (args['id'] is not None) and (args['username'] is not None):
            return {'message':'Please, just enter one'}, 404
        
        elif args['id'] is not None:
            qry = Sellers.query.filter_by(id = args['id']).first()

        elif args['username'] is not None:
            qry = Sellers.query.filter_by(username = args['username']).first()

        if qry.deleted == False:
            return {'message':'This account is still active!'}, 404

        qry.deleted = False
        db.session.commit()
        return {"message": "Activated"},200

api.add_resource(SellerResource,'/seller')
api.add_resource(RegisterSellerResource,'/seller/registration')
api.add_resource(GetSellersAdmin,'/admin/get/seller')
api.add_resource(DeleteSellersAdmin,'/admin/delete/seller')
api.add_resource(ActivatedSellerAdmin,'/admin/activate/seller')