import requests

def get_github_issue(owner, repo, issue_number, github_token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch issue. Status code: {response.status_code}")
        return None
