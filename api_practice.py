import json
import requests
from timedate_practice import get_activity_status
from datetime import datetime, timezone

def clean_repository(repo):
    clean_repo = {
        "full_name" : repo['full_name'],
        "language" : repo['language'] or "Unknown",
        "html_url" : repo['html_url'],
        "pushed_at" : repo['pushed_at'],
        "activity_status": get_activity_status(repo["pushed_at"]),
         "open_issues_count": repo["open_issues_count"],
        "forks_count" : repo ['forks_count'],
        "stargazers_count" : repo['stargazers_count']
       }
        
    return clean_repo


def fetch_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    params = {
    "sort": "updated",
    "per_page": 5
    }
    response = requests.get(
        url,
        params=params,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def save_report(repositories, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(repositories, file, indent=4)


def clean_all_repositories(repositories):
    clean_repositories = []
    for repo in repositories:
        clean_repo = clean_repository(repo)
        clean_repositories.append(clean_repo)
    return clean_repositories


def main():
    username = input("Enter GitHub username:").strip()



    try:
        data = fetch_repositories(username)
        if not data:
            print("No repositories found")
        else:
            cleaned_repositories = clean_all_repositories(data)

            save_report(
                cleaned_repositories, 
                "data/github_repositories.json"
                )
            print("Repository report saved successfully.")

        
            

    except requests.HTTPError as error:
        print(f"HTTP error: {error}")

    except requests.Timeout as error:  
        print(f"Request timed out: {error}")

    except requests.ConnectionError as error:
        print(f"Connection error: {error}")

    except requests.RequestException as error:
        print(f"Request failed: {error}")

if __name__ == "__main__":
    main()
    