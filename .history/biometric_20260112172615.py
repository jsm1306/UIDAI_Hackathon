dfs = []
for file in ['api_data_aadhar_biometric_0_500000.csv',
             'api_data_aadhar_biometric_500000_1000000.csv',
             'api_data_aadhar_biometric_1000000_1500000.csv',
             'api_data_aadhar_biometric_1500000_1861108.csv']:
    path = f"/content/drive/MyDrive/UIDAI/api_data_aadhar_biometric/{file}"
    chunks = pd.read_csv(path, chunksize=100000)
    dfs.append(pd.concat(chunks))

df = pd.concat(dfs, ignore_index=True)
#Converting Date into Dateformat and splitting into more columns
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
#Fill the missing in the columns
df['state'] = df['state'].fillna('Unknown')
df['district'] = df['district'].fillna('Unknown')
df[['bio_age_5_17','bio_age_17_']] = df[['bio_age_5_17','bio_age_17_']].fillna(0)
#Data Type Correction
df['pincode'] = df['pincode'].astype(str)
df.duplicated().sum()
df = df.drop_duplicates()
df = df[(df['bio_age_5_17'] >= 0) & (df['bio_age_17_'] >= 0)]
df_monthly = df.groupby(
    ['state','district','year','month']
)[['bio_age_5_17','bio_age_17_']].sum().reset_index()
df_monthly.to_csv('/content/drive/MyDrive/UIDAI/api_data_aadhar_biometric/processed_aadhaar.csv', index=False)
df['enrollment'] = df['bio_age_5_17'] + df['bio_age_17_']
df['target_log'] = np.log1p(df['enrollment'])
df = df.sort_values(['state', 'district', 'date']).reset_index(drop=True)
df['lag_7']  = df.groupby(['state', 'district'])['enrollment'].shift(7)
df['lag_14'] = df.groupby(['state', 'district'])['enrollment'].shift(14)
# Use shifted rolling means to avoid peeking at current/future enrollment
df['rolling_mean_7'] = df.groupby(['state','district'])['enrollment'].transform(lambda x: x.shift(7).rolling(7, min_periods=1).mean())

# Use shifted rolling means for 14-day window
df['rolling_mean_14'] = df.groupby(['state','district'])['enrollment'].transform(lambda x: x.shift(14).rolling(14, min_periods=1).mean())
# Shift before computing rolling std to prevent leakage
df['rolling_std_7'] = df.groupby(['state','district'])['enrollment'].transform(lambda x: x.shift(7).rolling(7, min_periods=1).std())

# Shift before computing rolling std for 14-day window
df['rolling_std_14'] = df.groupby(['state','district'])['enrollment'].transform(lambda x: x.shift(14).rolling(14, min_periods=1).std())
# Compute state-date average, then shift by 1 day per state to avoid contemporaneous leakage
# (state_date_avg is a temporary per-state-per-date value)
df['state_date_avg'] = df.groupby(['state','date'])['enrollment'].transform('mean')
# Use previous day's state average as the feature
df['state_avg_enrollment'] = df.groupby('state')['state_date_avg'].shift(1)
# Ratio relative to lagged state average
df['district_state_ratio'] = df['enrollment'] / (df['state_avg_enrollment'] + 1)
# Cleanup
df.drop(columns=['state_date_avg'], inplace=True)

df['target_log'] = np.log1p(df['enrollment'])
feature_cols = [
    'lag_7', 'lag_14',
    'rolling_mean_7', 'rolling_mean_14',
    'rolling_std_7', 'rolling_std_14',
    'state_avg_enrollment',
    'district_state_ratio'
]
print("Dataset shape before dropna:", df.shape)
print("NaN counts for features and target:\n", df[feature_cols + ['target_log']].isna().sum())

# Drop rows missing any required feature or target
df_model = df.dropna(subset=feature_cols + ['target_log']).copy()
print("Dataset shape after dropna:", df_model.shape)

# sample weights and splits
df_model['sample_weight'] = np.sqrt(df_model['enrollment'])
train_df = df_model[(df_model['month'] >= 3) & (df_model['month'] <= 10)]
val_df   = df_model[df_model['month'] == 11]
test_df  = df_model[df_model['month'] == 12]
print("Train/Val/Test sizes:", train_df.shape[0], val_df.shape[0], test_df.shape[0])
print("Enrollment sums (raw / used in model):", df['enrollment'].sum(), df_model['enrollment'].sum())
X_train = train_df[feature_cols]
y_train = train_df['target_log']
w_train = train_df['sample_weight']

X_val = val_df[feature_cols]
y_val = val_df['target_log']
w_val = val_df['sample_weight']

X_test = test_df[feature_cols]
y_test = test_df['target_log']
import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

lgb_model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='rmse',
    callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=50)],
    # verbose=False # Set verbose to False to avoid duplicate logging if using callback verbose
)
import numpy as np
from sklearn.metrics import mean_squared_error

lgb_pred_log = lgb_model.predict(X_test)
lgb_pred = np.expm1(lgb_pred_log)
y_true = np.expm1(y_test)

lgb_rmse = np.sqrt(mean_squared_error(y_true, lgb_pred))
print("LightGBM RMSE:", lgb_rmse)
