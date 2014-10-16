from flask import Flask, request
from flask.ext.pymongo import PyMongo
import json
import sys

app = Flask(__name__)
mongo = PyMongo(app)
order_fields = ['name', 'note', 'cost']


@app.route('/orders', methods=['GET'])
def orders():
    orders = []
    for order in mongo.db.orders_app.orders.find():
        d = {'id': str(order['_id'])}
        for field in order_fields:
            d[field] = order[field]
        orders.append(d)
    return json.dumps(orders)


@app.route('/addOrder/<int:order_id>', methods=['POST'])
def add_order(order_id):
    data = {'_id': order_id}
    for field in order_fields:
        data[field] = request.form[field]

    try:
        mongo.db.orders_app.orders.insert(data)
        return '', 200
    except:
        return '', 500


@app.route('/deleteOrder/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    try:
        mongo.db.orders_app.orders.remove({'_id': order_id})
        return '', 200
    except:
        return '', 500


if __name__ == '__main__':
    app.debug = True
    host = '127.0.0.1'
    port = 5000
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except:
        pass
    app.run(host, port)
