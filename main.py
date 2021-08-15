from flask import Flask, render_template, request, redirect, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

import os
from datetime import datetime
from base64 import b64encode
import base64
from io import BytesIO

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    length = db.Column(db.String(100), nullable=False)
    width = db.Column(db.String(100), nullable=False)
    thickness1 = db.Column(db.String(100), nullable=False)
    thickness2 = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    rendered_data = db.Column(db.Text, nullable=False)

    isActive = db.Column(db.Boolean, default=True)
    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Назва товару: {self.title}, Ціна: {self.price} Довжина: {self.length} Ширина: {self.width} Товщина: від {self.thickness1} до {self.thickness2} Кількість: {self.quantity} Зображення: {self.data}"


@app.route('/')
def index():
    items=Item.query.order_by(Item.price).all()  #будемо отримувати всі товари з таблиці Item і виводити в index.html
    return render_template("index.html", data=items)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/buy/<int:id>')
def item_buy(id):
    item=Item.query.get(id) #по id вибираю запис з таблиці і передаю в словник data значення поля "ціна"

    api = Api(merchant_id=1397120,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        length = request.form['length']
        width = request.form['width']
        thickness1 = request.form['thickness1']
        thickness2 = request.form['thickness2']
        quantity = request.form['quantity']
        file = request.files['inputFile']
        data = file.read()
        render_file = render_picture(data)

        item = Item(title=title, price=price, length=length, width=width,
                    thickness1=thickness1, thickness2=thickness2, quantity=quantity,
                    data=data, rendered_data=render_file)
        try: # зберігаю item як новий запис в БД
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Виникла помилка"

    else:
        return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True)