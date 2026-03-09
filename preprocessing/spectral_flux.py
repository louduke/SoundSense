import librosa
import matplotlib.pyplot as plt
import numpy as np
import scipy

def compute_spectral_flux(data_path, hop_length = 220, win_length = 441):

    #Load WAV file
    y, sr = librosa.load(data_path, sr = None)

    #Spectrogram       
    f, t, Sxx = scipy.signal.spectrogram(y, sr,nperseg=win_length, noverlap = win_length - hop_length, scaling = "density")
    Sxx_db = 20 * np.log10(np.abs(Sxx+ 1e-8))
    Flux = np.sum(np.abs(np.diff(Sxx, axis=1)), axis = 0)
    window_duration = 0.2
    window_frames = int(window_duration * sr / hop_length)

    Z = np.zeros_like(Flux)

    for i in range(window_frames, len(Flux)):
        local = Flux[i-window_frames:i]
        Z[i] = (Flux[i] - np.mean(local)) / (np.std(local) + 1e-8)

    # =============================
    # DERIVEE
    # =============================

    dZ = np.diff(Z)

    # LISSAGE (important !)
    dZ_smooth = scipy.ndimage.gaussian_filter1d(dZ, sigma=1)

    # =============================
    # DETECTION
    # =============================

    threshold = 6
    events_flux = t[2:][dZ_smooth > threshold]

    if len(events_flux) > 0:
        min_gap = 100e-3
        filtered_events = [events_flux[0]]

        for e in events_flux[1:]:
            if e - filtered_events[-1] > min_gap:
                filtered_events.append(e)

        events_flux = np.array(filtered_events)

    return events_flux
