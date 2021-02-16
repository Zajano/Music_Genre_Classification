# comprehensive script for training model data prep
# re-labels, sorts, and filters songs samples 
# cerates new directory "audio_samples" and deltes FMA/GTZAN directories

from notebook_functions import *
from pydub import AudioSegment
from song_lists import *
from pathlib import Path

import eyed3, os, shutil
import pandas as pd

print("Importing and prepping data for processing...")

# set string paths to directory locations for extracted data
data_dir = '/Volumes/APE_External/Dropbox/_Classes/21_Winter/CS_467/Project_Folder/fma/data/export'# path to data driectory, eg: "C:\\Users\\user\\Desktop\\data"
fma_dir = '/Volumes/APE_External/Dropbox/_Classes/21_Winter/CS_467/Project_Folder/fma/data/fma_medium'# directory name of FMA extraction location eg: "\\fma_medium"
gtzan_dir = '/Volumes/APE_External/Dropbox/_Classes/21_Winter/CS_467/Project_Folder/fma/data/genres_gtzan'# directory name of GTZAN extraction location eg:"\\GTZAN"
fma_metadata = '/Volumes/APE_External/Dropbox/_Classes/21_Winter/CS_467/Project_Folder/fma/data/fma_metadata' # directory name of FMA metadata extraction location eg:"\\fma_metadata"

# if you want the unused songs deleted
delete_unused = True

# ignore 'uncommon genre' warning
eyed3.log.setLevel("ERROR")

# load metadata
os.chdir(fma_metadata)
genres_df = pd.read_csv('genres.csv')
tracks_df = pd.read_csv('raw_tracks.csv')

# prep for re-labeling
tracks_df = tracks_df[["track_id", "track_genres"]]
tracks_df = tracks_df[tracks_df['track_genres'].notna()]
tracks_df['track_genres'] = tracks_df['track_genres'].apply(eval)
tracks_df['genre_ids'] = tracks_df['track_genres'].apply(get_genre_id)
tracks_df['genre_ids'] = tracks_df['genre_ids'].apply(id_to_int)
tracks_df['track_id'] = tracks_df['track_id'].apply(id_to_int)

# lookups for re-labeling and re-organizating loop
fma_paths, _ = make_file_list(fma_dir)
gtzan_paths, gtzan_songs = make_file_list(gtzan_dir)
genre_lookup = genres_df.set_index('genre_id').to_dict()['title']
id_lookup = genres_df.set_index('title').to_dict()['genre_id']
parent_lookup = genres_df.set_index('genre_id').to_dict()['top_level']
track_genre_lookup = tracks_df.set_index('track_id').to_dict()['genre_ids']

# genres for classification
target_genres = ["Reggae", "Rock", "Punk", "Metal", "Psych-Rock", "Post-Rock", \
                "Indie-Rock", "Electronic", "Ambient Electronic", "Techno", \
                "Chiptune", "Trip-Hop", "Jazz", "Classical", "Country", \
                "Pop", "Folk", "Hip-Hop"]

# so these are not re-labeled as their top-level genre
preserved_genres = ["Psych-Rock", "Post-Rock", "Ambient Electronic", "Techno", \
                "Indie-Rock", "Trip-Hop", "Punk", "House"]

# create directories to move songs into
sample_dir = data_dir + "/audio_samples"
Path(sample_dir).mkdir(mode=0o777, parents=False, exist_ok=True)
for genre in target_genres:
    genre_dir = sample_dir + "/" + genre
    Path(genre_dir).mkdir(mode=0o777, parents=False, exist_ok=True)

def genre_fix(song_genre, filename):
    '''adjusts current genres to be of only target genres'''
    if "Reggae" in song_genre: song_genre = "Reggae"
    elif "Chip" in song_genre or filename in chiptune_relabel: song_genre = "Chiptune"
    elif "Metal" in song_genre: song_genre = "Metal"
    elif "House" in song_genre: song_genre = "Techno"
    elif filename in country_relabel: song_genre = "Country"
    elif song_genre not in preserved_genres: 
        song_genre = genre_lookup[parent_lookup[id_lookup[song_genre]]]
    return song_genre

print("Starting to re-label and move songs...")
# re-label and move FMA samples
for i in range(len(fma_paths)):
    os.chmod(fma_paths[i], 0o777)
    filename = fma_paths[i][-10:-4]
    song_genre = genre_lookup[track_genre_lookup[int(filename)]]
    if filename not in fma_skips and song_genre not in fma_skips:
        audiofile = eyed3.load(fma_paths[i])
        song_genre = genre_fix(song_genre, filename)
        audiofile.tag.genre = song_genre
        audiofile.tag.save()

        ########## TODO: finish screening song samples for Rock, Electric, and Punk
        ########## then remove this portion of the script
        skip_song = False
        if song_genre == 'Electronic' and int(filename) <= 58343:
            skip_song = True
        elif song_genre == 'Rock' and filename not in safe_rock:
            skip_song = True
        elif song_genre == 'Punk' and int(filename) <= 93983:
            skip_song = True

        if not skip_song:
        ########## end of portion to remove
            new_path = data_dir + "/audio_samples/" + song_genre + "/" + fma_paths[i][-10:]
            os.replace(fma_paths[i], new_path)

print("Beginning GTZAN wav to mp3 conversions and moving...")
# convert to mp3, move, and then re-label GTZAN songs
for i in range(len(gtzan_paths)):
    filename = gtzan_songs[i]
    for genre in gtzan_genres: 
        if genre in filename and filename not in gtzan_skips:
            genre = genre.capitalize()
            new_file = data_dir + "/audio_samples/" + genre + "/" + filename[:-4] + ".mp3"
            AudioSegment.from_wav(gtzan_paths[i]).export(new_file, format="mp3")
            audiofile = eyed3.load(new_file)
            audiofile.tag.genre = genre
            audiofile.tag.save()

if delete_unused:
    shutil.rmtree(fma_dir)
    shutil.rmtree(gtzan_dir)

print("Done moving, re-labeling, and converting files.")
