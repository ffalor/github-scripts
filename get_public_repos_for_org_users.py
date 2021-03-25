from github import Github
from tabulate import tabulate
import csv
import argparse
import time
import datetime

start_time = time.time()
parser = argparse.ArgumentParser()

parser.add_argument("token", help="Github Token for Auth", type=str)
parser.add_argument("org", help="Github Org to Check", type=str)
parser.add_argument("--path", help="Output path for report",
                    type=str, default="./")

args = parser.parse_args()

# Base url to build repo url
GITHUB_BASE_URL = "https://github.com"

g = Github(args.token)

org = g.get_organization(args.org)
org.login

members = org.get_members()

repo_report_data = []
repo_report_headers = ["User", "Repo Name", "Repo URL"]

user_report_data = []
user_report_headers = ["User", "Public Repo Count"]

members_wo_public_repos = []
members_w_public_repos = []
total_public_repos = 0

for member in members:
    public_repo_count = member.public_repos
    member_login = member.login

    if public_repo_count > 0:

        members_w_public_repos.append(member_login)
        total_public_repos += public_repo_count

        repo_names = []
        repo_urls = []

        for repo in member.get_repos():
            repo_report_data.append({
                "User": member_login,
                "Repo Name": repo.name,
                "Repo URL": f"{GITHUB_BASE_URL}/{repo.full_name}"
            })
            user_report_data.append({
                "User": member_login,
                "Public Repo Count": public_repo_count
            })
    else:
        members_wo_public_repos.append(member_login)

# Write report to CSV
if repo_report_data != []:
    with open(f"{args.path}/repo_report.csv", mode="w", newline='') as csv_file:
        dict_writer = csv.DictWriter(csv_file, repo_report_headers)
        dict_writer.writeheader()
        dict_writer.writerows(repo_report_data)
    print("Repo report created at: ", f"{args.path}repo_report.csv")

# Write report to CSV
if repo_report_data != []:
    with open(f"{args.path}/user_report.csv", mode="w", newline='') as csv_file:
        dict_writer = csv.DictWriter(csv_file, user_report_headers)
        dict_writer.writeheader()
        dict_writer.writerows(user_report_data)
    print("User report created at: ", f"{args.path}user_report.csv")
        
print("\n", "#"*35, "SUMMARY", "#"*35)
print(tabulate([[len(members_wo_public_repos), len(
    members_w_public_repos), total_public_repos]], headers=["Members w/o public repos", "Members w public repos", "Total Public Repos"], tablefmt="fancy_grid"))

print("\nTime to Process:", str(datetime.timedelta(
    seconds=(time.time() - start_time))))
