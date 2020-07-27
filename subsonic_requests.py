import os
import base64
import hashlib
import requests

VERSION = os.environ.get('SSC_APIVERSION')
SERVER = os.environ.get('SSC_SERVER').rstrip('/')
USER = os.environ.get('SSC_USER')
PASSWD = os.environ.get('SSC_PASSWD')
CLIENT = 'subsonic_scripts'


def generate_token():
    salt = os.urandom(16)
    salt_encoded = str(base64.b64encode(salt))
    string_for_md5 = PASSWD + salt_encoded
    token = hashlib.md5(string_for_md5.encode('utf-8')).hexdigest()
    return (token, salt_encoded)


def get(path, extra_param=None):
    token, salt = generate_token()
    params = {'u': USER, 't': token, 's': salt, 'v': VERSION, 'c': CLIENT}
    if extra_param:
        params[extra_param['key']] = extra_param['value']
    response = requests.get(SERVER + "/rest/" + path, params=params)
    return response.text
