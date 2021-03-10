from keras.models import load_model
import numpy as np
import librosa
import os

clear = lambda: os.system('cls')

DONE = 0

while(DONE != 1):
    clear()
    print("What's the filename of the song you would like me to guess the genre of?")
    try:
        user_song = input("Filename (include extension): ")

        shape, sample_rate = librosa.core.load(user_song)

        mel_specs = []

        # compute mel spectrograms
        for i in range(2):
            spect = librosa.feature.melspectrogram(shape, sr=sample_rate, n_fft=2048, hop_length=1024)
            spect = librosa.power_to_db(spect, ref=np.max)

            # adjust spectrograms to all be 128 x 660
            if spect.shape[1] != 660:
                spect.resize(128,660, refcheck=False)

            # flatten to fit trained model
            spect = spect.flatten()
            mel_specs.append(spect)

        # scale to fit same min as model
        mel_specs = np.array(mel_specs)
        min_val = mel_specs.min()
        mel_specs /= min_val

        # Reshaping images to be 128 x 660 x 1, where the 1 represents the single color channel
        mel_specs = mel_specs.reshape(mel_specs.shape[0], 128, 660, 1)

        # load model
        cnn_model = load_model('model_030921.h5')

        # Making predictions from the cnn model
        predictions = cnn_model.predict(mel_specs, verbose=0)
        choice = cnn_model.predict_classes(mel_specs, verbose=0)
        # pred_list = cnn_model.predict_log_proba(mel_specs)

        labels_dict = {
            0: 'Ambient Electronic',
            1: 'Chiptune',
            2: 'Classical',
            3: 'Country',
            4: 'Electronic',
            5: 'Folk',
            6: 'Hip-Hop',
            7: 'Indie-Rock',
            8: 'Jazz',
            9: 'Metal',
            10: 'Pop',
            11: 'Post-Rock',
            12: 'Psych-Rock',
            13: 'Punk',
            14: 'Reggae',
            15: 'Rock',
            16: 'Techno',
            17: 'Trip-Hop'
        }

        clear()
        print('I predict the genre of ' + user_song + ' is: ')
        print(labels_dict[choice[0]])
        print('Would you like try out another song? \n Please enter: 1 for NO')
        user_choice = input('>> ')
        DONE = int(user_choice)
    except:
        clear()
        print("Sorry! Something went wrong; maybe the song filename or file type?")

print('Thanks for using our application!')
