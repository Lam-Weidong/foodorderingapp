import  requests as req
import  pytest
import json


def getToken():
   resp = req.get("http://localhost:15000/login/00001/1111") 
   return resp.json()['access_token']

@pytest.fixture()
def headers():
   return getToken()