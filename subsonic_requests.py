import os
import base64
import hashlib
import requests

import const


def generate_token():
    salt = os.urandom(16)
    salt_encoded = str(base64.b64encode(salt))
    string_for_md5 = const.PASSWD + salt_encoded
    token = hashlib.md5(string_for_md5.encode('utf-8')).hexdigest()
    return (token, salt_encoded)


def get(path, extra_param=None):
    token, salt = generate_token()
    params = {'u': const.USER, 't': token, 's': salt, 'v': const.VERSION, 'c': const.CLIENT}
    if extra_param:
        params[extra_param['key']] = extra_param['value']
    response = requests.get(const.SERVER + "/rest/" + path, params=params)
    return response.text


def post(path, **kwargs):
    token, salt = generate_token()
    params = {'u': const.USER, 't': token, 's': salt, 'v': const.VERSION, 'c': const.CLIENT}
    params_merged = {**params, **kwargs}
    response = requests.post(const.SERVER + "/rest/" + path, params=params_merged)
    return response.text
