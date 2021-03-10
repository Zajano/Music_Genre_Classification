from keras.models import load_model
import librosa

print("What's the filename of the song you would like me to guess the genre of?")
user_song = input("Filename (include extension): ")

shape, sample_rate = librosa.core.load(user_song)

# compute mel spectrograms
spect = librosa.feature.melspectrogram(shape, sr=sample_rate, n_fft=2048, hop_length=1024)
spect = librosa.power_to_db(spect, ref=np.max)

# adjust spectrograms to all be 128 x 660
if spect.shape[1] != 660:
    spect.resize(128,660, refcheck=False)

# flatten to fit trained model
spect = spect.flatten()

# scale to fit same min as model
min_val = spect.min()
spect /= min_val

# Reshaping images to be 128 x 660 x 1, where the 1 represents the single color channel
spect = spect.reshape(spect.shape[0], 128, 660, 1)

# load model
cnn_model = load_model('model_030921.h5')

# Making predictions from the cnn model
prediction = cnn_model.predict(spect, verbose=1)
pred_list = cnn_model.predict_log_proba(spect)
print('I predict the genre of ' + user_song + ' is: ')
print(prediction)