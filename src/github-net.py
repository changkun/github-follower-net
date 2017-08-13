import json
import requests
import configparser


class Spider(object):
    def __init__(self, auth_user, auth_pass, degree):
        self.step = degree
        self.cache = ['https://api.github.com/users/' +
                      auth_user + '/followers']
        self.auth = {
            'user': auth_user,
            'pass': auth_pass
        }
        self.db = '../data/github-data.json'

    def get_followers(self, url):
        params = {
            'per_page': 100,
            'page': 1
        }
        data = []
        while True:
            resp = requests.get(url=url, auth=(
                self.auth['user'], self.auth['pass']), params=params)
            temp = json.loads(resp.text)
            # rate limite
            if type(temp) == type(dict()):
                if 'message' in temp:
                    break
            # if not empty, continue request get
            if temp:
                params['page'] += 1
                data += temp
            else:
                break
        return data

    def creeper(self, depth):

        if depth < 1:
            return

        # iterate follower in cache, initial cache contains the first user
        cache = self.cache[:]
        for item in cache:
            print('START:' + item)
            # fetch all follower under the url
            data = self.get_followers(item)
            # construct user object
            user = {
                "url": item,
                "followers": data
            }
            # store the user object into database (json file)
            # TODO: optimize here
            with open(self.db, "r") as json_file:
                db = json.load(json_file)
            if user not in db:  # only consider new user
                db.append(user)
                with open(self.db, "w") as json_file:
                    json_file.write(json.dumps(
                        db, indent=4, separators=(',', ': ')))
            # push all new follower url into CACHE
            for follower in data:
                self.cache.append(follower["followers_url"])
            # clear this item in CACHE, make sure no repetition
            while item in self.cache:
                self.cache.remove(item)
            print('FINISH: ' + item)

        print('depth ' + str(depth) + ' finished...')
        self.creeper(depth - 1)


def main():
    # load config
    config = configparser.ConfigParser()
    config.read('../data/config.ini')
    username = config.get('AUTH', 'username')
    password = config.get('AUTH', 'password')
    degree = config.get('SPIDER', 'degree')

    # create spider object
    spider = Spider(username, password, degree)


if __name__ == '__main__':
    main()
