from dataclasses import dataclass
from flask import Flask, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

import requests
from sqlalchemy import UniqueConstraint

from producer import publish

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
db = SQLAlchemy(app)
Migrate(app, db)
CORS(app)
app.app_context().push()


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products/')
def index():
    return jsonify(Product.query.all())


@app.route('/api/product/<int:id>/like/', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user/')
    json = req.json()
    try:
        product_user = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        publish('product_liked', id)
        return jsonify({
            'message': 'success'
        })
    except Exception as e:
        abort(400, 'You already liked this product')


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
