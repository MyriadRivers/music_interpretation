# Music Interpretation

Represents some scripts for generating the files necessary for the music visualizations used in the Deaf and Hard of Hearing (DHH) music interpretation project.

## Using the Scripts

```bash
# Install requirements
pip install -r requirements.txt
python extract_features.py -p [path/to/audio/file] -u [spotify_track_uri]
```

Generates the features files that the visualization takes in in the `features_files` directory.
