import json
with open('s:/UIDAI_Hackathon/spikeprediction.ipynb', 'r') as f:
    nb = json.load(f)

# Add spike classifier training cell
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# Train Spike Classification Model\n',
        '# Features for classification\n',
        'classification_features = [\n',
        '    \"month\", \"day_of_week\", \"week_of_year\",\n',
        '    \"lag_1\", \"lag_7\", \"lag_14\",\n',
        '    \"rolling_mean_7\", \"rolling_std_7\", \"growth_rate_7\",\n',
        '    \"cv\", \"district_volatility\"\n',
        ']\n',
        '\n',
        '# Prepare data\n',
        'X = df_agg[classification_features]\n',
        'y = df_agg[\"spike_label\"]\n',
        '\n',
        '# Split by time (train on earlier months, test on later)\n',
        'train_mask = df_agg[\"date\"].dt.month <= 10\n',
        'X_train = X[train_mask]\n',
        'y_train = y[train_mask]\n',
        'X_test = X[~train_mask]\n',
        'y_test = y[~train_mask]\n',
        '\n',
        'print(f\"Train shape: {X_train.shape}, Test shape: {X_test.shape}\")\n',
        'print(f\"Train spike ratio: {y_train.mean():.3f}, Test spike ratio: {y_test.mean():.3f}\")\n',
        '\n',
        '# Train LightGBM Classifier\n',
        'spike_classifier = lgb.LGBMClassifier(\n',
        '    n_estimators=100,\n',
        '    learning_rate=0.1,\n',
        '    max_depth=6,\n',
        '    scale_pos_weight=len(y_train) / y_train.sum(),  # Handle class imbalance\n',
        '    random_state=42\n',
        ')\n',
        '\n',
        'spike_classifier.fit(X_train, y_train)\n',
        '\n',
        '# Predictions\n',
        'y_pred_proba = spike_classifier.predict_proba(X_test)[:, 1]\n',
        'y_pred = (y_pred_proba > 0.5).astype(int)\n',
        '\n',
        'print(\"Classification Report:\")\n',
        'print(classification_report(y_test, y_pred))\n',
        'print(f\"AUC-ROC: {roc_auc_score(y_test, y_pred_proba):.3f}\")\n',
        '\n',
        '# Feature importance\n',
        'lgb.plot_importance(spike_classifier, max_num_features=10)\n',
        'plt.title(\"Spike Classifier Feature Importance\")\n',
        'plt.show()'
    ]
})

with open('s:/UIDAI_Hackathon/spikeprediction.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)