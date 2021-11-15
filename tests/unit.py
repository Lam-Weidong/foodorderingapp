import pytest
import requests as req


#Testing orderapi
def test_OrderAPI_Login_Successfully():
    resp = req.get("http://localhost:15000/login/00001/1111") 
    assert resp.status_code == 201


def test_OrderAPI_Login_Fail():
    resp = req.get("http://localhost:15000/login/gg/gg")  
    assert resp.status_code == 401

def test_OrderAPI_Logout():
    resp = req.get("http://localhost:15000/logout")  
    assert resp.status_code == 201

#Customer Endpoint

def test_OrderAPI_Customer(headers):
    resp = req.get("http://localhost:15000/customers?jwt="+headers)  
    
    assert resp.status_code == 200
    
def test_OrderAPI_CustomerByID(headers):
    resp = req.get("http://localhost:15000/customers/00001?jwt="+headers)  
    
    assert resp.status_code == 200

#Cart Endpoint
def test_OrderAPI_Cart(headers):
    resp = req.get("http://localhost:15000/cart?jwt="+headers)  
    
    assert resp.status_code == 200

    
def test_OrderAPI_CartByID(headers):
    resp = req.get("http://localhost:15000/cart/00001?jwt="+headers)      
    assert resp.status_code == 200

#Shop Endpoint
def test_OrderAPI_Shop(headers):
    resp = req.get("http://localhost:15000/shops?jwt="+headers)  
  
    assert resp.status_code == 200

def test_OrderAPI_ShopByID(headers):
    resp = req.get("http://localhost:15000/shops/001?jwt="+headers)  
    
    assert resp.status_code == 200

#Menu Endpoint
def test_OrderAPI_Menu(headers):
    resp = req.get("http://localhost:15000/menu?jwt="+headers)  
    
    assert resp.status_code == 200

def test_OrderAPI_MenuByShopId(headers):
    resp = req.get("http://localhost:15000/menu/001?jwt="+headers)  
    
    assert resp.status_code == 200

#Order Endpoint
def test_OrderAPI_generate_order_by_Custid(headers):
    resp = req.get("http://localhost:15000/cart/00001/order?jwt="+headers)  
    assert resp.status_code == 201


def test_OrderAPI_Order(headers):
    resp = req.get("http://localhost:15000/orders?jwt="+headers)  
    assert resp.status_code == 200

def test_OrderAPI_OrderByCustID(headers):
    resp = req.get("http://localhost:15000/orders/00001?jwt="+headers)  
    assert resp.status_code == 200
    

#Testing Admin
def test_Admin_Login_Successfully():
    resp = req.get("http://localhost:16000/login/admin/admin") 
    assert resp.status_code == 201


def test_Admin_Login_Fail():
    resp = req.get("http://localhost:16000/login/gg/gg")  
    assert resp.status_code == 401

def test_Admin_Logout():
    resp = req.get("http://localhost:16000/logout")  
    assert resp.status_code == 201

#Customer Endpoint

def test_Admin_Customer(headers):
    resp = req.get("http://localhost:16000/customers?jwt="+headers)  
    
    assert resp.status_code == 200
    
def test_Admin_CustomerByID(headers):
    resp = req.get("http://localhost:16000/customers/00001?jwt="+headers)  
    
    assert resp.status_code == 200

#Cart Endpoint
def test_Admin_Cart(headers):
    resp = req.get("http://localhost:16000/cart?jwt="+headers)  
    
    assert resp.status_code == 200

    
def test_Admin_CartByID(headers):
    resp = req.get("http://localhost:16000/cart/00001?jwt="+headers)      
    assert resp.status_code == 200

#Shop Endpoint
def test_Admin_Shop(headers):
    resp = req.get("http://localhost:16000/shops?jwt="+headers)  
  
    assert resp.status_code == 200

def test_Admin_ShopByID(headers):
    resp = req.get("http://localhost:16000/shops/001?jwt="+headers)  
    
    assert resp.status_code == 200

#Menu Endpoint
def test_Admin_Menu(headers):
    resp = req.get("http://localhost:16000/menu?jwt="+headers)  
    
    assert resp.status_code == 200

def test_Admin_MenuByShopId(headers):
    resp = req.get("http://localhost:16000/menu/001?jwt="+headers)  
    
    assert resp.status_code == 200

#Order Endpoint
def test_Admin_generate_order_by_Custid(headers):
    resp = req.get("http://localhost:16000/cart/00001/order?jwt="+headers)  
    assert resp.status_code == 201


def test_Admin_Order(headers):
    resp = req.get("http://localhost:16000/orders?jwt="+headers)  
    assert resp.status_code == 200

def test_Admin_OrderByCustID(headers):
    resp = req.get("http://localhost:16000/orders/00001?jwt="+headers)  
    assert resp.status_code == 200

#Testing Menu
def test_Admin_Login_Successfully():
    resp = req.get("http://localhost:15001/login/001/001") 
    assert resp.status_code == 201


def test_Admin_Login_Fail():
    resp = req.get("http://localhost:15001/login/gg/gg")  
    assert resp.status_code == 401

def test_Admin_Logout():
    resp = req.get("http://localhost:15001/logout")  
    assert resp.status_code == 201
#Testing get menu by shop id 
def test_Menu_MenuByShopId(headers):
    resp = req.get("http://localhost:15001/menu/001?jwt="+headers)  
    
    assert resp.status_code == 200


#Testing Shop
def test_Shop_Login_Successfully():
    resp = req.get("http://localhost:15002/login/001/001") 
    assert resp.status_code == 201


def test_Shop_Login_Fail():
    resp = req.get("http://localhost:15001/login/gg/gg")  
    assert resp.status_code == 401

def test_Shop_Logout():
    resp = req.get("http://localhost:15001/logout")  
    assert resp.status_code == 201

#Testing finish_order by customer id
def test_Shop_FinishOrder(headers):
    resp = req.get("http://localhost:15001/finish_order/00001?jwt="+headers)  
    
    assert resp.status_code == 404 # because have not order for customer at the beginning

#Testing get receiptss
def test_Shop_MenuByShopId(headers):
    resp = req.get("http://localhost:15001/receipts?jwt="+headers)  
    assert resp.status_code == 404 # because have not finished order at the beginning
