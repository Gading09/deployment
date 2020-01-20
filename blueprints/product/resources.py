from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app, admin_required, seller_required, agent_required, user_required
from blueprints.seller.model import Sellers
from blueprints.product.model import Products
from blueprints.cart.model import Cartdetails
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy

Bp_product = Blueprint('product',__name__)
api = Api(Bp_product)

# CRUD product GET, DELETE, PUT (accessed by seller)
class ProductResource(Resource):

    @jwt_required
    @seller_required
    # showing product profile (himself)
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('name_product', location = 'args')
        parser.add_argument('halal', location = 'args', type = inputs.boolean)
        parser.add_argument('taste', location = 'args', help = "Invalid input", choices=('salty', 'sweet','sour','spicy'))

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Products.query.filter_by(id_seller = claims['id'])

        if args['name_product'] is not None:
            qry = qry.filter_by(name_product = args['name_product'])

        if args['halal'] is not None:
            qry = qry.filter_by(halal = args['halal'])
        
        if args['taste'] is not None:
            qry = qry.filter_by(taste = args['taste'])
        
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Products.response_fields))
        return rows, 200

    @jwt_required
    @seller_required
    # delete product (himself)
    def delete(self):
        claims = get_jwt_claims()
        qry = Products.query.filter_by(id_seller = claims['id']).first()
        if qry.deleted:
            return {'message':'NOT_FOUND'}, 404

        qry.deleted = True
        db.session.commit()
        
        # product_cart_details = Cartdetails.query.filterby(id_product = qry.id).all()
        # if product_cart_details[0] is not None:
        #     for each_product_cart_details in product_cart_details:
        #         db.session.delete(each_product_cart_details)
        #         db.session.commit()
        return {"message": "Deleted"},200

    @jwt_required
    @seller_required
    # edit product account (himself)
    def put(self,id=None):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id_seller', location = 'json')
        parser.add_argument('name_product', location = 'json')
        parser.add_argument('description', location = 'json')
        parser.add_argument('weight', location = 'json')
        parser.add_argument('price', location = 'json')
        parser.add_argument('reference', location = 'json', help = "Invalid input", choices=("cardboard","wrap"))
        parser.add_argument('stock', location = 'json')
        parser.add_argument('halal', location = 'json', type = inputs.boolean)
        parser.add_argument('tasty', location = 'json', help = "Invalid input", choices=('salty', 'sweet','sour','spicy'))
        parser.add_argument('image', location = 'json')
        args = parser.parse_args()

        qry = Products.query.get(id)

        if qry.deleted:
            return{'message' : 'NOT_FOUND'}, 404
        if args ['id_seller'] is not None:
            qry.id_seller = args['id_seller']
        if args['name_product'] is not None:
            qry.name_product = args['name_product']
        if args['description'] is not None:
            qry.description = args['description']
        if args['weight'] is not None:
            qry.weight = args['weight']
        if args['price'] is not None:
            qry.price = args['price']
        if args['reference'] is not None:
            qry.reference = args['reference']
        if args['stock'] is not None:
            qry.stock = args['stock']
        if args['halal'] is not None:
            qry.halal = args['halal']
        if args['tasty'] is not None:
            qry.tasty = args['tasty']
        if args['image'] is not None:
            qry.image = args['image']

        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error in Database!'}, 400
        return marshal(qry, Products.response_fields), 200

# CRUD product PUT (accessed by user)
class GiveRatingProduct(Resource):
    @jwt_required
    @user_required
    # edit product rating by user after selling
    def put(self,id=None):
        claims = get_jwt_claims()
        qry = Products.query.get(id)
        parser = reqparse.RequestParser()
        parser.add_argument('rating', location = 'json')


        args = parser.parse_args()

        if qry.deleted:
            return{'message' : 'NOT_FOUND'}, 404
        if args ['rating'] is not None:
            qry.rating = args['rating']

        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error in Database!'}, 400
        return marshal(qry, Products.response_fields), 200

