import requests


def fetch_login_user(token):
    url = 'https://reacthon-pizza.tk/auth/user/'
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    return response
