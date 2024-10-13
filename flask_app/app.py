from flask import Flask
from pymongo import MongoClient
from flask import render_template


app = Flask(__name__)

client = MongoClient("mongodb+srv://root:Ru4Lcav8q06A0zPv@flaskapp.wqfsi.mongodb.net/?retryWrites=true&w=majority&appName=flaskApp")
db = client.shop_db #replace "app" with your database name. here db name is app
products_collection = db.products

@app.route('/')#homepage
def hello_world():  # put application's code here
    return render_template('home.html')

@app.route('/products')
def products():
    # getting all products from database
    products_list = list(products_collection.find())
    return render_template('products.html',products=products_list)

if __name__ == '__main__':
    app.run()


