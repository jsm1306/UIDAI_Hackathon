import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if cell['id'] == 'VSC-98a14d54':
        for i, line in enumerate(cell['source']):
            if 'features = ' in line and 'volatility_change' in line:
                cell['source'][i] = "features = ['lag_7', 'lag_14', 'rolling_mean_7', 'rolling_std_7', 'growth_rate_7', 'month', 'week_of_year', 'day_of_week', 'district_encoded', 'district_volatility', 'state_avg', 'pct_of_state', 'is_weekend', 'is_month_end', 'recent_volatility', 'is_spike']\n"
                break
        break
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)