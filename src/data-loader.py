import json

users = []

with open('../data/github-data.json', 'r') as f:
    db = json.load(f)

for item in db:
    for follower in item['followers']:
        user = {
            'id': follower['id'],
            'name': follower['login'],
            'followers_url': follower['followers_url'],
            'followers': []
        }
        if follower not in users:
            users.append(user)

print(users)

for user in users:
    url = user['followers_url']
    followers = []
    for item in db:
        if url == item['url']:
            for follower in item["followers"]:
                followers.append(follower['id'])
            break
    print(user)
    user['followers'] += followers

with open("../data/github-follower-graph.json", "w") as json_file:
    json_file.write(json.dumps(users, indent=4, separators=(',', ': ')))
