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
    repos_response = requests.get(f"https://api.github.com/users/{input_name}/repos")
    repos_data = repos_response.json()

    repos_info = []
    if repos_response.status_code == 200:
        for repo in repos_data:
            name = repo.get('name', 'N/A')
            url = repo.get('html_url', '#')
            updated_at = repo.get('updated_at', '')
            if updated_at:
                parsed_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = parsed_date.strftime("%B %d, %Y %H:%M:%S")
            else:
                formatted_date = 'N/A'

            # Get the latest commit for this repo
            commits_url = f"https://api.github.com/repos/{input_name}/{name}/commits"
            commits_response = requests.get(commits_url)
            latest_commit_hash = 'N/A'
            latest_commit_author = 'N/A'
            latest_commit_date = 'N/A'
            latest_commit_message = 'N/A'
            if commits_response.status_code == 200:
                commits_data = commits_response.json()
                if commits_data:  # Check if there is at least one commit
                    latest_commit = commits_data[0]  # Get the latest commit
                    latest_commit_hash = latest_commit.get('sha', 'N/A')
                    if 'commit' in latest_commit:
                        latest_commit_author = latest_commit['commit']['author']['name']
                        latest_commit_date = latest_commit['commit']['author']['date']
                        latest_commit_date = datetime.strptime(latest_commit_date, "%Y-%m-%dT%H:%M:%SZ")
                        latest_commit_date = latest_commit_date.strftime("%B %d, %Y %H:%M:%S")
                        latest_commit_message = latest_commit['commit']['message']

            repo_info = {
                'name': name,
                'url': url,
                'updated_at': formatted_date,
                'latest_commit_hash': latest_commit_hash,
                'latest_commit_author': latest_commit_author,
                'latest_commit_date': latest_commit_date,
                'latest_commit_message': latest_commit_message
            }
            repos_info.append(repo_info)
    else:
        repos_info = [{'name': "Account not found", 'url': '#', 'updated_at': 'N/A', 'latest_commit': {}}]

    return render_template("hello.html", name=input_name, repos_info=repos_info)

if __name__ == "__main__":
    app.run(debug=True)

