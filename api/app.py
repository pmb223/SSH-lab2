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
    response = requests.get("https://api.github.com/users/{username}/repos".format(input_name))
    if response.status_code == 200:
        repos = response.json() # data returned is a list of ‘repository’ entities
    else:
        repos = ["Account not found", None]
    return render_template("hello.html", name=input_name, user_repos = repos)