#CRUD product POST (accessed by seller)
class CreateProductResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200
    @jwt_required
    @seller_required
    # create product
    def post(self):
        parser = reqparse.RequestParser()
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name_product', location = 'json', required = True)
        parser.add_argument('description', location = 'json', required = True)
        parser.add_argument('weight', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        parser.add_argument('reference', location = 'json', required = True, help = "Invalid input", choices=("cardboard","wrap"))
        parser.add_argument('stock', location = 'json', required = True)
        parser.add_argument('halal', location = 'json', type = inputs.boolean, required = True)
        parser.add_argument('taste', location = 'json', required = True, help = "Invalid input", choices=('salty','sweet','sour','spicy'))
        parser.add_argument('image', location = 'json', required = True)        
        
        args = parser.parse_args()
        
        product = Products(claims['id'], args['name_product'], args['description'], args['weight'], args['price'], args['reference'], args['stock'], args['halal'], args['taste'], args['image'])
        db.session.add(product)
        db.session.commit()
        app.logger.debug('DEBUG : %s', product)
        
        return {'message' : "add product success !!!"},200,{'Content-Type': 'application/json'}


#CRUD product GET (accessed by public)
class GetProductPublic(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200
    # showing all product
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('name_product', location = 'args')
        parser.add_argument('halal', location = 'args', type = inputs.boolean)
        parser.add_argument('taste', location = 'args', help = "Invalid input", choices=('salty', 'sweet','sour','spicy'))

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Products.query

        if args['name_product'] is not None:
            qry = qry.filter_by(name_product = args['name_product'])

        if args['halal'] is not None:
            qry = qry.filter_by(halal = args['halal'])
        
        if args['taste'] is not None:
            qry = qry.filter_by(taste = args['taste'])
        
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Products.response_fields))
        return rows, 200

class GetProductPubli(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('keyword', location = 'args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Products.query.filter(Products.name_product.like("%"+args["keyword"]+"%") | Products.reference.like("%"+args["keyword"]+"%") | Products.taste.like("%"+args["keyword"]+"%"))
        
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Products.response_fields))
        return rows, 200


#CRUD product GET (accessed by public)
class GetByOneProductPublic(Resource):

    # showing product
    def get(self,id=None):
        qry = Products.query.get(id)
        id_seller = qry.id_seller
        qry_seller = Sellers.query.get(id_seller)
        marshal_seller = (marshal(qry_seller, Sellers.response_fields))
        print(marshal_seller)
        marshal_qry = (marshal(qry, Products.response_fields))
        marshal_qry['id_seller'] = marshal_seller

        if qry is not None:
            if not qry.deleted:
                return marshal_qry, 200
        return {'message' : 'NOT_FOUND'}, 404

#CRUD product DELETE (accessed by admin)
class DeleteProductAdmin(Resource):
    @jwt_required
    @admin_required
    # delete agent account with filter by id or username
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args')

        args = parser.parse_args()
        
        if args['id'] is not None:
            qry = Products.query.filter_by(id = args['id']).first()

        if qry.deleted:
            return {'message':'NOT_FOUND'}, 404

        qry.deleted = True
        db.session.commit()
        
        # product_cart_details = Cartdetails.query.filter_by(id_product = args['id']).all()
        # if product_cart_details[0] is not None:
        #     for each_product_cart_details in product_cart_details:
        #         db.session.delete(each_product_cart_details)
        #         db.session.commit()
 
        return {"message": "Deleted"},200

#CRUD product PUT (accessed by admin)
class ActivatedProductAdmin(Resource):
    @jwt_required
    @admin_required
    # Activate agent account with filter by id or username
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args')

        args = parser.parse_args()
        
        if args['id'] is not None:
            qry = Products.query.filter_by(id = args['id']).first()

        if qry.deleted == False:
            return {'message':'This account is still active!'}, 404

        qry.deleted = False
        db.session.commit()
        return {"message": "Activated"},200

api.add_resource(ProductResource,'/seller/product','/seller/product/<int:id>')
api.add_resource(GiveRatingProduct,'/user/product/rating/<id>')
api.add_resource(CreateProductResource,'/seller/product/create')
api.add_resource(GetProductPublic,'/public/product')
api.add_resource(GetProductPubli,'/public/product/search')
api.add_resource(GetByOneProductPublic,'/public/product/<id>')
api.add_resource(DeleteProductAdmin,'/admin/delete/product')
api.add_resource(ActivatedProductAdmin,'/admin/activate/product')