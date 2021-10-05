import requests
import json

username = 'mfsov'
url = f'https://api.github.com/users/{username}'
user_data = requests.get(url).json()
user_repos = requests.get(f'{url}/repos').json()
with open('homework_1_1.json', 'w') as f:
    json.dump(user_repos, f)
with open('homework_1_1.json') as saved:
    repos_list = json.load(saved)
for repo in repos_list:
    print(repo['name'], repo['html_url'])

token = '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'
repos = requests.get('https://api.github.com/user/repos', auth=(username, token)).json()
for repo in repos:
    if repo['private']:
        print(repo['name'], repo['html_url'])
repotoshow = 'gbprivaterepo1'
commits = requests.get(f'https://api.github.com/repos/{username}/{repotoshow}/commits', auth=(username, token)).json()
with open('homework_1_2.json', 'w') as f:
    json.dump(commits, f)
with open('homework_1_2.json') as saved:
    commits_list = json.load(saved)
for el in commits_list:
    print(el['commit']['message'])
