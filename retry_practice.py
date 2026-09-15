import time
import requests


def get_with_retry(url, headers=None, params=None, timeout=10, max_attempts=3):

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=timeout
            ) 
            response.raise_for_status()

            print("Request succeeded")
            return response

        except (requests.Timeout, requests.ConnectionError) as error:
            print(f"Attempt {attempt} failed {error}")
            if attempt < max_attempts:
                wait_time = 2 ** (attempt - 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
        except requests.HTTPError as error:
            status_code = error.response.status_code
            print(f"Attempt {attempt} failed with HTTP {status_code}")
            if status_code in [429, 500, 502, 503, 504]:
                if attempt < max_attempts:
                    wait_time = 2 ** (attempt - 1)
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise
def main():
    response = get_with_retry(
        "https://httpbin.org/status/503",
        max_attempts=3
    )

if __name__ == "__main__":
    main()