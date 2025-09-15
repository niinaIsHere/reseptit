import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request
from flask import session
import db
import config
import items, users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    if "user_id" in session:
        user_id = session["user_id"]
        db = sqlite3.connect("database.db")
        user_items = items.get_user_items(user_id)
        all_items = items.get_all_items()
        return render_template("start.html", all_items = all_items, items=user_items)
    else:
        return render_template("start.html")

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    item_tags = items.get_tags(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item, item_tags=item_tags)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    
    try:
        users.create_user(username, password1)
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
        
        user_id = users.check_login(username, password)

    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/page1")
def page1():
    session["test"] = "aybabtu"
    return "Istunto asetettu"

@app.route("/page2")
def page2():
    return "Tieto istunnosta: " + session["test"] + str(session["user_id"])

@app.route("/create_recipe")
def create_recipe():
    require_login()
    return render_template("create_recipe.html")

@app.route("/recipe_result", methods=["POST"])
def recipe_result():
    require_login()
    user_id = session["user_id"]
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    menu = request.form["menu"]
    skill = request.form["skill"]
    tags = request.form.getlist("tag")

    sql = """INSERT INTO recipes (user_id, title, description, menu, skill)
                VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, title, description, menu, skill])

    recipe_id = db.last_insert_id()
    for tag in tags:
        sql_tag = """INSERT INTO tags (recipe_id, tag) VALUES (?, ?)"""
        db.execute(sql_tag, [recipe_id, tag])

    return redirect("/")

@app.route("/edit/<int:item_id>")
def edit_recipe(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_recipe.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"]

    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)

    user_id = session["user_id"]
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    menu = request.form["menu"]
    skill = request.form["skill"]

    items.update_item(item_id, user_id, title, description, menu, skill)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if request.method == "GET":
        if not item:
            abort(404)
        if item["user_id"] != session["user_id"]:
            abort(403)
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/search_item", methods = ["GET"])
def find_item():
    require_login()
    query = request.args.get("query")
    if query:
        results = items.find_item(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/add_comment")
def add_comment():
    require_login()
    return render_template("add_comment.html")

@app.route("/comment_result", methods=["POST"])
def comment_result():
    require_login()
    comment = request.form["comment"]
    return render_template("comment_result.html", comment=comment)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    user_items = items.get_user_items(user_id)
    if not user:
        abort(403)
    return render_template("show_user.html", user=user, user_items=user_items)
