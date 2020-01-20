from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app, admin_required, user_required, agent_required
from blueprints.user.model import Users
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy

Bp_review = Blueprint('review',__name__)
api = Api(Bp_review)

# CRUD user PUT (accessed by user)
class CreateUserReview(Resource):

    @jwt_required
    @user_required
    # showing user profile (himself)
    def put(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        parser = reqparse.RequestParser()
        parser.add_argument('rating', location = 'json')
        parser.add_argument('review', location = 'json')

        args = parser.parse_args()

        if qry.deleted:
            return{'message' : 'NOT_FOUND'}, 404
        if args['rating'] is not None:
            qry.rating = args['rating']
        if args['review'] is not None:
            qry.review = args['review']
        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error in Database!'}, 400
        return {'id': qry.id, 'rating' : qry.rating, 'review' : qry.review}, 200 ,{'Content-Type': 'application/json'}


# CRUD agent PUT (accessed by agent)
class CreateAgentReview(Resource):

    @jwt_required
    @agent_required
    # showing user profile (himself)
    def put(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        parser = reqparse.RequestParser()
        parser.add_argument('rating', location = 'json')
        parser.add_argument('review', location = 'json')

        args = parser.parse_args()

        if qry.deleted:
            return{'message' : 'NOT_FOUND'}, 404
        if args['rating'] is not None:
            qry.rating = args['rating']
        if args['review'] is not None:
            qry.review = args['review']
        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error in Database!'}, 400
        return {'id': qry.id, 'rating' : qry.rating, 'review' : qry.review}, 200 ,{'Content-Type': 'application/json'}


# CRUD user and agent GET (accessed by admin)
class ReviewUserAgent(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200
    # showing user profile (himself)
    def get(self):
        qry_user = Users.query.filter_by(role = "user").filter_by(rating = 5).first()
        qry_agent = Users.query.filter_by(role = "agent").filter_by(rating = 5).first()
        if qry_user is None:
            qry_user = Users.query.filter_by(role = "user").filter_by(rating = 4).first()
        if qry_agent is None:
            qry_agent = Users.query.filter_by(role = "agent").filter_by(rating = 4).first()
        else:
            return {'message': 'Integrity Error in Database!'}, 400
        output = {
            'image_user' : qry_user.image,
            'nama_user' : qry_user.fullname,
            'rating_user' : qry_user.rating,
            'review_user' : qry_user.review,
            'image_agent' : qry_agent.image,
            'nama_agent' : qry_agent.fullname,
            'rating_agent' : qry_agent.rating,
            'review_agent' : qry_agent.review
        }
        return output, 200,{'Content-Type': 'application/json'}

api.add_resource(CreateUserReview,'/user/review')
api.add_resource(CreateAgentReview,'/agent/review')
api.add_resource(ReviewUserAgent,'/review')