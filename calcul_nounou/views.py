from flask import render_template
from app import app

@app.route("/")
def homepage():
    return render_template('register_day.html')


@app.route("/seeDetails")
def seeDetails():
    return render_template('see_details.html')