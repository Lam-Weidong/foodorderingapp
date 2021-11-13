from flask import Flask, request,jsonify, redirect, url_for
import os

from pymongo import MongoClient
from datetime import datetime
import sys


#get connection details from env variable if available
if os.getenv('MONGO_SERVER_HOST') is not None:
    mongo_host = os.getenv('MONGO_SERVER_HOST')
else:
    mongo_host = "mongo"
    
if os.environ.get('MONGO_SERVER_PORT') is not None:
    mongo_port = os.environ.get('MONGO_SERVER_PORT')
else:
    mongo_port='27017'

if os.getenv('MONGO_USERNAME') is not None:
    mongo_user = os.getenv('MONGO_USERNAME')
    
if os.environ.get('MONGO_PASSWORD') is not None:
    mongo_password = os.environ.get('MONGO_PASSWORD')

conn_str = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
print(f"Connecting to mongo server: {conn_str} ",flush=True)

client = MongoClient(conn_str)
try:
    client.list_database_names()
    print('Connection to Mongo Server Suceeded')

except Exception as err:
    print(f"Connection to Mongo Server Failed. Error: {err}")
    sys.exit() 

mydb = client["ordershop"] #use db
mycol = mydb["customer"] #use collection
mycol2 = mydb["cart"] 
mycol3 = mydb["shop"] 
mycol4 = mydb["menu"] 
mycol5 = mydb["order"] 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index_page():
    #Index page   
    return 'Order Shop Api\n', 200

@app.route('/me', methods=['GET'])
def about_me():
    #Put your studentID and name in my_info variable
    my_info = {
                'id':'17077493D',
                'name':'Lam Weidong'
                }       
    return jsonify(my_info)

# Get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    output =[]    
    results = list(mycol.find({},{"_id":0},).sort('customer_id'))

    l = len(results)
    if l >0:
        for x in results:
            print(x, flush=True)
            output.append(x)
        return jsonify(output),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 


