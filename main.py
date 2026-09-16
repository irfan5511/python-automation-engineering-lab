import os
from dotenv import load_dotenv
import requests
from api_practice import  clean_all_repositories, save_report, summarize_repositories
from datetime import datetime, timezone
from retry_practice import get_with_retry
import logging
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def fetch_repositories(token):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    page = 1
    all_repositories = []
    while True:
        params = {
            "sort": "updated",
            "per_page": 5,
            "page": page
        }
        
        response = get_with_retry(
            url,
            headers= headers,
            params= params,
            timeout= 10,
            max_attempts=3
            )
        reset_timestamp = response.headers.get("x-ratelimit-reset")
        reset_time = datetime.fromtimestamp(
            int(reset_timestamp),
            tz= timezone.utc
        )
        logging.info(f"Rate limit resets: {reset_time}")

        remaining = int(response.headers.get("x-ratelimit-remaining"))
        if remaining <= 100:
            logging.warning(
                f"Only {remaining} API requests remaining")
        

        page_data= response.json()
        if not page_data:
                break
        all_repositories.extend(page_data)
        page += 1
    return all_repositories

    


def main():

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logging.error("Missing GitHub token")
        return

    
    logging.info("GitHub token loaded successfully")


    try:
        data= fetch_repositories(token)
        logging.info(f"Repositories returned: {len(data)}")
        if not data:
            logging.warning("No repositories found")
        else:
            cleaned_repositories= clean_all_repositories(data)
            summary = summarize_repositories(cleaned_repositories)
            report = {
                "summary": summary,
                "repositories": cleaned_repositories
            }
            save_report(
                report,
                "data/github_irfan_repositories.json")
            logging.info("Repository report saved successfully")


    except requests.HTTPError as error: 
        logging.error(f"HTTP error: {error}")

    except requests.Timeout as error:  
        logging.error(f"Request timed out: {error}")

    except requests.ConnectionError as error:
        logging.error(f"Connection error: {error}")

    except requests.RequestException as error:
        logging.error(f"Request failed: {error}")


if __name__ == "__main__":
    main()