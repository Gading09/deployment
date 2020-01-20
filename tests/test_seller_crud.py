import pytest, logging
from . import app, cache, create_token, client, reset_db
from flask import Flask, request, json
from flask_jwt_extended import get_jwt_claims
import hashlib

class TestUserCrud():
    def test_get_seller_id(self, client):
        reset_db()
        token = create_token("seller")
        res = client.get('/seller', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
      
    def test_put_seller(self, client):
        reset_db()
        token = create_token("seller")
        data = {
            'username' : "TEST",
            'password': 'Uedyy1',
            'shop_name' : "oka",
            'fullname_owner' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu",
            "company" : True
        }
        res = client.put('/seller', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200
    
    def test_del_user_id_invalid(self, client):
        reset_db()
        token = create_token("seller")
        res = client.delete('/seller', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
        
    def test_post_user(self, client):
        reset_db()
        token = create_token("seller")
        data = {
            'username' : "TEST",
            'password': 'Uedyy1',
            'shop_name' : "oka",
            'fullname_owner' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi"
        }
        res = client.post('/seller/registration', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200

    def test_get_admin_user_id(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            'p' : 1,
            'rp': 25,
            'id' : 1,
            'role' : "seller",
            "username" : "Seller",
            "city" : "sby",
            "gender" : "Male",
        }
        res = client.get('/admin/get/seller', query_string = data ,headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
    def test_del_user_admin_invalid(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            # 'id' : 1,
            'username': "TEST",
        }
        res = client.delete('/admin/delete/costumer',query_string = data, headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
    
    def test_del_seller_admin_invalid1(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            'id' : 1,
            # 'username': "TEST",
        }
        res = client.delete('/admin/delete/seller',query_string = data, headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200

    def test_activate_user_admin(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            'id' : 1
            # 'username': "TEST",
        }
        res = client.put('/admin/activate/seller',query_string = data, headers={'Authorization': 'Bearer '+token})
        assert res.status_code==404
    # def test_activate_user_admin2(self, client):
    #     reset_db()
    #     token = create_token("ok")
    #     data = {
    #         # 'id' : 1
    #         'username': "TEST"
    #     }
    #     res = client.put('/admin/activate/seller',query_string = data, headers={'Authorization': 'Bearer '+token})
    #     assert res.status_code==404