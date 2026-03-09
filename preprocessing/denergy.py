import librosa
import matplotlib.pyplot as plt
import numpy as np
import scipy

def compute_denergy(data_path, hop_length = 220, win_length = 441):
    #Load WAV file
    y, sr = librosa.load(data_path, sr = None)


    #Spectrogram       
    f, t, Sxx = scipy.signal.spectrogram(y, sr,nperseg=win_length, noverlap = win_length - hop_length, scaling = "density")
    Sxx_db = 20 * np.log10(np.abs(Sxx+ 1e-8))

    band = f < 2000
    E = np.sum(Sxx[band, :], axis = 0)

    dE = np.diff(E)

    window_duration = 0.2
    window_frames = int(window_duration * sr / hop_length)

    Z = np.zeros_like(E)

    for i in range(window_frames, len(E)):
        local = E[i-window_frames:i]
        Z[i] = (E[i] - np.mean(local)) / (np.std(local) + 1e-8)

    # =============================
    # DERIVEE
    # =============================

    dZ = np.diff(Z)

    # LISSAGE (important !)
    dZ_smooth = scipy.ndimage.gaussian_filter1d(dZ, sigma=1)

    threshold = 6
    events = t[1:][dZ_smooth > threshold]
    if len(events) > 0:
        min_gap = 100e-3
        filtered_events = [events[0]]

        for e in events[1:]:
            if e - filtered_events[-1] > min_gap:
                filtered_events.append(e)

        events = np.array(filtered_events)

    return events

