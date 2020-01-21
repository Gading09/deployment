import json, os
from flask_cors import CORS
from datetime import timedelta
from functools import wraps

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

app = Flask(__name__)

app.config['APP_DEBUG']=True
CORS(app)
# ========================================
# ==================JWT===================
# ========================================

app.config['JWT_SECRET_KEY'] = 'JWjs924bG9epW02LsqwZaM309QL1tW31'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['isinternal'] == False:
            return {'status': 'FORBIDDEN', 'message' : 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == "user":
            return fn(*args, **kwargs)
        else:
            return {'status': 'FORBIDDEN', 'message' : 'user doesn\'t get access!'}, 403
    return wrapper

def agent_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == "agent":
            return fn(*args, **kwargs)
        else:
            return {'status': 'FORBIDDEN', 'message' : 'agent doesn\'t get access!'}, 403
    return wrapper

def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == "seller":
            return fn(*args, **kwargs)
        else:
            return {'status': 'FORBIDDEN', 'message' : 'seller doesn\'t get access!'}, 403
    return wrapper
    
# =========================================
# ================DATABASE=================
# =========================================

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/Project_Restful_API'
try :
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0/Project_Backend_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@alta.cyjqq86bpzjh.ap-southeast-1.rds.amazonaws.com/Project_Backend'
except Exception as e :
    raise e

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# ======================================
# =========IMPORT BLUEPRINT=============
# ======================================

from blueprints.auth import bp_auth
app.register_blueprint(bp_auth,url_prefix = '')

from blueprints.cart.resources import Bp_cart
app.register_blueprint(Bp_cart,url_prefix = '')

from blueprints.product.resources import Bp_product
app.register_blueprint(Bp_product,url_prefix = '')

from blueprints.review import Bp_review
app.register_blueprint(Bp_review,url_prefix = '')

from blueprints.seller.resources import Bp_seller
app.register_blueprint(Bp_seller,url_prefix = '')

from blueprints.transaction.resources import Bp_transaction
app.register_blueprint(Bp_transaction,url_prefix = '')

from blueprints.user.resources import Bp_user
app.register_blueprint(Bp_user,url_prefix = '')

db.create_all()

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()

    log = {
        'status_code':response.status_code,
        'method':request.method,
        'code':response.status,
        'uri':request.full_path,
        'request': requestData, 
        'response': json.loads(response.data.decode('utf-8'))
    }

    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps(log))
    elif response.status_code >= 400:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps(log))
    
    return response
