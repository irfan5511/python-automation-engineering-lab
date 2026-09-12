import os
from dotenv import load_dotenv
import requests
from api_practice import  clean_all_repositories, save_report
load_dotenv()


def fetch_repositories(token):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    params = {
        "sort": "updated",
        "per_page": 5
    }
    response = requests.get(
        url,
        headers= headers,
        params= params,
        timeout= 10
        )
    response.raise_for_status()
    return response.json()


def main():

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Missing GitHub token")
        return

    
    print("GitHub token loaded successfully")


    try:
        data= fetch_repositories(token)
        if not data:
            print("No repositories found")
        else:
            cleaned_repositories= clean_all_repositories(data)
            save_report(
                cleaned_repositories,
                "data/github_irfan_repositories.json")
            print("Repository report saved successfully")


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