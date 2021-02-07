# functions for jupyter notebooks

import os

def make_file_list(root_dir):
    '''given a directory, loops through folders and files and return list of files paths
        and file names'''
    
    path_list = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.mp3', '.wav')):
                path_list.append(os.path.join(subdir, file))

    return path_list

def get_genre_id(genre_dict_list):
    return genre_dict_list[0]['genre_id']

def id_to_int(val):
    return int(val)