from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
import csv
import numpy as np
import pandas as pd
import requests
import json
import plotly
import plotly.express as px
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datatable import dt, f, by, g, join, sort, update, ifelse
from datetime import date



# data_ecom = pd.read_csv("/home/aisuathu/Documents/ecom2.csv")
# data_ecom2 =pd.read_csv("/home/aisuathu/Documents/ecom.csv")
#print(data_ecom.head(50))
import matplotlib.pyplot as plt
import io
# import random
from flask import Response
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

missing_value_formats = ["n.a.","?","NA","n/a", "na", "--"]


# CustomerID = data_ecom.isnull().sum().sort_values(ascending=False).head().CustomerID
# Description = data_ecom.isnull().sum().sort_values(ascending=False).head().Description
# Country = data_ecom.isnull().sum().sort_values(ascending=False).head().Country
# InvoiceDate =data_ecom.isnull().sum().sort_values(ascending=False).head().InvoiceDate
# Quantity =data_ecom.isnull().sum().sort_values(ascending=False).head().Quantity


# x = np.array(["A", "B", "C", "D"])
# y = np.array([3, 8, 1, 10])

# plt.bar(x,y)
# plt.show()


# x = np.array(["A", "B", "C", "D"])
# y = np.array([3, 8, 1, 10])

# s = pd.Series([1, 2, 3])
# fig, ax = plt.subplots()
# s.plot.bar()
# fig.savefig('my_plot2.png')


# creating dataframe
# df = pd.DataFrame({
#     'Coloumn': ['CustomerID', 'Description', 'Country','InvoiceDate','Quantity'],
   
#     'Malicious': [CustomerID, Description, Country,InvoiceDate,Quantity]
# })
  
# # plotting graph
# df.plot(x="Coloumn", y=["Malicious"], kind="bar")
# plt.show()

# data_ecom.plot(x="InvoiceNo", y=["CustomerID"])
# plt.show()
# df_wine['alcohol_class'] = np.where(df_wine['alcohol']>=10.0, '1', '0')
# print(data_ecom.info())
#print(data_ecom.isnull().sum().sort_values(ascending=False).head().CustomerID)


# X = data_ecom.iloc[:,0].values
# X= X.reshape(-1, 1)
# # To put constant using imputer class
# imputer = SimpleImputer(missing_values=np.nan, strategy='constant')
# imputer = imputer.fit(X)
# X = imputer.transform(X)
# print(X)

# df5 = print(data_ecom, data_ecom2, pd.merge(data_ecom, data_ecom2, on='InvoiceNo'))
# print(df5)
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True



app.config['MONGO_URI'] =  "mongodb+srv://jisa:jisa@cluster0.jfbx4.mongodb.net/flask?retryWrites=true&w=majority"

# 'mongodb+srv://flask:flask@cluster0.zjwhk.mongodb.net/flaskpython?retryWrites=true&w=majority'
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://jisa:jisa@cluster0.jfbx4.mongodb.net/flask?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mongo = PyMongo(app)
todos = mongo.db.flaskpython



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
    if request.method == 'GET':
        saved_todos = list(todos.find())
        lei = []
        for d in saved_todos:
            if(d.get("lei") == ""):
                score_titles = [{"lei": "lei empty", "email": d.get("email"),"mongoID":d.get("_id")}]
                # score_titles = [{"lei": d.get("lei"), "email": d.get("email"),"mongoID":d.get("_id")}]
                lei.append(score_titles)
            else:
                # print("LEI TO BE SEARCHED")
                # print(d.get("lei"))
                URL = "https://api.gleif.org/api/v1/lei-records?page[size]=10&page[number]=1&filter[lei]="+d.get("lei")
                response_API = requests.get(URL)
                # print("response api")
                # print(response_API)
                # print("response api")
                data = response_API.text
                parse_json = json.loads(data)
                # print("parse json")
                # print(parse_json)
                # print("parse json")
                # active_case = parse_json['data']['attributes']
                active_case = parse_json['data']
                # print("active_case")
                # print(active_case)
                # print("active_case")
                if not active_case:
                    # print("empty")
                    today = date.today()
                    # today = datetime.date.today()
                    score_titles = {"status":"LEI NOT FOUND","lei": d.get("lei"), "email": d.get("email"),"wallet":d.get("wallet"),"kycreg":d.get("date"),"checkDate":str(today),"mongoID":d.get("_id")}
                    lei.append(score_titles)
                else:
                    print("data present")
                # if(len(active_case)<0):
                #     print("length < 0")
                # else:
                #     print("length > 0")
                    for i in active_case:
                        # print(i)
                        print(i['attributes']['entity']['status'])
                        # active2 = json.loads(i)
                        # a3 = active2["attributes"]
                        # print(a3)
                        # score_titles = {"status":a3,"lei": d.get("lei"), "email": d.get("email"),"mongoID":d.get("_id")}
                        # lei.append(score_titles)


                #     # active_case2 = active_case['attributes']

                #     # print(active_case)
                

                #     # response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
                #     # data = response_API.text
                #     # parse_json = json.loads(data)
                #     # active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
                #     # print("Active cases in South Andaman:", active_case)
                #     # score_titles = {"lei": d.get("lei"), "email": d.get("email"),"mongoID":d.get("_id")}
                #         lei.append(score_titles)
        print(lei)     
        return render_template('db.html', todos=saved_todos,leiIssue= lei)


# READ THE WHOLE DATASET AND DISPLAY IN A TABLE IN HTML PAGE
@app.route('/data', methods=['GET', 'POST'])
def data():
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


