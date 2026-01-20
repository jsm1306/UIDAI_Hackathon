import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if 'source' in cell and any('Improved volatility-based training complete.' in line for line in cell['source']):
        # Find the index of the print line
        for i, line in enumerate(cell['source']):
            if 'print("Improved volatility-based training complete.")' in line:
                # Insert after this line
                insert_index = i + 1
                cell['source'].insert(insert_index, '\n')
                cell['source'].insert(insert_index + 1, '# Post-Processing Smoothing\n')
                cell['source'].insert(insert_index + 2, 'y_test_pred_combined_smoothed = y_test_pred_combined.rolling(3, center=True, min_periods=1).mean()\n')
                cell['source'].insert(insert_index + 3, 'evaluate(y_test_orig, y_test_pred_combined_smoothed, "Smoothed Overall Test")\n')
                cell['source'].insert(insert_index + 4, '\n')
                cell['source'].insert(insert_index + 5, '# Diagnostic: Top MAE districts\n')
                cell['source'].insert(insert_index + 6, "district_mae = abs(y_test_pred_combined - y_test_orig).groupby(df_agg[test_mask].loc[y_test_pred_combined.index, 'district']).mean()\n")
                cell['source'].insert(insert_index + 7, 'print("Top 10 High-Error Districts:")\n')
                cell['source'].insert(insert_index + 8, 'print(district_mae.sort_values(ascending=False).head(10))\n')
                break
        break
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)