# Song Genre Classification with a Convolutional Neural Network

#### April Catañeda, Katie Stutts, Zachary Jaffe-Notier

------------

## Dependencies
While the training and generation of the model itself required significantly more packages to be installed, using the trained model itself only requires a few installations (assuming Python and its standard core has already been installed):
- Keras==2.4.3
- numpy==1.18.5
- librosa==0.8.0

Batch installation is possible using the supplied "requirements.txt" with pip or conda.

````cmd
pip install -r requirements.txt
````

Additionally, [ffmpeg](http://ffmpeg.org/download.html) is required by Librosa to convert audio files into spectrograms, which cannot be installed through pip.  

## Using the model
After the required dependencies have been installed, from within the directory where you downloaded these files execute the command to run the usage script for the model:

````cmd
python guess_song_genre.py
````

You will then be prompted to enter the filename (indluding the file type extension!) of the song file you wish to have the model predict the genre of. There are a few included MP3's you may use, or you may provide your own. The file must be within the same directory as the model and script, and it has only been tested with MP3 and WAV files; other file types may raise an exception or lead to unexpected behavior.
