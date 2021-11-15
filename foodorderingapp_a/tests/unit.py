import pytest
from flask import Flask
import requests as req


def test_Login_Successfully():
    resp = req.get("http://localhost:20000/login/00001/1111")  
    assert resp.status_code == 201


def test_Login_Fail():
    resp = req.get("http://localhost:20000/login/gg/gg")  
    assert resp.status_code == 401

def test_Logout():
    resp = req.get("http://localhost:20000/logout")  
    assert resp.status_code == 201





