import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = os.getenv('GITHUB_API_URL', 'https://api.github.com')  # Default API URL if not specified in .env
TOKEN = os.getenv('TOKEN')
ORG_NAMES = os.getenv('ORG_NAMES').split(',')  # Expects a comma-separated list of organization names
OUTPUT_CSV = 'github_stats.csv'

def get_repositories(org):
    url = f"{GITHUB_API_URL}/orgs/{org}/repos?type=all"
    headers = {'Authorization': f'token {TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()

def count_open_issues(repo):
    """Count open issues in a repository."""
    url = repo['issues_url'].replace('{/number}', '') + '?state=open'
    headers = {'Authorization': f'token {TOKEN}'}
    response = requests.get(url, headers=headers)
    return len(response.json())

def count_subscribers(repo):
    """Count the number of subscribers to a repository."""
    url = repo['subscribers_url']
    headers = {'Authorization': f'token {TOKEN}'}
    response = requests.get(url, headers=headers)
    return len(response.json())

def main():
    data_to_csv = []

    for org_name in ORG_NAMES:
        repositories = get_repositories(org_name)
        
        for repo in repositories:
            repo_stats = {
                'Organization': org_name,
                'Repository Name': repo['name'],
                'Stars': repo['stargazers_count'],
                'Forks': repo['forks_count'],
                'Open Issues': count_open_issues(repo),
                'Watchers': repo['watchers_count'],
                'Repository Size (KB)': repo['size'],
                'Network Count': repo['forks_count'],
                'Subscribers': count_subscribers(repo)
            }
            print(repo_stats)
            data_to_csv.append(repo_stats)
    
    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        fieldnames = ['Organization', 'Repository Name', 'Stars', 'Forks', 'Open Issues', 'Watchers', 
                      'Repository Size (KB)', 'Network Count', 'Subscribers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in data_to_csv:
            writer.writerow(data)

main()
