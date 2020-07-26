import os
import base64
import hashlib
import requests
import xmltodict


VERSION = os.environ.get('SH_APIVERSION')
SERVER = os.environ.get('SH_SERVER')
USER = os.environ.get('SH_USER')
PASSWD = os.environ.get('SH_PASSWD')
CLIENT = 'subsonic_automation'


def generate_token():
    salt = os.urandom(16)
    salt_encoded = str(base64.b64encode(salt))
    string_for_md5 = PASSWD + salt_encoded
    token = hashlib.md5(string_for_md5.encode('utf-8')).hexdigest()
    return (token, salt_encoded)


def subsonic_getrequest(path, extra_param=None):
    token, salt = generate_token()
    params = {'u': USER, 't': token, 's': salt, 'v': VERSION, 'c': CLIENT}
    if extra_param:
        params[extra_param['key']] = extra_param['value']
    response = requests.get(SERVER + "/rest/" + path, params=params)
    # print(response.text)
    return response.text


def get_playlist_ids():
    playlists_xml = subsonic_getrequest('getPlaylists')
    playlists_dict = xmltodict.parse(playlists_xml)
    playlists = playlists_dict['subsonic-response']['playlists']['playlist']

    playlist_ids = []
    for playlist in playlists:
        for k, v in playlist.items():
            if k == '@id':
                playlist_ids.append(v)
    return playlist_ids


def get_playlist_song_positions(playlist_id):
    playlist_xml = subsonic_getrequest(
        'getPlaylist', extra_param={'key': 'id', 'value': playlist_id}
    )
    playlist_dict = xmltodict.parse(playlist_xml)
    playlist = playlist_dict['subsonic-response']['playlist']

    song_positions = {}
    for k, v in playlist.items():
        if k == '@name':
            song_positions['playlist_name'] = v
        if k == '@id':
            song_positions['playlist_id'] = v
        if k == 'entry':
            song_positions['songs'] = []
            for i, song in enumerate(v):
                for k, v in song.items():
                    if k == '@id':
                        song_positions['songs'].append(
                            {'position': i, 'song_id': v}
                        )
    return song_positions


if __name__ == "__main__":

    playlist_ids = get_playlist_ids()

    for plid in playlist_ids:
        song_positions = get_playlist_song_positions(plid)
        print(song_positions)
