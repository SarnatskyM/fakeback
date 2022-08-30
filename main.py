import random
from urllib import request
from flask import Flask
from flask import request as req
import sqlite3 as sql
import json
from db import DB

app = Flask(__name__)

def valid(r):
    error = []

    try:
        card_number = r['card_number']
        card_cvv = r['card_cvv']
        card_gg = r['card_gg']
        card_mm = r['card_mm']
        if card_number is None or len(str(card_number)) < 16 or len(str(card_number)) > 16:
            raise Exception("Error")
        if card_cvv is None or len(str(card_cvv)) > 3 or len(str(card_cvv)) < 3:
            raise Exception("Error")
        if card_gg is None or len(str(card_gg)) < 2 or len(str(card_gg)) > 2:
            raise Exception("Error")
        if card_mm is None or len(str(card_mm)) < 2 or len(str(card_mm)) > 2:
            raise Exception("Error")
    except Exception as e:error.append("Fill in the example")

    return error


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True 
    return response

@app.route('/api/cards' , methods=["GET"])
def index():
    return DB().get_cards()


@app.route('/api/orderid' , methods=["GET"])
def order():
    uid = req.args.get("uid")
    request = {
        "merchant_id": random.randint(0,100),
        "order": random.randint(0,1000),
        "order_sum":random.randint(100,10000)
    }
    return request

@app.route('/api/new_card' , methods=["POST", "GET"])
def new_card():
    if req.method == "POST":
        request_data = json.loads(req.data.decode("utf-8"))
        resp  = valid(request_data)
        if len(resp) > 0:
            _ = {
                "status":"error",
                "message": resp
            }, 403
            return _
        elif not DB().exist_card(request_data['card_number']):
            DB().add_card(request_data['card_number'], request_data['card_cvv'], request_data['card_gg'], request_data['card_mm'])
            _ = {
                "status":"success"
            }, 200
            return _
        else:
            _ = {
                "status":"error",
                "message":"This is card already exist"
            }, 403
            return _


@app.route('/api/card' , methods=["POST"])
def card_item():
    request_data = json.loads(req.data.decode("utf-8"))
    return DB().get_card(request_data['id'])

if __name__  == "__main__":
    app.run()