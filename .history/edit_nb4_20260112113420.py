import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if 'source' in cell and any('Top 10 High-Error Districts' in line for line in cell['source']):
        for i, line in enumerate(cell['source']):
            if 'print(district_mae.sort_values(ascending=False).head(10))' in line:
                insert_index = i + 1
                cell['source'].insert(insert_index, '\n')
                cell['source'].insert(insert_index + 1, '# Investigate top-error district: North 24 Parganas\n')
                cell['source'].insert(insert_index + 2, "district_name = 'North 24 Parganas'\n")
                cell['source'].insert(insert_index + 3, "district_data = df_agg[test_mask & (df_agg['district'] == district_name)]\n")
                cell['source'].insert(insert_index + 4, "district_pred = y_test_pred_combined[district_data.index]\n")
                cell['source'].insert(insert_index + 5, "district_actual = y_test_orig[district_data.index]\n")
                cell['source'].insert(insert_index + 6, "print(f'\\nInvestigation for {district_name}:')\n")
                cell['source'].insert(insert_index + 7, "print(f'Volatility: {district_data[\"district_volatility\"].iloc[0]:.2f}')\n")
                cell['source'].insert(insert_index + 8, "print(f'Mean enrollment: {district_data[\"total_enrollment\"].mean():.2f}')\n")
                cell['source'].insert(insert_index + 9, "print(f'MAPE: {mean_absolute_percentage_error(district_actual, district_pred):.4f}')\n")
                cell['source'].insert(insert_index + 10, "plt.figure(figsize=(10,6))\n")
                cell['source'].insert(insert_index + 11, "plt.plot(district_data['date'], district_actual, label='Actual', marker='o')\n")
                cell['source'].insert(insert_index + 12, "plt.plot(district_data['date'], district_pred, label='Predicted', marker='x')\n")
                cell['source'].insert(insert_index + 13, "plt.title(f'Actual vs Predicted for {district_name}')\n")
                cell['source'].insert(insert_index + 14, "plt.xlabel('Date')\n")
                cell['source'].insert(insert_index + 15, "plt.ylabel('Enrollment')\n")
                cell['source'].insert(insert_index + 16, "plt.legend()\n")
                cell['source'].insert(insert_index + 17, "plt.xticks(rotation=45)\n")
                cell['source'].insert(insert_index + 18, "plt.show()\n")
                break
        break
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)