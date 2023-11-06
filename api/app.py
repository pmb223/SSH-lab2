from datetime import datetime
from flask import Flask, render_template, request
import requests

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
        repos = response.json()  # Data returned is a list of ‘repository’ entities
    else:
        repos = [{"name": "Account not found"}]  # Ensure keys are used for consistency

    repo_names = []
    repo_urls = []
    repo_updated_at = []

    for r in repos:
        repo_names.append(r.get('name', 'N/A'))  # Provide a default value in case 'name' is not present
        repo_urls.append(r.get('html_url', '#'))  # 'html_url' is the URL to the repository on GitHub
        updated_at = r.get('updated_at', '')
        if updated_at:
            # Parse the date string and reformat it
            parsed_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = parsed_date.strftime("%B %d, %Y %H:%M:%S")  # E.g., "October 09, 2023 15:06:21"
            repo_updated_at.append(formatted_date)
        else:
            repo_updated_at.append('N/A')

    return render_template("hello.html", name=input_name, rnames=repo_names, rurls=repo_urls, rupdated=repo_updated_at)

if __name__ == "__main__":
    app.run(debug=True)
