import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)

# Find the last cell
last_cell = nb['cells'][-1]
last_cell['source'][1] = "import matplotlib.pyplot as plt\n"

with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)