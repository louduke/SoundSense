from pathlib import Path
import pandas as pd
import seaborn as sns
from preprocessing import compute_denergy, compute_spectral_flux
import numpy as np
import matplotlib.pyplot as plt


DATASET_PATH = Path("/Users/louiseduquenne/Documents/projets/SoundSense/data/generated_dataset")

##LOAD FILES
meta = pd.read_csv(DATASET_PATH / "annotations.csv")

methods = {
    "denergy": compute_denergy,
    "spectral_flux": compute_spectral_flux
}

tolerance = 100e-3  # 100 ms

categories = meta["event_label"].unique()

results = []

for method_name, method in methods.items():
    for cat in categories:
        TP, FP, FN = 0, 0, 0
        subset = meta[meta["event_label"] == cat]
        for _, row in subset.iterrows():
            audio_path = DATASET_PATH / 'audio' / row["filename"]
            events = method(audio_path)

            if len(events) > 0:
                if abs(events[0] - row["start_time"]) < tolerance:
                    TP += 1
                else :
                    FP +=1
            else:
                FN += 1
        
        precision = TP / (TP + FP) 
        recall = TP / (TP + FN) 

        results.append({
            "method": method_name,
            "category": cat,
            "TP": TP,
            "FP": FP,
            "FN": FN,
            "precision": precision,
            "recall": recall
        })
results_df = pd.DataFrame(results)

##GLOBAL SCORE
global_scores = results_df.groupby("method")[["TP","FP","FN"]].sum()
global_scores["precision"] = global_scores["TP"] / (global_scores["TP"] + global_scores["FP"])
global_scores["recall"] = global_scores["TP"] / (global_scores["TP"] + global_scores["FN"])

print("\nGlobal scores")
print(global_scores)

# ---------------------------
# MATRICES
# ---------------------------

precision_matrix = results_df.pivot(index="category", columns="method", values="precision")
recall_matrix = results_df.pivot(index="category", columns="method", values="recall")


# ---------------------------
# HEATMAP PRECISION
# ---------------------------

plt.figure(figsize=(8,5))
sns.heatmap(
    precision_matrix,
    annot=True,
    cmap="YlGnBu",
    vmin=0,
    vmax=1
)
plt.title("Precision per category and method")
plt.show()



# ---------------------------
# HEATMAP RECALL
# ---------------------------

plt.figure(figsize=(8,5))
sns.heatmap(
    recall_matrix,
    annot=True,
    cmap="YlOrRd",
    vmin=0,
    vmax=1
)
plt.title("Recall per category and method")
plt.show()
    
# TP = 0 #True positive
# FN = 0 #False negative
# FP = 0 #False positive

# for _, row in meta.iterrows():
#     audio_path = DATASET_PATH / 'audio' / row["filename"]
#     events = compute_denergy(audio_path)

#     if len(events) > 0:
#         if abs(events[0] - row["start_time"]) < tolerance:
#             TP += 1
#         else :
#             FP +=1
#     else:
#         FN += 1

# print(f"denergy : TP = {TP}, FN = {FN}, FP = {FP}")


# TP = 0 #True positive
# FN = 0 #False negative
# FP = 0 #False positive


# for _, row in df.iterrows():

#     events = compute_spectral_flux(row["audio_path"])

#     if len(events) > 0:
#         if abs(events[0] - row["start_time"]) < tolerance:
#             TP += 1
#         else :
#             FP +=1
#     else:
#         FN += 1

# print(f"spectral flux : TP = {TP}, FN = {FN}, FP = {FP}")


