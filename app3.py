from pandas.core.frame import DataFrame
from flask import Flask, render_template, url_for, request, redirect
import csv
# import numpy as np
import pandas as pd
import requests
import json
# import plotly
# import plotly.express as px
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import date

from bson.json_util import dumps, loads
# import matplotlib.pyplot as plt
# import io
from flask import Response
# from sklearn.impute import SimpleImputer

missing_value_formats = ["n.a.","?","NA","n/a", "na", "--"]

countries = ["NORTH KOREA", "CUBA", "SOUTH KOREA"]


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True



app.config['MONGO_URI'] = 'mongodb+srv://flask:flask@cluster0.zjwhk.mongodb.net/flaskpython?retryWrites=true&w=majority'
mongo = PyMongo(app)
todos = mongo.db.flaskpython
transaction = mongo.db.transaction_hist


@app.route('/', methods=['POST', 'GET'])
def index():
 
    # if request.method == 'POST':
    #     task_content = request.form['content']
    #     new_task = Todo(content=task_content)

    #     try:
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return 'There was an issue adding your task'

    # else:
    #     tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html')



@app.route('/getDB')
def getDB():
    #vLEI program. The governance framework is under open review at Trust over IP Foundation. The beta software and documentation are also available.
    if request.method == 'GET':
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
      
        
        return render_template('db.html', todos=saved_todos,leiIssue= lei,txhistory= wallet_tx,docs = trx)



@app.route('/secondorder')
def secondorder():
    #vLEI program. The governance framework is under open review at Trust over IP Foundation. The beta software and documentation are also available.
    if request.method == 'GET':
    # if request.form.get("historicalId"):
        get_transactions = list(transaction.find())
        lei = []
        sec_his = []
        print('Book ID: ',request.args.get('historicalId'))
        leiNO = request.args.get('historicalId')

        # print('Book ID: ', request.form['historicalId'])
        # request.args.get('username')
      
        for j in get_transactions:
        # count = 0
        # if(d.get("") != i.get("lei")):
            if((j.get("lei") == leiNO)):    
                sec_his.append({"consignee":j.get("consignee"),"quantity":j.get("quantity"),"orderDetails":j.get("orderDetails"), "orderId":j.get("orderId"),"orderdate":j.get("date")})
        print(sec_his)   

        # # json_data = dumps(saved_todos, indent = 2) 

        # # with open('data.json', 'w') as file:
        # #     file.write(json_data)


 
        # result2 = todos.aggregate([
        #     # { '$match': { 'tx': '0' } },
        #     {
                
        #         '$lookup': {
        #             'from': 'transaction_hist', 
        #             'localField': 'lei', 
        #             'foreignField': 'lei', 
        #             'as': 'com'
        #         }
        #     },
        #     {
        #         '$unwind':'$com'                
        #     },
        #     {
        #         '$match':{
        #             'com.tx':1
        #         }
        #     }
        # ])

        # # trans_hist.append(list(result2))    
        # # print(trans_hist)
        # trx = list(result2)
        # print(trx)
      
        
        # return render_template('db.html', todos=saved_todos,leiIssue= lei,txhistory= wallet_tx,docs = trx)
        return render_template('second_order.html',txhistory = sec_his)



