import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    if 'source' in cell:
        for line in cell['source']:
            if 'features = ' in line and 'volatility_change' in line:
                print(f"Cell {i}, id {cell.get('id')}")
                for j, line in enumerate(cell['source']):
                    if 'features = ' in line and 'volatility_change' in line:
                        cell['source'][j] = "features = ['lag_7', 'lag_14', 'rolling_mean_7', 'rolling_std_7', 'growth_rate_7', 'month', 'week_of_year', 'day_of_week', 'district_encoded', 'district_volatility', 'state_avg', 'pct_of_state', 'is_weekend', 'is_month_end', 'recent_volatility', 'is_spike']\n"
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)