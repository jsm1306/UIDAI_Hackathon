import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if 'source' in cell:
        for i, line in enumerate(cell['source']):
            if 'features = ' in line and 'recent_volatility' in line and 'is_spike' in line:
                cell['source'].insert(i+1, "features.remove('volatility_change')\n")
                cell['source'].insert(i+2, "features.remove('cv')\n")
                break
        break
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)