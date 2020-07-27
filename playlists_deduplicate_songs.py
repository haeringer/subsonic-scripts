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

    for k, v in playlist.items():
        if k == 'entry':  # "entry" contains all entries of the playlist..
            for i, song in enumerate(v):
                song['position'] = i
    return playlist


def identify_duplicates(playlist):
    seen = {}
    pl_with_dups = {
        'name': playlist['@name'],
        'id': playlist['@id'],
        'dups': []
    }
    for song in playlist['entry']:
        sid = song['@id']
        if sid not in seen:
            seen[sid] = 1
        else:
            if seen[sid] == 1:
                pl_with_dups['dups'].append(song)
            seen[sid] += 1
    return pl_with_dups


def remove_duplicates(playlist):
    if not playlist['dups']:
        return
    else:
        print('Found duplicates in playlist "{}":'.format(playlist['name']))

    dup_positions = []
    for dup_song in playlist['dups']:
        dup_positions.append(dup_song['position'])
        print('- Removing duplicate song "{} - {} - {}"'.format(
            dup_song['@artist'], dup_song['@album'], dup_song['@title'])
        )

    update_response_xml = subsonic_requests.post(
        'updatePlaylist',
        playlistId=playlist['id'],
        songIndexToRemove=dup_positions
    )
    update_response = xmltodict.parse(update_response_xml)
    if update_response['subsonic-response']['@status'] == 'ok':
        print('Duplicate removal successful.')
    else:
        print('Duplicate remove failed:\n', update_response_xml)


if __name__ == "__main__":

    playlist_ids = get_playlist_ids()

    for plid in playlist_ids:
        songs_with_positions = get_playlist_song_positions(plid)
        playlist_with_duplicates = identify_duplicates(songs_with_positions)
        remove_duplicates(playlist_with_duplicates)
