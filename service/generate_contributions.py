# generate_contributions.py

import requests
import datetime
import matplotlib.pyplot as plt
import os


def get_user_contributions(username, token):
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/users/{username}/events"

    response = requests.get(url, headers=headers)  
    if response.status_code == 200:
        events = response.json()
        contributions = [0] * 365
        for event in events:
            if event["type"] == "PushEvent":
                date_str = event["created_at"][:10]
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                day_of_year = date.timetuple().tm_yday - 1  # tm_yday is 1-indexed
                contributions[day_of_year] += len(event["payload"]["commits"])
        return contributions
    else:
        print(f"Failed to fetch contributions for {username}")
        return []


def plot_contributions(contributions, output_file):
    plt.plot(contributions, color="green")
    plt.xlabel("Day of the Year")
    plt.ylabel("Number of Contributions")
    plt.title("GitHub Contributions")
    # plt.show()
    plt.savefig(output_file)
    plt.close()

def main():
    username = "WangYingJay"
    token = os.environ.get('GITHUB_TOKEN')
    contributions = get_user_contributions(username, token)
    if contributions:
        # plot_contributions(contributions)
        output_directory = ''
        output_file = os.path.join(output_directory, "contributions.png")
        plot_contributions(contributions, output_file)


if __name__ == "__main__":
    main()