# Get customer by ID
@app.route('/customers/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    output =[]    
    results = list(mycol.find({ "customer_id": customer_id},{'_id':0}))
    
    l = len(results)
    if l >0:
        return jsonify(results),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 

# get carts created by all customers
@app.route('/cart', methods=['GET'])
def get_carts():
    output =[] 
    pipeline=[   
        { "$project": {'_id':0}},     
        { '$sort' : { 'customer_id':1 } }  ,
        {
            '$lookup':
            {
                'from': "cart",
                'localField': "customer_id",
                'foreignField': "customer_id",
                'as': "customer_cart",
                'pipeline': [
                    { '$project': {'_id':0,'customer_id':0}},     
                    { '$sort' : { 'customer_id':1 } }
                ]
            }
        }

        ]   
    results = list(mycol.aggregate(pipeline))

    l = len(results)
    if l >0:
        for x in results:
            print(x, flush=True)
            output.append(x)
        return jsonify(output),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 


# get cart created by specified customer
@app.route('/cart/<customer_id>', methods=['GET'])
def get_cart_by_id(customer_id):
    output = []
    pipeline=[
        { "$match": {'customer_id':customer_id}},           
        { "$project": {'_id':0}},        
        {
            '$lookup':
            {
                'from': "cart",
                'localField': "customer_id",
                'foreignField': "customer_id",
                'as': "customer_cart",
                'pipeline': [
                    { '$project': {'_id':0, 'customer_id':0}}
                ]
            }
        }

        ]   
    results = list(mycol.aggregate(pipeline))

    l = len(results)
    if l >0:
        for x in results:
            print(x, flush=True)
            output.append(x)
        return jsonify(output),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 

#adding customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    customer_id = data["customer_id"]
    username = data["username"]
    deliver_address = data["deliver_address"]
    password = data["password"]
    mycol.insert_one(data)
    return jsonify({"message":"added customer"}),201

#editing customer
@app.route('/customers/<customer_id>', methods=['PATCH'])
def edit_customer(customer_id):
    new_data = request.json
    username = new_data["username"]
    deliver_address = new_data["deliver_address"]
    password = new_data["password"]
    mycol.update_one({"customer_id": customer_id}, { "$set" : new_data})
    return jsonify({"message":"edited customer"}),201

#deleting customer
@app.route('/customers/<customer_id>/delete', methods=['DELETE'])
def del_customer(customer_id):
    del_data = { "customer_id" : customer_id }
    mycol.delete_one(del_data)
    return jsonify({"message":"deleted customer"}),200

#creating cart
@app.route('/cart', methods=['POST'])
def add_cart():
    data = request.json
    customer_id = data["customer_id"]
    item_ids = data["item_ids"]
    shop_id = data["shop_id"]
    mycol2.insert_one(data)
    return jsonify({"message":"created cart"}),201

#editing cart
@app.route('/cart/<customer_id>', methods=['PATCH'])
def edit_cart(customer_id):
    new_data = request.json
    item_ids = new_data["item_ids"]
    shop_id = new_data["shop_id"]
    mycol2.update_one({"customer_id": customer_id}, { "$set" : new_data})
    return jsonify({"message":"edited cart"}),201

#empty cart
@app.route('/cart/<customer_id>/delete', methods=['DELETE'])
def empty_cart(customer_id):
    del_data = { "customer_id" : customer_id }
    mycol2.delete_one(del_data)
    return jsonify({"message":"cart emptied"}),200

#Get all shops
@app.route('/shops', methods=['GET'])
def get_shops():
    output =[]    
    results = list(mycol3.find({},{"_id":0},).sort('shop_id'))

    l = len(results)
    if l >0:
        for x in results:
            print(x, flush=True)
            output.append(x)
        return jsonify(output),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 


# Get shop by ID
@app.route('/shops/<shop_id>', methods=['GET'])
def get_shop_by_id(shop_id):
    output =[]    
    results = list(mycol3.find({ "shop_id": shop_id},{'_id':0}))
    
    l = len(results)
    if l >0:
        return jsonify(results),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 

# get menu created by all shops
@app.route('/menu', methods=['GET'])
def get_menu():
    output =[] 
    pipeline=[   
        { "$project": {'_id':0}},     
        { '$sort' : { 'shop_id':1 } }  ,
        {
            '$lookup':
            {
                'from': "menu",
                'localField': "shop_id",
                'foreignField': "shop_id",
                'as': "shop_menu",
                'pipeline': [
                    { '$project': {'_id':0,'shop_id':0}},     
                    { '$sort' : { 'shop_id':1 } }
                ]
            }
        }

        ]   
    results = list(mycol3.aggregate(pipeline))

    l = len(results)
    if l >0:
        for x in results:
            print(x, flush=True)
            output.append(x)
        return jsonify(output),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 


# get menu created by specified shop
@app.route('/menu/<shop_id>', methods=['GET'])
def get_menu_by_id(shop_id):
    output =[] 
    pipeline=[
        { "$match": {'shop_id':shop_id}},           
        { "$project": {'_id':0}},        
        {
            '$lookup':
            {
                'from': "menu",
                'localField': "shop_id",
                'foreignField': "shop_id",
                'as': "shop_menu",
                'pipeline': [
                    { '$project': {'_id':0, 'shop_id':0}}
                ]
            }
        }

        ]   
    results = list(mycol3.aggregate(pipeline))

    l = len(results)
    if l >0:
        for x in results:
            print(x, flush=True)
            output.append(x)
        return jsonify(output),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 

#adding shop
@app.route('/shops', methods=['POST'])
def add_shop():
    data = request.json
    shop_id = data["shop_id"]
    shopname = data["shopname"]
    shop_address = data["shop_address"]
    tel = data["tel"]
    mycol3.insert_one(data)
    return jsonify({"message":"added shop"}),201

#editing shop
@app.route('/shops/<shop_id>', methods=['PATCH'])
def edit_shop(shop_id):
    new_data = request.json
    shopname = new_data["shopname"]
    shop_address = new_data["shop_address"]
    tel = new_data["tel"]
    mycol3.update_one({"shop_id": shop_id}, { "$set" : new_data})
    return jsonify({"message":"edited shop"}),201

#deleting shop
@app.route('/shops/<shop_id>/delete', methods=['DELETE'])
def del_shop(shop_id):
    del_data = { "shop_id" : shop_id }
    mycol3.delete_one(del_data)
    return jsonify({"message":"deleted shop"}),200

#creating menu
@app.route('/menu', methods=['POST'])
def add_menu():
    data = request.json
    shop_id = data["shop_id"]
    item_ids = data["item_ids"]
    mycol4.insert_one(data)
    return jsonify({"message":"created menu"}),201

#editing menu
@app.route('/menu/<shop_id>', methods=['PATCH'])
def edit_menu(shop_id):
    new_data = request.json
    item_ids = new_data["item_ids"]
    mycol4.update_one({"shop_id": shop_id}, { "$set" : new_data})
    return jsonify({"message":"edited menu"}),201

#empty menu
@app.route('/menu/<shop_id>/delete', methods=['DELETE'])
def empty_menu(shop_id):
    del_data = { "shop_id" : shop_id }
    mycol4.delete_one(del_data)
    return jsonify({"message":"menu emptied"}),200

#generate order from cart
@app.route('/cart/<customer_id>/order', methods=['GET'])
def generate_order_by_id(customer_id):   
    return jsonify({"message":"unfinished"}),200



#start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)