# # READ THE DATASET AND DO PREPROCESSING; REMOVING NAN VALUES
# @app.route('/preprocessing', methods=['GET', 'POST'])
# def preprocessing():
#     if request.method == 'POST':
#         f = request.form['preprocessing']
#         data = []
#         with open(f) as file:
#             print(file.name)
#             # data_ecom3 =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name,na_values = missing_value_formats)
#             # data_ecom3 =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name)
#             data_ecom3 =pd.read_csv(file.name+".csv")
#             data_ecom3['CustomerID'].fillna(0, inplace=True)
#             data_ecom3['InvoiceNo'].fillna(0, inplace=True)
#             data_ecom3['Description'].fillna(0, inplace=True)
#             data_ecom3['Quantity'].fillna(0, inplace=True)
#             data_ecom3['InvoiceDate'].fillna(0, inplace=True)
#             data_ecom3['Country'].fillna(0, inplace=True)
#             # X = data_ecom3.iloc[:,0].values
#             # X= X.reshape(-1, 1)
#             # # To put constant using imputer class
#             # imputer = SimpleImputer(missing_values=np.nan, strategy='constant')
#             # imputer = imputer.fit(X)
#             # X = imputer.transform(X)
#         data = pd.DataFrame(data_ecom3)
#         return render_template('procNan.html',  tables=[data.head().to_html(classes='data')], titles=data.columns.values)


# # READ THE DATASET AND DO PREPROCESSING; DROPING NAN VALUES
# @app.route('/preprocessingdrop', methods=['GET', 'POST'])
# def preprocessingdrop():
#     if request.method == 'POST':
#         f = request.form['preprocessingdrop']
#         data = []
#         with open(f) as file:
#             print(file.name)
#             # data_ecom3 =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name,na_values = missing_value_formats)
#             # data_ecom3 =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name)
#             data_ecom3 =pd.read_csv(file.name+".csv")
#             # data_ecom3.dropna(axis=0,inplace=True)
#             new_df = data_ecom3.dropna(axis = 0, how ='any') 

#             # X = data_ecom3.iloc[:,0].values
#             # X= X.reshape(-1, 1)
#             # # To put constant using imputer class
#             # imputer = SimpleImputer(missing_values=np.nan, strategy='constant')
#             # imputer = imputer.fit(X)
#             # X = imputer.transform(X)
#         data = pd.DataFrame(new_df)
#         return render_template('data.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)


# # READ THE DATASET AND CREATE A BAR GRAPH BASED ON COLUMNS
@app.route('/barch', methods=['GET', 'POST'])
def barch():
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
@app.route('/barchC', methods=['GET', 'POST'])
def barchC():
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


# @app.route('/plot.png')
# def plot_png2():
#         data = []
#         # with open(f) as file:
#             # print(file.name)
#             # data_ecom3 =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name)
#         x = np.array(['CustomerID', 'Description', 'Country','InvoiceDate','Quantity'])
#         y = np.array([3, 8, 1, 10,15])
#         plt.bar(x,y)
#         plt.show()
#         # data = pd.DataFrame(new_df)
#         # return render_template('data.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)



# @app.route('/barchartcol', methods=['GET', 'POST'])
# def barchartcol():
#     if request.method == 'POST':
#         f = request.form['barchartcol']
#         data = []
#         with open(f) as file:
#             print(file.name)
#             data_ecom =pd.read_csv(file.name+".csv")
#             # data_ecom =pd.read_csv("/home/aisuathu/Documents/Aisu office/FlaskIntroduction-master/"+file.name)
#             CustomerID = data_ecom.isnull().sum().sort_values(ascending=False).head().CustomerID
#             Description = data_ecom.isnull().sum().sort_values(ascending=False).head().Description
#             Country = data_ecom.isnull().sum().sort_values(ascending=False).head().Country
#             InvoiceDate =data_ecom.isnull().sum().sort_values(ascending=False).head().InvoiceDate
#             Quantity =data_ecom.isnull().sum().sort_values(ascending=False).head().Quantity
#         data = pd.DataFrame(data_ecom)
#         return render_template('figure.html')


# @app.route('/my_plot2.png')
# def my_plot2():
#     fig = create_figure2()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png') 

# def create_figure2():
#     fig = Figure()
#     axis = fig.add_subplot(1,1,1)
#     xs = ['CustomerID', 'Description', 'Country','InvoiceDate','Quantity']
#     ys = [CustomerID, Description, Country,InvoiceDate,Quantity]
#     axis.plot(xs, ys)
#     return fig

# @app.route('/my_plot3.png',methods=['GET', 'POST'])
# def my_plot3():
#     if request.method == 'POST':
#         x = ["APPLES", "BANANAS"]
#         y = [400, 350]
#         plt.bar(x, y)
#         plt.show()

# def create_figure3():
#     fig, ax = plt.subplots(figsize = (6,4))
#     fig.patch.set_facecolor('#E8E5DA')

#     x = ['CustomerID', 'Description', 'Country','InvoiceDate','Quantity']

#     y = [CustomerID, Description, Country,InvoiceDate,Quantity]


#     ax.bar(x, y, color = "#304C89")

#     plt.xticks(rotation = 30, size = 5)
#     plt.ylabel("Expected Clean Sheets", size = 5)


#     return fig



if __name__ == '__main__':
    from livereload import Server
    server = Server(app.wsgi_app)
    server.serve(host = '0.0.0.0',port=5000)