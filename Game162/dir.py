import requests


def readdir():
    session = requests.Session()
    session.verify = False
    res = session.get('https://comsci.srru.ac.th/dir.php')
    print(res.status_code)
    if res.status_code == 200:
        data = res.json()
        for d in data:
            print(d['id'])


if __name__ == '__main__':
    readdir()
