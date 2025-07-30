import requests

def get_github_issue(owner, repo, issue_number, token=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {token}"} if token else {}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Failed to fetch issue: {response.status_code}",
            "details": response.text
        }
