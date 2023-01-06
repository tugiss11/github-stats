import json
import os
import requests


def store_contributions(username, access_token, start_date, end_date):
    base_url = "https://api.github.com/graphql"
    query = """
    query($username: String!, $start_date: DateTime, $end_date: DateTime) {
    user(login: $username) {
        contributionsCollection(from: $start_date, to: $end_date) {
        contributionCalendar {
            totalContributions
            weeks {
            contributionDays {
                contributionCount
                date
            }
            }
        }
        }
    }
    }
    """

    variables = {"username": username, "start_date": start_date, "end_date": end_date}
    headers = {"Authorization": f"bearer {access_token}"}
    payload = {"query": query, "variables": variables}
    response = requests.post(base_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        with open("data/contributions.json", "w") as f:
            json.dump(data, f)
    else:

        print(f"Failed to fetch contributions: {response.status_code}")


def store_commits(username: str, access_token: str, start_date, end_date):
    all_commits = []
    page = 1
    commits = get_commits(username, access_token, start_date, end_date, page)
    all_commits += commits
    while len(commits) == 100:
        page += 1
        commits = get_commits(username, access_token, start_date, end_date, page)
        all_commits += commits

    with open("data/commits.json", "w") as f:
        json.dump(all_commits, f)


def get_commits(username: str, access_token: str, start_date, end_date, page):
    url = f"https://api.github.com/search/commits?q=author:{username}+author-date:{start_date}..{end_date}&page={page}&per_page=100"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    with open("data/test.json", "w") as f:
        json.dump(data, f)
    print(data["incomplete_results"])
    return [item["commit"] for item in data["items"]]


def main():
    print("Starting main() in fetch_data.py")
    access_token = os.environ["GITHUB_PAT"]
    username = os.environ["GITHUB_USERNAME"]
    year = 2022
    start_date = f"{year}-01-01T00:00:00Z"
    end_date = f"{year}-12-31T23:59:59Z"
    # store_contributions(username, access_token, start_date, end_date)
    store_commits(username, access_token, start_date, end_date)


if __name__ == "__main__":
    main()
