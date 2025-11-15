import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score

# load our saved tools
with open('dv.bin', 'rb') as f_in:
    dv = pickle.load(f_in)

with open('model.bin', 'rb') as f_in:
    model = pickle.load(f_in)


df = pd.read_csv('healthcare-dataset-stroke-data.csv')

# cleaning
bmi_mean = df['bmi'].mean()
df['bmi'] = df['bmi'].fillna(bmi_mean)
df.columns = df.columns.str.lower()
df = df.drop('id', axis=1)

# splitting
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
y_test = df_test['stroke'].values


df_test_features = df_test.drop('stroke', axis=1)
test_dicts = df_test_features.to_dict(orient='records')
X_test = dv.transform(test_dicts)

y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluate Our Final Model
# metric 1: the overall ROC-AUC score
final_auc = roc_auc_score(y_test, y_pred_proba)

# metric 2: the F1-Score at our best threshold (0.09)
best_threshold = 0.09 
y_pred_binary = (y_pred_proba >= best_threshold).astype(int)
final_f1 = f1_score(y_test, y_pred_binary)


print("--- Final Model Report Card (on unseen test data) ---")
print(f"Final ROC-AUC Score: {final_auc:.4f}")
print(f"Final F1-Score (at {best_threshold} threshold): {final_f1:.4f}")