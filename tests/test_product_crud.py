import pytest, logging
from . import app, cache, create_token, client, reset_db
from flask import Flask, request, json
from flask_jwt_extended import get_jwt_claims
import hashlib

class TestUserCrud():
    def test_get_product_id(self, client):
        reset_db()
        token = create_token("seller")
        data = {
            "p" : 1,
            "rp" : 25,
            "name_product" :"palu",
            "halal" : True,
            "taste" : "sweet"
        }
        res = client.get('/seller/product',query_string = data, headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
      
    # def test_get_agent_id(self, client):
    #     reset_db()
    #     token = create_token("agent")
    #     res = client.get('/agent', headers={'Authorization': 'Bearer '+token})
    #     assert res.status_code==200

    def test_put_user(self, client):
        reset_db()
        token = create_token("seller")
        data = {
            'id_seller' : "1",
            'nama_product': 'kapak',
            'description' : "hoho",
            'weight' : 70,
            "price" : 100,
            "reference" : "wrap",
            "stock" : 17,
            "halal" : True,
            "tasty" : "sweet"
        }
        res = client.put('/seller/product', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200
    
    def test_del_user__invalid(self, client):
        reset_db()
        token = create_token("seller")
        res = client.delete('/seller/product', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200

    def test_get_agent(self,client):
        reset_db()
        token = create_token("user")
        data = {
            "rating" : 5
        }
        res = client.put('/user/product/rating/1', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200

    def test_post_product(self, client):
        reset_db()
        token = create_token("seller")
        data = {
            'nama_product': 'kapak',
            'description' : "hoho",
            'weight' : 70,
            "price" : 100,
            "reference" : "wrap",
            "stock" : 17,
            "halal" : True,
            "tasty" : "sweet"
        }
        res = client.post('/seller/product/create', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200
