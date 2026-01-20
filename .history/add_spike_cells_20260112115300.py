import json
with open('s:/UIDAI_Hackathon/spikeprediction.ipynb', 'r') as f:
    nb = json.load(f)

# Add data preprocessing cell
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Data Preprocessing and Feature Engineering\n',
        'df_agg = df.groupby([\"date\", \"district\"]).agg({\n',
        '    \"total_enrollment\": \"sum\"\n',
        '}).reset_index()\n',
        '\n',
        '# Add district-level statistics\n',
        'district_stats = df_agg.groupby(\"district\")[\"total_enrollment\"].agg([\"mean\", \"std\"]).reset_index()\n',
        'district_stats.columns = [\"district\", \"district_mean\", \"district_std\"]\n',
        'df_agg = df_agg.merge(district_stats, on=\"district\")\n',
        '\n',
        '# Label spikes: enrollment > mean + 2*std for that district\n',
        'df_agg[\"spike_label\"] = ((df_agg[\"total_enrollment\"] - df_agg[\"district_mean\"]) > 2 * df_agg[\"district_std\"]).astype(int)\n',
        '\n',
        'print(f\"Spike days: {df_agg[\"spike_label\"].sum()} out of {len(df_agg)} ({df_agg[\"spike_label\"].mean():.1%})\")\n',
        'print(df_agg.head())'
    ]
})

# Add feature engineering cell
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Feature Engineering for Spike Classification\n',
        'df_agg = df_agg.sort_values([\"district\", \"date\"])\n',
        '\n',
        '# Time-based features\n',
        'df_agg[\"month\"] = df_agg[\"date\"].dt.month\n',
        'df_agg[\"day_of_week\"] = df_agg[\"date\"].dt.dayofweek\n',
        'df_agg[\"week_of_year\"] = df_agg[\"date\"].dt.isocalendar().week\n',
        '\n',
        '# Lag features\n',
        'for lag in [1, 7, 14]:\n',
        '    df_agg[f\"lag_{lag}\"] = df_agg.groupby(\"district\")[\"total_enrollment\"].shift(lag)\n',
        '\n',
        '# Rolling statistics\n',
        'df_agg[\"rolling_mean_7\"] = df_agg.groupby(\"district\")[\"total_enrollment\"].shift(1).rolling(7).mean()\n',
        'df_agg[\"rolling_std_7\"] = df_agg.groupby(\"district\")[\"total_enrollment\"].shift(1).rolling(7).std()\n',
        '\n',
        '# Growth rates\n',
        'df_agg[\"growth_rate_7\"] = (df_agg[\"lag_1\"] - df_agg[\"lag_7\"]) / df_agg[\"lag_7\"]\n',
        '\n',
        '# Volatility measures\n',
        'df_agg[\"cv\"] = df_agg[\"rolling_std_7\"] / df_agg[\"rolling_mean_7\"]\n',
        'df_agg[\"district_volatility\"] = df_agg[\"district_std\"]\n',
        '\n',
        '# Drop NaN values\n',
        'df_agg = df_agg.dropna()\n',
        'print(f\"After feature engineering: {df_agg.shape}\")\n',
        'print(df_agg.columns.tolist())'
    ]
})

with open('s:/UIDAI_Hackathon/spikeprediction.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)