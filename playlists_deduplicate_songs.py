import xmltodict
import subsonic_requests


def get_playlist_ids():
    playlists_xml = subsonic_requests.get('getPlaylists')
    playlists_dict = xmltodict.parse(playlists_xml)
    playlists = playlists_dict['subsonic-response']['playlists']['playlist']

    playlist_ids = []
    for playlist in playlists:
        for k, v in playlist.items():
            if k == '@id':
                playlist_ids.append(v)
    return playlist_ids


def get_playlist_song_positions(playlist_id):
    playlist_xml = subsonic_requests.get(
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


def identify_duplicates(song_positions):
    seen = {}
    pl_with_dups = {
        'name': song_positions['playlist_name'],
        'id': song_positions['playlist_id'],
        'dups': []
    }
    for entry in song_positions['songs']:
        sid = entry['song_id']
        if sid not in seen:
            seen[sid] = 1
        else:
            if seen[sid] == 1:
                pl_with_dups['dups'].append(entry)
            seen[sid] += 1
    return pl_with_dups


if __name__ == "__main__":

    playlist_ids = get_playlist_ids()

    for plid in playlist_ids:
        song_positions = get_playlist_song_positions(plid)
        identify_duplicates(song_positions)
