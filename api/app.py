import requests

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello_world():
    user_ip = request.remote_addr  # Get the user's IP address
    return render_template("index.html", user_ip=user_ip)

@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    user_ip = request.remote_addr  # Get the user's IP address
    return render_template("hello.html", name=input_name, age=input_age, user_ip=user_ip)

response = requests.get(“https://api.github.com/users/pmb223/repos”)
if response.status_code == 200:
    repos = response.json() # data returned is a list of ‘repository’ entities
    for repo in repos:
        print(repo[“full_name”])
