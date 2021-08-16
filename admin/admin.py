from flask import Blueprint, request, redirect, url_for, flash, render_template, session

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


def login_admin():
    session['admin_logged'] = 1  # функція створює запис в сесії 'admin_logged'. Дальше припускаю якщо такий запис існує, то адміністратор залогінений.


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route("/")
def index():
    return "admin"


@admin.route('/login', methods=["POST", "GET"])
def login():
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
