import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if 'source' in cell:
        for j, line in enumerate(cell['source']):
            if "weights_volatile = [0.33, 0.33, 0.34]" in line:
                cell['source'][j] = "weights_volatile = optimize_weights([y_val_pred_volatile_xgb, y_val_pred_volatile_lgb, y_val_pred_volatile_cb], y_val_volatile)\n"
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)