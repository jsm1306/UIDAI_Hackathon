import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if 'source' in cell:
        for j, line in enumerate(cell['source']):
            if "threshold = df_agg['district_volatility'].quantile(0.70)" in line:
                cell['source'][j] = "threshold = df_agg[train_mask]['district_volatility'].quantile(0.70)\n"
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)