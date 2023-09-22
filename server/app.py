#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    serialized_bakeries = [bakery.to_dict() for bakery in bakeries]
    
    response = make_response(
        jsonify(serialized_bakeries),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return ''

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        serialized_bakery = bakery.to_dict(nested=['baked_goods'])
        return jsonify(serialized_bakery)
    else:
        return jsonify({"message": "Bakery not found"}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    serialized_baked_goods = [good.to_dict() for good in baked_goods]
    return jsonify(serialized_baked_goods)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return jsonify(baked_good.to_dict())
    else:
        return jsonify({"message": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
