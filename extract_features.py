import librosa
import os
from pathlib import Path
from syrics.api import Spotify
from credentials import cookie

import color_generation

# Track name with extension
track = "no_culture.mp3"
track_path = os.path.join("original_audio", track)
spotify_track_id = "0jG6wsuGg5w1VFB1LSZgJB"

track_name = track.split(".")[0]
# audio_directory = "separated_stems/"

# stems_directory = audio_directory + track_name

# set up lyrics connection to spotify
# Get sp_dc cookie here to authenticate services 
sp_dc = cookie
sp = Spotify(sp_dc)
lyrics = sp.get_lyrics(spotify_track_id)["lyrics"]["lines"]

# Set up source separation
# separator = Separator('spleeter:4stems')
# separator.separate_to_file(track, stems_directory)

# Make a directory for storing the features files of songs if it doesn't already exist
Path("features_files").mkdir(parents=True, exist_ok=True)

# Write all features into a text file "[song_name].txt"
with open( os.path.join("features_files", track_name + ".txt"), "w", encoding="utf-8") as features_file:
    
    # TITLE
    # TODO: Spotify API - Get Track
    title = track_name
    features_file.write("title," + title)

    # TEMPO
    tempo = 127.003
    features_file.write("tempo," + tempo)

    # METER
    # TODO: We'll print 4 for common time here as a placeholder, but eventually fetch this from the Spotify API - Get Audio Features
    meter = 4
    features_file.write("meter," + meter)

    # DANCEABLILITY
    danceability = 0.704
    features_file.write("danceability," + danceability)

    # ENERGY
    energy = 0.89
    features_file.write("energy," + energy)

    # VALENCE
    valence = 0.754
    features_file.write("valence," + valence)

    # HUE
    features_file.write("hue," + color_generation.getBaseHue(valence, energy))

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

    # # Load the individual stems for feature extraction
    # for stem in os.listdir(stems_directory):
    #     file_name = os.path.join(stems_directory, stem)
        
    #     features_file.write(stem.split(".")[0] + "\n")
        
    #     y, sr = librosa.load(file_name)

    #     print("frames in entire song: " + str(len(y)))
        
    #     onset_strength_env = librosa.onset.onset_strength(y=y, sr=sr)

    #     print("frames in onset envelope: " + str(len(onset_strength_env)))


    #     # times = librosa.times_like(onset_strength_env, sr=sr)
    #     # onset_frames = librosa.onset.onset_detect(onset_envelope=onset_strength_env, sr=sr)
    #     # onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    #     # strengths_to_times = {time: strength for time, strength in zip(times, onset_strength_env)}
    #     # # times are the times corresponding to every frame of the onset strength envelope
    #     # # onset_frames are the specific frames of the onset in the context of the entire track
    #     # onset_strengths = [strengths_to_times[on_time] for on_time in times[onset_frames]]

    #     # features_file.write("Onsets:")
    #     # features_file.write(str(onset_times) + "\n")

    #     # features_file.write("Onsets Strengths:")
    #     # features_file.write(str(onset_strengths) + "\n")
        
    #     # print("frames in entire song: " + str(len(y)))
    #     # print("frames in onset envelope: " + str(len(onset_strength_env)))