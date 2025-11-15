import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('healthcare-dataset-stroke-data.csv')

# clean data 
bmi_mean = df['bmi'].mean()
df['bmi'] = df['bmi'].fillna(bmi_mean)
df.columns = df.columns.str.lower()
df = df.drop('id', axis=1)

# split dataset
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
y_test = df_test.stroke.values
del df_test['stroke']

y_full_train = df_full_train['stroke'].values
X_full_train_df = df_full_train.drop('stroke', axis=1)

# vectorize our new X_full_train_df
dv_full = DictVectorizer(sparse=True)
X_full_train = dv_full.fit_transform(X_full_train_df.to_dict(orient='records'))

model = LogisticRegression(solver='liblinear', C=35, max_iter=1000, random_state=42)
model.fit(X_full_train, y_full_train)

# Save the vectorizer (dv_full)
with open('dv.bin', 'wb') as f_out:
    pickle.dump(dv_full, f_out)
    print("Vectorizer saved to dv.bin")

# Save the final model
with open('model.bin', 'wb') as f_out:
    pickle.dump(model, f_out)
    print("Model saved to model.bin")
