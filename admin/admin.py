from flask import Blueprint, request, redirect, url_for, flash, render_template, session

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

from main import Item, db, render_picture


def login_admin():
    session['admin_logged'] = 1  # функція створює запис в сесії 'admin_logged'. Дальше припускаю якщо такий запис існує, то адміністратор залогінений.


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [{'url': 'index', 'title': 'Магазин'},
        {'url': '.index', 'title': 'Панель'},
        {'url': '.create', 'title': 'Додати новий товар'},
        {'url': '.logout', 'title': 'Вийти'}

        ]


@admin.route("/")
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    items = Item.query.order_by(Item.id).all()
    return render_template('admin/index.html', menu=menu, data=items, title='Адмін-панель')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for(".index"))
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Пара Логін/Пароль є невірною", "error")

    return render_template('admin/login.html', title='Панель адміністратора')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))


@admin.route('/create', methods=["POST", "GET"])
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
        return render_template("admin/create.html", title='Додати товар', menu=menu)


@admin.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    item_to_update = Item.query.get_or_404(id)
    if request.method == "POST":
        item_to_update.title = request.form['title']
        item_to_update.price = request.form['price']
        item_to_update.length = request.form['length']
        item_to_update.width = request.form['width']
        item_to_update.thickness1 = request.form['thickness1']
        item_to_update.thickness2 = request.form['thickness2']
        item_to_update.quantity = request.form['quantity']
        file = request.files['inputFile']
        item_to_update.data = file.read() or item_to_update.data
        item_to_update.rendered_data = render_picture(item_to_update.data)



        try: # зберігаю item як новий запис в БД
            db.session.commit()
            return redirect('/admin')
        except:
            return "Виникла помилка"

    else:
        return render_template("/admin/update.html", title='Редагувати товар', item_to_update=item_to_update)

