import sqlite3
from flask import Flask
from flask import redirect, render_template, request
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    db = sqlite3.connect("databse.db")
    return render_template("start.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/page1")
def page1():
    session["test"] = "aybabtu"
    return "Istunto asetettu"

@app.route("/page2")
def page2():
    return "Tieto istunnosta: " + session["test"]

@app.route("/create_recipe")
def create_recipe():
    return render_template("create_recipe.html")

@app.route("/recipe_result", methods=["POST"])
def recipe_result():
    recipe = request.form["recipe"]
    description = request.form["description"]
    menu = request.form["menu"]
    diet = request.form["diet"]
    skill = request.form["skill"]
    return render_template("recipe_result.html", recipe=recipe, description=description, menu=menu, diet=diet, skill=skill)

@app.route("/add_comment")
def add_comment():
    return render_template("add_comment.html")

@app.route("/comment_result", methods=["POST"])
def comment_result():
    comment = request.form["comment"]
    return render_template("comment_result.html", comment=comment)

