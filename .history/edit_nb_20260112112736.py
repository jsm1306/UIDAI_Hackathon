import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if 'source' in cell:
        for j, line in enumerate(cell['source']):
            if 'sample_weight_stable = np.sqrt(y_train_stable_orig)' in line:
                cell['source'][j] = "sample_weight_stable = 1 / (y_train_stable_orig + 1)\n"
                cell['source'][j+1] = "sample_weight_stable = sample_weight_stable / sample_weight_stable.sum() * len(sample_weight_stable)\n"
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)