import json
from datetime import datetime


def read_contributions(filename: str) -> dict:
    """Read the contribution data from a JSON file."""
    with open(filename, "r") as f:
        data = json.load(f)
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"][
        "weeks"
    ]


def read_commits(filename: str) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def count_contributions_per_weekday(contributions: dict):
    """Count the number of contributions per weekday."""
    weekday_stats = [
        {
            "name": weekday_name,
            "total_contributions": 0,
            "days_with_contributions": 0,
            "days_without_contributions": 0,
        }
        for weekday_name in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    ]
    for week in contributions:
        for contribution_day in week["contributionDays"]:
            weekday_number = datetime.strptime(
                contribution_day["date"], "%Y-%m-%d"
            ).weekday()
            weekday_stats[weekday_number]["total_contributions"] += contribution_day[
                "contributionCount"
            ]
            if contribution_day["contributionCount"] > 0:
                weekday_stats[weekday_number]["days_with_contributions"] += 1
            else:
                weekday_stats[weekday_number]["days_without_contributions"] += 1

    return weekday_stats


def print_contributions_stats(weekday_counts):
    days_with_contributions = sum(
        [item["days_with_contributions"] for item in weekday_counts]
    )
    total_contributions = sum([item["total_contributions"] for item in weekday_counts])
    print(
        f"During the year I made total of {total_contributions} contributions on {days_with_contributions} days"
    )
    print("Avg contributions per weekday:")
    for item in sorted(
        weekday_counts, key=lambda x: x["total_contributions"], reverse=True
    ):
        print(f"{item['name']}: {item['total_contributions']/52:.2f}")
    print("Days with Github contributions and (without):")
    for item in sorted(
        weekday_counts, key=lambda x: x["days_with_contributions"], reverse=True
    ):
        print(
            f"{item['name']}: {item['days_with_contributions']} ({item['days_without_contributions']})"
        )


def count_commits_per_hour(commits):
    print(f"Total number of commits made during the year: {len(commits)}")
    commits_per_hour = {i: 0 for i in range(25)}
    for commit in commits:
        date = datetime.strptime(commit["committer"]["date"], "%Y-%m-%dT%H:%M:%S.%f%z")
        commits_per_hour[date.hour] += 1
    print("Commits made by hour:")
    for key in commits_per_hour.keys():
        print(f"{key}: {commits_per_hour[key]}")


def main():
    print("Starting main() in parse_files.py")
    contributions = read_contributions("data/contributions.json")
    weekday_counts = count_contributions_per_weekday(contributions)
    print_contributions_stats(weekday_counts)
    commits = read_commits("data/commits.json")
    count_commits_per_hour(commits)


if __name__ == "__main__":
    main()
