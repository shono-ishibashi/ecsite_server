from unittest import mock
import requests
import json


def create_mock(user_pk):
    mock_res = requests.Response()
    mock_res.status_code = 201
    user = {
        "user": {
            "id": user_pk
        }
    }
    user = json.dumps(user).encode('utf-8')
    mock_res._content = user
    my_mock = mock.MagicMock(return_value=mock_res)
    return my_mock
