# using flask_restful
from flask import Flask, jsonify, request,Response
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
import requests
from datetime import date
import json
from bson.json_util import dumps, loads
from bson import json_util
from flask_cors import CORS

# creating the flask app
app = Flask(__name__)
CORS(app)
# creating an API object
api = Api(app)
app.config['MONGO_URI'] = 'mongodb+srv://flask:flask@cluster0.zjwhk.mongodb.net/flaskpython?retryWrites=true&w=majority'
mongo = PyMongo(app)

todos = mongo.db.flaskpython
transaction = mongo.db.transaction_hist

missing_value_formats = ["n.a.","?","NA","n/a", "na", "--"]
countries = ["NORTH KOREA", "CUBA", "SOUTH KOREA"]


class Hello(Resource):

	def get(self):

		return jsonify({'message': 'hello world'})

	# Corresponds to POST request
	def post(self):
		
		data = request.get_json()	 # status code
		return jsonify({'data': data}), 201


class DBT(Resource):
    def get(self):
        data = 'dt'
        saved_todos = list(todos.find())
        get_transactions = list(transaction.find())
        # get_wallet = list(todos.find({},{ "_id": 0, "lei": 0, "country": 0,"name": 0, "wallet": 1,"ipfs": 0, "date": 0,"contact": 0, "email": 0 }))
        # print(get_wallet)
        lei = []
        wallet_tx = []
        trans_hist = []
        for d in saved_todos:
            if(d.get("lei") == ""):
                if(d.get("country").upper() in countries):
                    print("exists")
                    country="Discrepancy"
                else:
                    print("not exists")
                today = date.today()
                score_titles = {"status":"LEI NOT ADDED BY USER","lei": "NA", "email": d.get("email"),"wallet":d.get("wallet"),"kycreg":d.get("date"),"checkDate":str(today),"mongoID":d.get("_id")}
                lei.append(score_titles)
            else:
                if(d.get("country").upper() in countries):
                    print("exists")
                else:
                    print("not exists")
                URL = "https://api.gleif.org/api/v1/lei-records?page[size]=10&page[number]=1&filter[lei]="+d.get("lei")
                response_API = requests.get(URL)
                data = response_API.text
                parse_json = json.loads(data)
                active_case = parse_json['data']
                if not active_case:
                    today = date.today()
                    score_titles = {"status":"LEI NOT FOUND","lei": d.get("lei"), "email": d.get("email"),"wallet":d.get("wallet"),"kycreg":d.get("date"),"checkDate":str(today),"mongoID":d.get("_id")}
                    lei.append(score_titles)
                else:
                    print("")
        for i in saved_todos:
            for j in get_transactions:
            # count = 0
            # if(d.get("") != i.get("lei")):
                if((i.get("wallet") == j.get("seller_wallet")) and (j.get("tx") == 1)):    
                    wallet_tx.append({"seller_wallet":i.get("wallet"),"lei":i.get("lei"),"kycdate":i.get("date"), "orderId":j.get("orderId"),"orderdate":j.get("date")})
        print(wallet_tx)   

        # json_data = dumps(saved_todos, indent = 2) 

        # with open('data.json', 'w') as file:
        #     file.write(json_data)


 
        result2 = todos.aggregate([
            # { '$match': { 'tx': '0' } },
            {
                
                '$lookup': {
                    'from': 'transaction_hist', 
                    'localField': 'lei', 
                    'foreignField': 'lei', 
                    'as': 'com'
                }
            },
            {
                '$unwind':'$com'                
            },
            {
                '$match':{
                    'com.tx':1
                }
            }
        ])

        # trans_hist.append(list(result2))    
        # print(trans_hist)
        trx = list(result2)
        print(trx)

        cD = {
            'todos':saved_todos,'leiIssue':lei,'txhistory':wallet_tx,'docs':trx
        }      
        
        # return render_template('db.html', todos=saved_todos,leiIssue= lei,txhistory= wallet_tx,docs = trx)

        # return jsonify(saved_todos)
        # return jsonify({'todos':saved_todos,'leiIssue':lei,'txhistory':wallet_tx,'docs':trx})
        # return  Response(json.dumps(saved_todos,default=str),mimetype="application/json")
        # return Response(json_util.dumps({"items": saved_todos}))
        return  Response(json.dumps(cD,default=str),mimetype="application/json")


# another resource to calculate the square of a number
class Square(Resource):

	def get(self, num):

		return jsonify({'square': num**2})


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')
api.add_resource(DBT,'/getDB')

# driver function
if __name__ == '__main__':

	app.run(debug = True)
