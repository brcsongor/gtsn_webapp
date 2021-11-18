from flask import Flask, request, render_template, make_response, redirect, url_for, session
import random as r
from model import User, Pontok, db
import hashlib

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "Cidsa"
db.create_all()


def hash(str):
    return hashlib.md5(str.encode("UTF-8")).hexdigest()


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/new")
def new_user():
    return render_template("register.html")


@app.route("/register,", methods=["POST"])
def register():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-pw")
    try:
        create_user(name, email, password)
        return redirect(url_for("login"))
    except:
        return "Szerveroldali hiba történt! :("


@app.route("/login", methods=["POST", "GET"])
def log_user_in():
    if session.get('logged_in'):
        if session['logged_in']:
            return redirect("/start")
    else:
        user = request.form.get("user-name")
        password = request.form.get("user-pw")
        check_login = check_user_login(user,password)
        if check_login is not None:
            session["logged_in"] = True
            session["userid"] = check_login.id
@app.route("/start", methods=["POST", "GET"])
def start():
    return "Sikeresen beléptél!"


# CRUDE függvények: create, read, update, delete
def create_user(name, email, password):
    hash_pw = hash(password)
    add_user = User(name=name, email=email, password=hash_pw)
    db.add(add_user)
    db.commit()
def check_user_login(user,password):
    login = db.query(User).filter_by(name=user, password=hash(password)).first()
    return login
if __name__ == '__main__':
    app.run()