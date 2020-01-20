import pytest, logging
from . import app, cache, create_token, client, reset_db
from flask import Flask, request, json
from flask_jwt_extended import get_jwt_claims
import hashlib

class TestUserCrud():
    def test_get_user_id(self, client):
        reset_db()
        token = create_token("user")
        res = client.get('/user', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
      
    def test_get_agent_id(self, client):
        reset_db()
        token = create_token("agent")
        res = client.get('/agent', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200

    def test_put_user(self, client):
        reset_db()
        token = create_token("user")
        data = {
            'username' : "TEST",
            'password': 'HEDYY1',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.put('/user', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200

    def test_put_user1(self, client):
        reset_db()
        token = create_token("user")
        data = {
            'username' : "TEST",
            'password': 'HEDYYY',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.put('/user', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==422
    
    def test_del_user_id_invalid(self, client):
        reset_db()
        token = create_token("user")
        res = client.delete('/user', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
        
    # def test_del_user_id_invalid11(self, client):
    #     reset_db()
    #     token = create_token("user")
    #     res = client.delete('/user', headers={'Authorization': 'Bearer '+token})
    #     assert res.status_code==404
    
    # def test_get_user_id1(self, client):
    #     reset_db()
    #     token = create_token("user")
    #     res = client.get('/user', headers={'Authorization': 'Bearer '+token})
    #     assert res.status_code==404

    def test_put_agent(self, client):
        reset_db()
        token = create_token("agent")
        data = {
            'username' : "Agent",
            'password': 'HEDYY1',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.put('/agent', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200

    def test_put_agent1(self, client):
        reset_db()
        token = create_token("agent")
        data = {
            'username' : "Agent",
            'password': 'HEDYYY',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.put('/agent', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==422
    
    def test_delete_agent(self, client):
        reset_db()
        token = create_token("agent")
        res = client.delete('/agent', headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
    
    # def test_delete_agent1(self, client):
    #     reset_db()
    #     token = create_token("agent")
    #     res = client.delete('/agent', headers={'Authorization': 'Bearer '+token})
    #     assert res.status_code==404
    
    # def test_get_agent1(self,client):
    #     reset_db()
    #     token = create_token("agent")
    #     res = client.get('/agent', headers={'Authorization': 'Bearer '+token})
    #     assert res.status_code==404

    def test_post_agent(self, client):
        reset_db()
        token = create_token("agent")
        data = {
            'username' : "Agent2",
            'password': 'Hedy22',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.post('/agent/registration', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200

    def test_post_agent1(self, client):
        reset_db()
        token = create_token("agent")
        data = {
            'username' : "Agent2",
            'password': 'Hedyyy',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.post('/agent/registration', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==422
        
    def test_post_user(self, client):
        reset_db()
        token = create_token("user")
        data = {
            'username' : "User",
            'password': 'Hedyy1',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.post('/user/registration', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200

    def test_post_user1(self, client):
        reset_db()
        token = create_token("user")
        data = {
            'username' : "User",
            'password': 'Hedyyy',
            'fullname' : "hoho",
            'address' : "ihi",
            "number_phone" : 12345,
            "email" : "hihi",
            "gender" : "Male",
            "city" : "sby",
            "image" : "hu"
        }
        res = client.post('/user/registration', json=data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==422

    def test_get_admin_user_id(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            'p' : 1,
            'rp': 25,
            'id' : 1,
            'role' : "user",
            "username" : "TEST",
            "city" : "sby",
            "gender" : "Male",
        }
        res = client.get('/admin/get/costumer', query_string = data ,headers={'Authorization': 'Bearer '+token})
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
    
    def test_del_user_admin_invalid1(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            'id' : 1,
            # 'username': "TEST",
        }
        res = client.delete('/admin/delete/costumer',query_string = data, headers={'Authorization': 'Bearer '+token})
        assert res.status_code==200
    def test_activate_user_admin(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            'id' : 1
            # 'username': "TEST",
        }
        res = client.put('/admin/activate/costumer',query_string = data, headers={'Authorization': 'Bearer '+token})
        assert res.status_code==404
    def test_activate_user_admin2(self, client):
        reset_db()
        token = create_token("ok")
        data = {
            # 'id' : 1
            'username': "TEST"
        }
        res = client.put('/admin/activate/costumer',query_string = data, headers={'Authorization': 'Bearer '+token})
        assert res.status_code==404