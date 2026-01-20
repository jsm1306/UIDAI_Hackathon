import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if 'source' in cell and any('plt.show()' in line for line in cell['source']):
        for i, line in enumerate(cell['source']):
            if 'plt.show()' in line:
                insert_index = i + 1
                cell['source'].insert(insert_index, '\n')
                cell['source'].insert(insert_index + 1, '# Tune district_volatility threshold\n')
                cell['source'].insert(insert_index + 2, 'for q in [0.6, 0.65, 0.7, 0.75, 0.8]:\n')
                cell['source'].insert(insert_index + 3, '    thresh = df_agg[train_mask]["district_volatility"].quantile(q)\n')
                cell['source'].insert(insert_index + 4, '    volatile_count = (df_agg[train_mask]["district_volatility"] > thresh).sum()\n')
                cell['source'].insert(insert_index + 5, '    print(f"Quantile {q}: Threshold {thresh:.2f}, Volatile districts: {volatile_count}")\n')
                break
        break
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)