# SoundSense : Environmental Audio Event Detection

SoundSense detects audio events in environmental recordings.

# Audio event detection 

Two detcetion methods are implemented :
- Spectral Flux
Detects sudden changes in the spectral content of the signal
- Derivative of Energy
Detects rapid increases in signal energy within a frequency band

Those methods analyse the spectrogram of the audio signal to identify potential event onset.

# Dataset Generation

Creation of audio scene by mixing :

- Background environments from TUT Acoustic Scenes dataset
- Sounds events from ESC-50 dataset 

The annotation file contains:

- filename
- background_label
- event_label
- start_time #Event timing 
- end_time


TUT Acoustic Scenes 2017, development dataset consists of 10-seconds audio segments from 15 acoustic scenes:

Bus - traveling by bus in the city (vehicle)
Cafe / Restaurant - small cafe/restaurant (indoor)
Car - driving or traveling as a passenger, in the city (vehicle)
City center (outdoor)
Forest path (outdoor)
Grocery store - medium size grocery store (indoor)
Home (indoor)
Lakeside beach (outdoor)
Library (indoor)
Metro station (indoor)
Office - multiple persons, typical work day (indoor)
Residential area (outdoor)
Train (traveling, vehicle)
Tram (traveling, vehicle)
Urban park (outdoor)
Each acoustic scene has 312 segments totaling 52 minutes of audio.


@inproceedings{piczak2015dataset,
  title = {{ESC}: {Dataset} for {Environmental Sound Classification}},
  author = {Piczak, Karol J.},
  booktitle = {Proceedings of the 23rd {Annual ACM Conference} on {Multimedia}},
  date = {2015-10-13},
  url = {http://dl.acm.org/citation.cfm?doid=2733373.2806390},
  doi = {10.1145/2733373.2806390},
  location = {{Brisbane, Australia}},
  isbn = {978-1-4503-3459-4},
  publisher = {{ACM Press}},
  pages = {1015--1018}
}

# Evaluation Pipeline

Each detection method is evaluated by comparing the detcted event time with the annotated ground truth 

Evaluation metrics :
- True Positives (TP)
- False Positive (FP)
- False Negative (FN)


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