@app.route('/lookupDB')
def lookupDB():
    if request.method == 'GET':
        print("getting data for aggreagation")
        fraud = []
        result = todos.aggregate([
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

        # print(list(result))
        # print(result)

        list_cur = list(result)
        print(list_cur)
  
# Converting to the JSON
        json_data = dumps(list_cur, indent = 2) 
   
# Writing data to file data.json
        # with open('data.json', 'w') as file:
        #     file.write(json_data)


        # x = list(result)
        # for i in result:
        #     print(i)
        #     # fraud.append({"seller_wallet":i.get["wallet"],"lei":i.get["lei"],"kycdate":i.get["date"], "orderId":i.get["com"]["orderId"],"orderdate":i.get["com"]["date"]})
        #     # fraud.append({"seller_wallet":i["wallet"],"lei":("lei"),"kycdate":i("date")})
        # print(fraud)            

        return render_template('fraud.html',docs2=list_cur)


# READ THE WHOLE DATASET AND DISPLAY IN A TABLE IN HTML PAGE
# @app.route('/data', methods=['GET', 'POST'])
# def data():
    if request.method == 'POST':
        f = request.form['uploadfile']
        data = []
        with open(f) as file:
            print(file.name)
            # data_ecom3 =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name)
            data_ecom3 =pd.read_csv(file.name)
            print(data_ecom3.head(50))
            # csvfile = csv.reader(file)
            # for row in csvfile:
            #     data.append(row)
        data = pd.DataFrame(data_ecom3)
        list_of_column_names = list(data_ecom3.columns)
        print(list_of_column_names)
        # return render_template('processing.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)
        return render_template('processing.html',  tables=[data.head().to_html(classes='table table-hover table-sm')],titles=data.columns.values,col=list_of_column_names)



# # READ THE DATASET AND CREATE A BAR GRAPH BASED ON COLUMNS
# @app.route('/barch', methods=['GET', 'POST'])
# def barch():
    if request.method == 'POST':
        f = request.form['barch']
        data = []
        with open(f) as file:
            print(file.name)
            # data_ecom =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name)
            data_ecom =pd.read_csv(file.name)
            CustomerID = data_ecom.isnull().sum().sort_values(ascending=False).head().CustomerID
            Description = data_ecom.isnull().sum().sort_values(ascending=False).head().Description
            Country = data_ecom.isnull().sum().sort_values(ascending=False).head().Country
            InvoiceDate =data_ecom.isnull().sum().sort_values(ascending=False).head().InvoiceDate
            Quantity =data_ecom.isnull().sum().sort_values(ascending=False).head().Quantity
            xaxis = np.array(['CustomerID', 'Description', 'Country','InvoiceDate','Quantity'])
            yaxis = np.array([CustomerID,Description,Country,InvoiceDate,Quantity])
            # df = pd.DataFrame({
            # 'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
            # 'Bananas'],
            # 'Amount': [4, 1, 2, 2, 4, 5],
            # 'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
            #  })
            # fig = px.bar(df, x='Fruit', y='Amount', color='City',  barmode='group')
            fig =px.bar(x=xaxis,y=yaxis)
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            # return plt.show()
            return render_template('chartFields.html', graphJSON=graphJSON)


# # READ THE DATASET AND CREATE A BAR GRAPH BASED ON COUNTRY
# @app.route('/barchC', methods=['GET', 'POST'])
# def barchC():
    if request.method == 'POST':
        f = request.form['barchC']
        data = []
        with open(f) as file:
            print(file.name)
            data_ecom =pd.read_csv(file.name)
            # data_ecom =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name)
            arr = data_ecom["Country"].to_numpy()
            unique_arr = np.unique(arr)
            print(unique_arr)
            df = data_ecom[data_ecom['CustomerID']== 'NaN'].groupby(['Country','CustomerID']).size().reset_index(name='count')
            print(df)
            # print(list(data_ecom['gender']).count('female'))
            # for(x in unqiuearray)
                # where row has nan wjere counrty  == x
                # push to y
            xas = unique_arr
            yas = np.array([1,2,3,4,5,6,7])
            fig2 =px.bar(x=xas,y=yas)
            graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            # return plt.show()
            return render_template('chartCountry.html', graphJSON=graphJSON)

            # plt.bar(x,y)
            # plt.show()
            # CustomerID = data_ecom.isnull().sum().sort_values(ascending=False).head().CustomerID
            # Description = data_ecom.isnull().sum().sort_values(ascending=False).head().Description
            # Country = data_ecom.isnull().sum().sort_values(ascending=False).head().Country
            # InvoiceDate =data_ecom.isnull().sum().sort_values(ascending=False).head().InvoiceDate
            # Quantity =data_ecom.isnull().sum().sort_values(ascending=False).head().Quantity
            # x = np.array(['CustomerID', 'Description', 'Country','InvoiceDate','Quantity'])
            # y = np.array([CustomerID,Description,Country,InvoiceDate,Quantity])
            # plt.bar(x,y)
            # return plt.show()
        # data = pd.DataFrame(new_df)
        # return render_template('data.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)


if __name__ == '__main__':
    from livereload import Server
    server = Server(app.wsgi_app)
    server.serve(host = '0.0.0.0',port=5000)
