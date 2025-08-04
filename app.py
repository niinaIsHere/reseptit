from flask import Flask
from flask import render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("start.html")

@app.route("/create_recipe")
def create_recipe():
    return render_template("create_recipe.html")

@app.route("/recipe_result", methods=["POST"])
def recipe_result():
    recipe = request.form["recipe"]
    menu = request.form["menu"]
    diet = request.form["diet"]
    skill = request.form["skill"]
    return render_template("recipe_result.html", recipe=recipe, menu=menu, diet=diet, skill=skill)

@app.route("/add_comment")
def add_comment():
    return render_template("add_comment.html")

@app.route("/comment_result", methods=["POST"])
def comment_result():
    comment = request.form["comment"]
    return render_template("comment_result.html", comment=comment)
