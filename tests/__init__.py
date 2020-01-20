import pytest, logging, hashlib
from app import app, cache
from blueprints import db
from blueprints.user.model import Users
from blueprints.seller.model import Sellers
from blueprints.product.model import Products
from flask import Flask, request, json

def reset_db():
    db.drop_all()
    db.create_all()
    password = hashlib.md5('Hedyy1'.encode()).hexdigest()
    user = Users('TEST', password, "hahaha", "hehe", "alamat", 12345, "user")
    user.image = "lian"
    db.session.add(user)
    user = Users('TEST1', password, "hahaha", "hehe", "alamat", 12345, "user")
    db.session.add(user)
    agent = Users("Agent", password,"hahaha", "hehe", "alamat", 12345, "agent")
    agent.image = "bambamb"
    db.session.add(agent)
    agent = Users("Agent1", password,"hahaha", "hehe", "alamat", 12345, "agent")
    db.session.add(agent)
    seller= Sellers("seller",password,"kuda","ok","ok","ok", 1234,"seller")
    db.session.add(seller)
    db.session.commit()
    product = Products(seller.id,"makanan","makanan",70,100,"wrap",3,True,"sweet")
    db.session.add(product)
    db.session.commit()


def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(role):
    if role == "user":
        cachename = 'test-token-user'
        data = {
            'username': 'TEST',
            'password': "Hedyy1"
        }
    elif role == "agent":
        cachename = 'test-token-agent'
        data = {
            'username': 'Agent',
            'password': "Hedyy1"
        }
    elif role == "seller":
        cachename = 'test-token-seller'
        data = {
            'username': 'Seller',
            'password': "Hedyy1"
        }
    elif role == "ok":
        cachename = 'test-token-admin'
        data = {
            'username': 'admin',
            'password': "admin"
        }
    token = cache.get(cachename)
    if token is not None:
        return token
    req = call_client(request)
    res = req.get('/login', query_string=data)
    resjson = json.loads(res.data)
    logging.warning('RESULT: %s', resjson)
    assert res.status_code==200
    cache.set(cachename, resjson['token'], timeout=60)
    return resjson['token']