# Music Interpretation

Represents some scripts for generating the files necessary for the music visualizations used in the Deaf and Hard of Hearing (DHH) music interpretation project.

## Using the Scripts

Make a file called credentials.py with one line of code:
```python
cookie = "<cookie>"
```
Get the cookie following these instructions: https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc

Follow Spotipy github to set up authentication for that too: https://github.com/spotipy-dev/spotipy

```bash
# Install requirements
pip install -r requirements.txt
python extract_features.py -p [path/to/audio/file] -u [spotify_track_uri]
```

Generates the features files that the Unity Music Interpreter project consumes in the `features_files` directory.
