import argparse
import librosa
import os
from pathlib import Path
from syrics.api import Spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import cookie
import color_generation

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-p", "--path", type=str, help="path to the audio file")
arg_parser.add_argument("-u", "--uri", type=str, help="spotify uri of the track")
args = arg_parser.parse_args()

uri = args.uri
track_path = args.path

# Set up connection to Spotify Web API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
spotify_track = spotify.track(uri)

track_name = spotify_track['name']

# set up lyrics connection to spotify
# Get sp_dc cookie here to authenticate services 
sp_dc = cookie
sp = Spotify(sp_dc)
lyrics = sp.get_lyrics(uri)["lyrics"]["lines"]

# Make a directory for storing the features files of songs if it doesn't already exist
Path("features_files").mkdir(parents=True, exist_ok=True)

# Write all features into a text file "[song_name].txt"
with open(os.path.join("features_files", track_name + ".txt"), "w", encoding="utf-8") as features_file:
    
    features = spotify.audio_features(uri)[0]
    
    # TITLE
    features_file.write("title," + track_name + "\n")

    # TEMPO
    tempo = features['tempo']
    features_file.write("tempo," + str(tempo) + "\n")

    # METER
    meter = features['time_signature']
    features_file.write("meter," + str(meter) + "\n")

    # Duration in seconds
    duration = features['duration_ms']
    features_file.write("duration," + str(duration / 1000) + "\n")

    # DANCEABLILITY
    danceability = features['danceability']
    features_file.write("danceability," + format(danceability, '.3f') + "\n")

    # ENERGY
    energy = features['energy']
    features_file.write("energy," + format(energy, '.3f') + "\n")

    # VALENCE
    valence = features['valence']
    features_file.write("valence," + format(valence, '.3f') + "\n")

    # HUE
    hue = color_generation.getBaseHue(valence, energy)[0]
    features_file.write("hue," + format(hue, '.3f') + "\n")

    # LYRICS EXTRACTION
    features_file.write("lyrics_start\n")
    for lyric in lyrics:
        features_file.write(str(int(lyric["startTimeMs"]) / 1000) + "," + lyric["words"] + "\n")
    features_file.write("lyrics_end\n")
    

    # Load the composite track for feature extraction
    y, sr = librosa.load(track_path)


    # BEAT EXTRACTION
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    features_file.write("beats_start\n")
    for beat_time in beat_times:
        features_file.write(str(beat_time) + "\n")
    features_file.write("beats_end\n")


    # ENERGY (RMS)
    S, phase = librosa.magphase(librosa.stft(y))
    rms = librosa.feature.rms(S=S)
    rms_times = librosa.times_like(rms)

    # Get maximum RMS so we can easily normalize the energy to a scale of 1
    # TODO: Make this logarithmic and better mapped to actual perceived loudness
    max_rms = rms[0, 0]
    for i in range(rms.size):
        if (rms[0, i] > max_rms):
            max_rms = rms[0, i]
    
    features_file.write("energy_start\n")
    for i in range(rms.size):
        features_file.write(str(rms_times[i]) + ',' + "{:.8f}".format(rms[0, i] / max_rms) + '\n')
    features_file.write("energy_end\n")