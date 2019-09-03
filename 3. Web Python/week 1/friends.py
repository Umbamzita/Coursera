import requests
import collections
from operator import itemgetter


def calc_age(uid):
    result = []

    ACCESS_TOKEN = '97cf5ffc97cf5ffc97cf5ffc3d97a3f5a9997cf97cf5ffccaa23971fd9ccb98d51309bf'
    url_id = f'https://api.vk.com/method/users.get?v=5.71&access_token={ACCESS_TOKEN}&user_ids={uid}'
    r = requests.get(url_id).json()
    id = r['response'][0]['id']

    url_friends = f'https://api.vk.com/method/friends.get?v=5.71&access_token={ACCESS_TOKEN}&user_id={id}&fields=bdate'
    get_friends = requests.get(url_friends).json()

    #return get_friends['response']['items']

    for x in get_friends['response']['items']:
        date = str(x.get('bdate', 0))
        d = date.split('.')
        if int(d[-1]) > 100:
            result.append(2019 - int(d[-1]))

    d=collections.Counter(result).most_common()
    return sorted(d, key=lambda x: (-x[1], x[0]))


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)