import os
import base64
import hashlib
import requests

import common


def generate_token():
    salt = os.urandom(16)
    salt_encoded = str(base64.b64encode(salt))
    string_for_md5 = common.PASSWD + salt_encoded
    token = hashlib.md5(string_for_md5.encode('utf-8')).hexdigest()
    return (token, salt_encoded)


def get(path, extra_param=None):
    token, salt = generate_token()
    params = {'u': common.USER, 't': token, 's': salt, 'v': common.VERSION, 'c': common.CLIENT}
    if extra_param:
        params[extra_param['key']] = extra_param['value']
    response = requests.get(common.SERVER + "/rest/" + path, params=params)
    return response.text


def post(path, **kwargs):
    token, salt = generate_token()
    params = {'u': common.USER, 't': token, 's': salt, 'v': common.VERSION, 'c': common.CLIENT}
    params_merged = {**params, **kwargs}
    response = requests.post(common.SERVER + "/rest/" + path, params=params_merged)
    return response.text
