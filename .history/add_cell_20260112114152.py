import json
with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'r') as f:
    nb = json.load(f)

# New cell for investigation
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Investigate Top Error Districts\n",
        "import matplotlib.pyplot as plt\n",
        "from sklearn.metrics import mean_absolute_percentage_error\n",
        "\n",
        "# Get top 5 error districts\n",
        "top_districts = district_mae.sort_values(ascending=False).head(5).index.tolist()\n",
        "print(\"Investigating top 5 error districts:\", top_districts)\n",
        "\n",
        "for district_name in top_districts:\n",
        "    district_data = df_agg[test_mask & (df_agg['district'] == district_name)]\n",
        "    if len(district_data) == 0:\n",
        "        print(f\"No test data for {district_name}\")\n",
        "        continue\n",
        "    district_pred = y_test_pred_combined[district_data.index]\n",
        "    district_actual = y_test_orig[district_data.index]\n",
        "    \n",
        "    print(f\"\\nInvestigation for {district_name}:\")\n",
        "    print(f\"Volatility: {district_data['district_volatility'].iloc[0]:.2f}\")\n",
        "    print(f\"Mean enrollment: {district_data['total_enrollment'].mean():.2f}\")\n",
        "    print(f\"MAPE: {mean_absolute_percentage_error(district_actual, district_pred):.4f}\")\n",
        "    print(f\"Data points: {len(district_data)}\")\n",
        "    \n",
        "    plt.figure(figsize=(10,6))\n",
        "    plt.plot(district_data['date'], district_actual, label='Actual', marker='o')\n",
        "    plt.plot(district_data['date'], district_pred, label='Predicted', marker='x')\n",
        "    plt.title(f'Actual vs Predicted for {district_name}')\n",
        "    plt.xlabel('Date')\n",
        "    plt.ylabel('Enrollment')\n",
        "    plt.legend()\n",
        "    plt.xticks(rotation=45)\n",
        "    plt.show()\n"
    ]
}

nb['cells'].append(new_cell)

with open('s:/UIDAI_Hackathon/Ensemble.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)