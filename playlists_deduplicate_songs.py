import os
import base64
import hashlib
import requests

VERSION = os.environ.get('SH_APIVERSION')
SERVER = os.environ.get('SH_SERVER')
USER = os.environ.get('SH_USER')
PASSWD = os.environ.get('SH_PASSWD')


def generate_token():
    salt = os.urandom(16)
    salt_encoded = str(base64.b64encode(salt))
    string_for_md5 = PASSWD + salt_encoded
    token = hashlib.md5(string_for_md5.encode('utf-8')).hexdigest()
    return (token, salt_encoded)


def subsonic_getrequest(path):
    token, salt = generate_token()
    response = requests.get(
        SERVER + "/rest/" + path + '?u=' + USER + '&t=' + token + '&s=' + salt + '&v=' + VERSION + '&c=' + 'subsonic_automation'
    )
    print(response.content)


subsonic_getrequest('ping.view')