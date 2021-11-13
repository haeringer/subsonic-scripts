import os
import logging
import subsonic_requests


LOGLEVEL = os.environ.get('SSC_LOGLEVEL', 'INFO')
LOGFILE = os.environ.get('SSC_LOGFILE', '/var/log/subsonic_playlists_dedup')

logging.basicConfig(
    filename=LOGFILE,
    level=LOGLEVEL,
    format='[%(asctime)s][%(levelname)s] %(message)s'
)
log = logging.getLogger()


def get_playlist_ids():
    response = subsonic_requests.get('getPlaylists')
    response_dict = response.json()
    playlists = response_dict['subsonic-response']['playlists']['playlist']

    playlist_ids = []
    for playlist in playlists:
        for k, v in playlist.items():
            if k == 'id':
                playlist_ids.append(v)
    return playlist_ids


def get_playlist_song_positions(playlist_id):
    response = subsonic_requests.get(
        'getPlaylist', extra_param={'key': 'id', 'value': playlist_id}
    )
    response_dict = response.json()
    playlist = response_dict['subsonic-response']['playlist']

    entries = playlist.get('entry')  # "entry" contains all entries of the playlist..
    for i, song in enumerate(entries):
        song['position'] = i
    return playlist


def identify_duplicates(playlist):
    seen = {}
    pl_with_dups = {
        'name': playlist.get('name'),
        'id': playlist.get('id'),
        'dups': []
    }
    for song in playlist.get('entry'):
        sid = song.get('id')
        if sid not in seen:
            seen[sid] = 1
        else:
            if seen[sid] == 1:
                pl_with_dups.get('dups').append(song)
            seen[sid] += 1
    return pl_with_dups


def remove_duplicates(playlist):
    if not playlist.get('dups'):
        return
    else:
        log.info('Found duplicates in playlist "{}":'.format(playlist['name']))

    dup_positions = []
    for dup_song in playlist.get('dups'):
        dup_positions.append(dup_song.get('position'))
        log.info('- Removing duplicate song "{} - {} - {}"'.format(
            dup_song.get('artist'), dup_song.get('album'), dup_song.get('title'))
        )

    update_response = subsonic_requests.post(
        'updatePlaylist',
        playlistId=playlist.get('id'),
        songIndexToRemove=dup_positions
    )
    update_response_dict = update_response.json()
    if update_response_dict['subsonic-response']['status'] == 'ok':
        log.info('Duplicate removal successful.')
    else:
        log.info('Duplicate removal failed:\n', update_response_dict)


if __name__ == "__main__":

    log.info('Searching for duplicate entries in playlists...')

    playlist_ids = get_playlist_ids()

    for plid in playlist_ids:
        songs_with_positions = get_playlist_song_positions(plid)
        playlist_with_duplicates = identify_duplicates(songs_with_positions)
        remove_duplicates(playlist_with_duplicates)

    log.info('Done.')
