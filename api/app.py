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
    response = requests.get(f"https://api.github.com/users/{input_name}/repos")
    if response.status_code == 200:
        repos = response.json() # data returned is a list of ‘repository’ entities
    else:
        repos = [{"Name", "Account not found"}]
    repo_names = []
    repo_url = []
    repo_updated_at = []
    for r in repos:
        repo_names.append(r['name'])
        repo_url.append(r['url'])
        repo_updated_at.append(r['updated_at'])
    return render_template("hello.html", name=input_name, rnames = repo_names, rurl = repo_url, rupdated = repo_updated_at)
