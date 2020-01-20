import pytest, logging
from . import app, cache, create_token, client, reset_db
from flask import Flask, request, json
from flask_jwt_extended import get_jwt_claims
import hashlib

class TestUserCrud():
    def test_get_user_id(self, client):
        reset_db()
        token = create_token("user")
        data = {
            "rating" : 5,
            "review": "hehehe"
        }
        res = client.put('/user/review', json = data , headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200
      
    def test_get_agent_id(self, client):
        reset_db()
        token = create_token("agent")
        data = {
            "rating" : 5,
            "review": "hehehe"
        }
        res = client.put('/agent/review', json = data, headers={'Authorization': 'Bearer '+token})
        resJson = json.loads(res.data)
        assert res.status_code==200

    # def test_put_user(self, client):
        # reset_db()
        # token = create_token("ok")
        # res = client.get('/review', headers={'Authorization': 'Bearer '+token})
        # assert res.status_code==200