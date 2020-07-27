# SubSonic Scripts

Helper scripts for automating tasks supporting the management of a SubSonic/AirSonic music libary.


## playlists_deduplicate_songs

When adding titles to a playlist, the SubSonic API does not verify wether a title is already present in the playlist. Therefore, titles can be added multiple times. This script can be run regularly in order to check all playlists of a given user for duplicates and remove those.

#### Environment variables

```sh
SSC_APIVERSION=<SubSonic API version>
SSC_SERVER=<SubSonic server address>
SSC_USER=<Username>
SSC_PASSWD=<Password>
SSC_LOGLEVEL=<INFO/DEBUG/..>  # optional, default INFO
SSC_LOGFILE=</path/to/file>   # optional, default /var/log/subsonic_playlists_dedup
```
