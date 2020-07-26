# SubSonic Scripts

Helper scripts for automating tasks supporting the management of a SubSonic/AirSonic music libary.


## playlists_deduplicate_songs

When adding titles to a playlist, the SubSonic API does not verify wether a title is already present in the playlist. Therefore, titles can be added multiple times. This script can be run regularly in order to check all playlists for duplicates and remove those.

#### Environment variables

```sh
SH_APIVERSION=<SubSonic API version>
SH_SERVER=<SubSonic server address>
SH_USER=<Username>
SH_PASSWD=<Password>
```
