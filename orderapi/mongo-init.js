db.auth('comp3122', '12345')
db = db.getSiblingDB('ordershop')

db.createCollection('customer');
db.customer.insertOne({'customer_id':'00001', 'username':'Customer1', 'deliver_address':'Address1', 'password':'1111'});
db.customer.insertOne({'customer_id':'00002', 'username':'Customer2', 'deliver_address':'Address2', 'password':'2222'});

db.createCollection('cart');
db.cart.insertOne({'customer_id':'00001', 'item_ids':[{'item_id' :'01', 'price' : 10},{'item_id' :'02', 'price' : 20}], 'shop_id':"001"});
db.cart.insertOne({'customer_id':'00002', 'item_ids':[{'item_id' :'01', 'price' : 10},{'item_id' :'02', 'price' : 20}], 'shop_id':"002"});

db.createCollection('shop');
db.shop.insertOne({'shop_id':'001', 'shopname':'shop1', 'shop_address':'S_Address1', 'tel':'12345678'});
db.shop.insertOne({'shop_id':'002', 'shopname':'shop2', 'shop_address':'S_Address2', 'tel':'12345678'});

db.createCollection('menu');
db.menu.insertOne({'shop_id':'001', 'item_ids':[{'item_id' :'01', 'price' : 10, 'stock' : 1},{'item_id' :'02', 'price' : 20, 'stock' : 2}]});
db.menu.insertOne({'shop_id':'002', 'item_ids':[{'item_id' :'01', 'price' : 10, 'stock' : 1},{'item_id' :'02', 'price' : 20, 'stock' : 2}]});

db.createCollection('order');
