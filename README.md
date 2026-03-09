# SoundSense : Environmental Audio Event Detection

SoundSense is a project focused on detecting audio events in environmental recordings using signal processing techniques.

The goal is to identify when a sound event occurs within a continuous audio signal. The project explores different detection methods and evaluates their performance using a synthetic dataset generated from real-world recordings.

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

- Bus - traveling by bus in the city (vehicle)
- Cafe / Restaurant - small cafe/restaurant (indoor)
- Car - driving or traveling as a passenger, in the city (vehicle)
- City center (outdoor)
- Forest path (outdoor)
- Grocery store - medium size grocery store (indoor)
- Home (indoor)
- Lakeside beach (outdoor)
- Library (indoor)
- Metro station (indoor)
- Office - multiple persons, typical work day (indoor)
- Residential area (outdoor)
- Train (traveling, vehicle)
- Tram (traveling, vehicle)
- Urban park (outdoor)

Each acoustic scene has 312 segments totaling 52 minutes of audio.

The ESC-50 dataset is used as a source of environmental sound events.

Reference:

Piczak, Karol J.
ESC: Dataset for Environmental Sound Classification
Proceedings of the 23rd Annual ACM Conference on Multimedia, 2015.

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
