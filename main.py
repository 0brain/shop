from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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

    isActive = db.Column(db.Boolean, default=True)
    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Запис: {self.title}"

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

    api = Api(merchant_id=,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": item.price
    }
    url = checkout.url(data).get('checkout_url')
    return id


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

        item = Item(title=title, price=price, length=length, width=width,
                    thickness1=thickness1, thickness2=thickness2, quantity=quantity)
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