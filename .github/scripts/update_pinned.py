import os
import re
import requests

token = os.environ["GH_TOKEN"]
username = "Rizz404"

query = """
{
  user(login: "%s") {
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          url
          description
          stargazerCount
          forkCount
          primaryLanguage {
            name
          }
        }
      }
    }
  }
}
""" % username

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers={"Authorization": f"Bearer {token}"}
)

repos = response.json()["data"]["user"]["pinnedItems"]["nodes"]

cards = []
for repo in repos:
    name = repo["name"]
    card_url = (
        f"https://github-readme-stats-pi-rouge-87.vercel.app/api/pin/"
        f"?username={username}&repo={name}"
        f"&theme=react&bg_color=1F1020&title_color=C8004A"
        f"&hide_border=true&icon_color=F0C800"
    )
    cards.append(
        f'  <a href="{repo["url"]}">\n'
        f'    <img width="278" src="{card_url}" alt="{name}"/>\n'
        f'  </a>'
    )

new_content = '<p align="left">\n' + "\n".join(cards) + "\n</p>"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

new_readme = re.sub(
    r"<!-- PINNED_REPOS_START -->.*?<!-- PINNED_REPOS_END -->",
    f"<!-- PINNED_REPOS_START -->\n{new_content}\n<!-- PINNED_REPOS_END -->",
    readme,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print(f"Updated {len(repos)} pinned repos!")
