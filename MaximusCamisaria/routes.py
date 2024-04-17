
from flask import render_template, url_for
from MaximusCamisaria import app

@app.route("/")
def homepage():
    return render_template("home.html")