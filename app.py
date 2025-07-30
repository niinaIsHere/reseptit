from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Heipparallaa!"

@app.route("/create_recipe")
def create_recipe():
    return render_template("create_recipe.html")

