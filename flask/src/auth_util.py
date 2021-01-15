import requests


def fetch_login_user(token):
    url = 'http://nginx:80/auth/user/'
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    return response
