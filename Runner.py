import requests
import re

def get_starred_repositories(username):
    url = f"https://api.github.com/users/{username}/starred"
    page = 1
    repositories = []
    total_pages = 1
    
    while page <= total_pages:
        params = {"page": page, "per_page": 100}  # Retrieve 100 repositories per page
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Extract total pages from the 'Link' header
            link_header = response.headers.get('Link')
            if link_header:
                matches = re.findall(r'page=(\d+)', link_header)
                if matches:
                    total_pages = max(int(page_num) for page_num in matches)

            page_repositories = response.json()
            if not page_repositories:
                break  # No more repositories to retrieve
            repositories.extend(page_repositories)
            page += 1
        else:
            print("Error fetching repositories.")
            break

    return repositories

# Replace 'YOUR_USERNAME' with your actual GitHub username
username = 'YOUR_USERNAME'

starred_repositories = get_starred_repositories(username)
if starred_repositories:
    print(f"Starred repositories for {username}:")
    for repo in starred_repositories:
        print(f"- {repo['name']} ({repo['html_url']})")
else:
    print(f"No starred repositories found for {username}.")
