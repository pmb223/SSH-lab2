from datetime import datetime
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    user_ip = request.remote_addr 
    return render_template("index.html", user_ip=user_ip)


@app.route("/submit", methods=["POST"])
def submit():
    limit = request.form.get("limit")
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': 'gXQBPINhpfnVGodo0mvsVQ==CIUM07hamfCP4WzY'})
    if response.status_code == requests.codes.ok:
        fact_data = response.json()
    else:
        fact_data = response.status_code

    input_name = request.form.get("name")
    repos_response = requests.get(f"https://api.github.com/users/{input_name}/repos")
    repos_data = repos_response.json()



    repos_info = []
    code = repos_response.status_code
    if code == 200:
        for repo in repos_data:
            name = repo.get('name', 'N/A')
            url = repo.get('html_url', '#')
            updated_at = repo.get('updated_at', '')
            if updated_at:
                parsed_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = parsed_date.strftime("%B %d, %Y %H:%M:%S")
            else:
                formatted_date = 'N/A'

        
            commits_url = f"https://api.github.com/repos/{input_name}/{name}/commits"
            commits_response = requests.get(commits_url)
            latest_commit_hash = 'N/A'
            latest_commit_author = 'N/A'
            latest_commit_date = 'N/A'
            latest_commit_message = 'N/A'
            if commits_response.status_code == 200:
                commits_data = commits_response.json()
                if commits_data:  
                    latest_commit = commits_data[0]  
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
        if code == 403:
            repos_info[0]['name'] = "Too many requests. Try again later."
    joke_response = requests.get("https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit")
    if joke_response.status_code == 200:
        joke_data = joke_response.json()
        if "joke" in joke_data:
            joke = joke_data["joke"]
        elif "setup" in joke_data:
            joke = joke_data["setup"] + " " + joke_data["delivery"]
        else:
            joke = "Joke not found."
    else:
        joke = "Joke API request failed. Try again later."

    return render_template("hello.html", name=input_name, repos_info=repos_info, joke=joke, fact_data=fact_data)

if __name__ == "__main__":
    app.run(debug=True)

