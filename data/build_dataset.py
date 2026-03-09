import os
import random
import numpy as np
import pandas as pd
import librosa
import soundfile as sf
from pathlib import Path
from tqdm import tqdm


# USER PARAMETERS


N_OUTPUTS = 500  
EVENT_CATEGORIES = [
    "car_horn",
    "clock_alarm",
    "siren",
    "chainsaw",
    "church_bells",
    "fireworks",
    "vacuum_cleaner",
    "washing_machine",
    "footsteps",
    "dog"
]

# PROJECT ROOT (folder where the script is located)
ROOT = Path(__file__).resolve().parent
TUT_PATH = ROOT / "TUT"
ESC_PATH = ROOT / "ESC-50-master"
OUTPUT_PATH = ROOT / "generated_dataset"


AUDIO_OUTPUT = OUTPUT_PATH / "audio"
ANNOTATIONS_FILE = OUTPUT_PATH / "annotations.csv"

AUDIO_OUTPUT.mkdir(parents=True, exist_ok=True)



# LOAD ESC EVENTS


esc_meta = pd.read_csv(ESC_PATH / "meta/esc50.csv")
esc_meta = esc_meta[esc_meta["category"].isin(EVENT_CATEGORIES)]
print("esc_meta", len(esc_meta))

event_dict = {}

for cat in EVENT_CATEGORIES:
    files = esc_meta[esc_meta["category"] == cat]["filename"].tolist()
    event_dict[cat] = [ESC_PATH / "audio" / f for f in files]

print("Events loaded:")
for k in event_dict:
    print(k, len(event_dict[k]))


# LOAD TUT BACKGROUNDS

tut_files = []

meta_file = TUT_PATH / 'meta/meta.txt'
meta = pd.read_csv(meta_file, sep="\t", names = ['path', "scene_label", "id"])
scene_labels = sorted(meta["scene_label"].unique())

background_dict = {}

for cat in scene_labels:
    files = meta[meta["scene_label"] == cat]["path"].tolist()

    background_dict[cat] = [TUT_PATH / f for f in files if (TUT_PATH / f).exists()]

print("background loaded:")
for k in background_dict:
    print(k, len(background_dict[k]))

print("METAAA",meta.head(),
meta.columns,
files[:5],
meta["scene_label"].unique())



# MERGE FUNCTION


def merge_event(bg1, bg2, event_path, output_path):

    # Load backgrounds
    bg_audio1, sr = librosa.load(bg1, sr=None)
    bg_audio2, _ = librosa.load(bg2, sr=sr)

    # Concatenate
    bg_audio = np.concatenate([bg_audio1, bg_audio2])

    # Load event
    event_audio, _ = librosa.load(event_path, sr=sr)

    # If event longer than background → skip
    if len(event_audio) >= len(bg_audio):
        return None

    # Random position
    max_start = len(bg_audio) - len(event_audio)
    start_sample = random.randint(0, max_start)

    mixed = bg_audio.copy()
    mixed[start_sample:start_sample+len(event_audio)] += event_audio * np.random.uniform(0.1, 1)

    # Normalize
    mixed = mixed / np.max(np.abs(mixed))

    sf.write(output_path, mixed, sr)

    start_time = start_sample / sr
    end_time = (start_sample + len(event_audio)) / sr

    return start_time, end_time



# GENERATION LOOP


annotations = []

for i in tqdm(range(N_OUTPUTS)):

    bg_category = random.choice(scene_labels)
    bg_index = np.random.randint(len(background_dict[bg_category])-2)
    bg_path = random.choice(background_dict[bg_category])
    if bg_index + 1 >= len(background_dict[bg_category]):
        break

    bg1 = background_dict[bg_category][bg_index]
    bg2 = background_dict[bg_category][bg_index + 1]

    # Random event category
    category = random.choice(EVENT_CATEGORIES)
    event_path = random.choice(event_dict[category])

    output_name = f"sample_{i:04d}.wav"
    output_path = AUDIO_OUTPUT / output_name

    result = merge_event(bg1, bg2, event_path, output_path)

    if result is None:
        continue

    start_time, end_time = result

    annotations.append({
        "filename": output_name,
        "background_label" : bg_category,
        "event_label": category,
        "start_time": round(start_time, 3),
        "end_time": round(end_time, 3)
    })

# Save CSV
df = pd.DataFrame(annotations)
df.to_csv(ANNOTATIONS_FILE, index=False)

print("Dataset generation complete.")
print("Files generated:", len(annotations))