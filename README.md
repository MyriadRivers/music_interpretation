# Music Interpretation

Represents some scripts for generating the files necessary for the music visualizations used in the Deaf and Hard of Hearing (DHH) music interpretation project.

## Using the Scripts

```bash
# install dependencies for spleeter using conda for source separation
conda install -c conda-forge ffmpeg libsndfile
# install spleeter with pip
pip install spleeter

# install syrics for getting lyrics from the spotify API
pip install syrics
```
Original audio of songs to be analyzed is in the `original_audio` folder. 

Source separated stems of that audi is in the respectively named folder in `source_separation/audio_output`.

```bash
python extract_features.py
``` 
Generates the features files that the visualization takes in in the `features_files` directory.