# functions for jupyter notebooks
import os, librosa, eyed3
import pandas as pd

def make_file_list(root_dir):
    '''given a directory, loops through folders and files and return list of files paths
        and file names'''
    
    path_list = []
    songs = []
    for subdir, dirs, files in os.walk(root_dir):
        songs.extend(files)
        for file in files:
            if file.endswith(('.mp3', '.wav')):
                path_list.append(os.path.join(subdir, file))

    return path_list, songs

def genre_fix(current_genre):
    '''given a'''
    for subdir, dirs, files in os.walk(root_dir):
        return files

def get_genre_id(genre_dict_list):
    return genre_dict_list[0]['genre_id']

def id_to_int(val):
    return int(val)

def make_mel_spectrogram_df(music_dir):
    '''
    Creates DataFrame with mel spectrogram and genres for all audio 
    sample files within given directory.
    dir     : string of directory location with audio samples
    returns : panda's DataFrame
    '''
    # helper function for getting lists of sample paths
    song_paths, _ = make_file_list(music_dir)
    
    mel_specs = []
    genre_labels = []
    
    for song in song_paths:
        
        # load sample data
        shape, sample_rate = librosa.core.load(song)
        audio_file = eyed3.load(song)
        
        # add genre to list for sample
        genre = audio_file.tag.genre
        genre_labels.append(str(genre))
        
        # compute mel spectrograms
        spect = librosa.feature.melspectrogram(shape, sr=sample_rate, n_fft=2048, hop_length=1024)
        spect = librosa.power_to_db(spect, ref=np.max)
        
        # adjust spectrograms to all be 128 x 660
        if spect.shape[1] != 660:
            spect.resize(128,660, refcheck=False)
        
        # flatten to fit dataframe and add to list
        spect = spect.flatten()
        mel_specs.append(spect)
    
    # Create dataframe and return
    df = pd.DataFrame(mel_specs)
    df['genres'] = genre_labels
    return df