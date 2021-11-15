from flask import Flask, request,jsonify, redirect, url_for,session
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
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
mycol6 = mydb["account_customer"] 
mycol7 = mydb["account_shop"] 
mycol8 = mydb["account_admin"] 


app = Flask(__name__)

#config JWT

app.config["JWT_SECRET_KEY"] = "Comp3122Project" 
app.config['SECRET_KEY'] = "Comp3122Project" 
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
jwt = JWTManager(app)
@app.route('/', methods=['GET'])
def index_page():
    #Index page   
    return 'Order Shop Api \n '+'please login by /login/shop_id/password', 200

@app.route('/login/<shop_id>/<password>', methods=['GET'])
def login(shop_id,password):
    test = mycol7.find_one({"shop_id": shop_id,"password":password})
    if test:
        access_token = create_access_token(identity=shop_id)
        session['token'] = access_token
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad shop id or Password"), 401
        
@app.route('/logout', methods=['GET'])
def logout():     
        session.clear()
        return jsonify(message="Logout Succeeded!"), 201

#finish order
@app.route('/finish_order/<customer_id>', methods=['PATCH',"get"])
def finish_order(customer_id):
    if 'token' not in session:
            # If user have not login
            return jsonify({"error":"you need to login first"}),401
    new_data = request.json
    item_ids = new_data["item_ids"]
    shop_id = new_data["shop_id"]
    delivery_status=new_data["delivery_status"]
    mycol2.update_one({"customer_id": customer_id}, { "$set" : new_data})
    return jsonify({"message":"finished order"}),201

#get delivered order 
@app.route('/receipts', methods=['GET'])
def get_receipts():
    if 'token' not in session:
            # If user have not login
            return jsonify({"error":"you need to login first"}),401
    output =[]    
    results = list(mycol2.find({"delivery_status":"y"},{"_id":0},).sort('customer_id'))

    l = len(results)
    if l >0:
        for x in results:
            print(x, flush=True)
            output.append(x)
        return jsonify(output),200 
    else:
        print("not found!",flush=True)
        return jsonify({"error":"not found"}),404 


#start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15002, debug=True)
