import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import seaborn as sns

print("Starting Model Training Pipeline...")

# Define Column Names
col_names = ["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty_level"]

# Attack category mapping
attack_mapping = {
    'normal': 'Normal',
    
    # DoS
    'back': 'DoS', 'land': 'DoS', 'neptune': 'DoS', 'pod': 'DoS', 'smurf': 'DoS', 'teardrop': 'DoS',
    'apache2': 'DoS', 'udpstorm': 'DoS', 'processtable': 'DoS', 'worm': 'DoS', 'mailbomb': 'DoS',
    
    # Probe
    'satan': 'Probe', 'ipsweep': 'Probe', 'nmap': 'Probe', 'portsweep': 'Probe', 'mscan': 'Probe', 'saint': 'Probe',
    
    # R2L
    'guess_passwd': 'R2L', 'ftp_write': 'R2L', 'imap': 'R2L', 'phf': 'R2L', 'multihop': 'R2L', 
    'warezmaster': 'R2L', 'warezclient': 'R2L', 'spy': 'R2L', 'xlock': 'R2L', 'xsnoop': 'R2L', 
    'snmpguess': 'R2L', 'snmpgetattack': 'R2L', 'httptunnel': 'R2L', 'sendmail': 'R2L', 'named': 'R2L',
    
    # U2R
    'buffer_overflow': 'U2R', 'loadmodule': 'U2R', 'rootkit': 'U2R', 'perl': 'U2R', 'sqlattack': 'U2R',
    'xterm': 'U2R', 'ps': 'U2R'
}

print("Loading Dataset...")
train_path = os.path.join('dataset', 'KDDTrain+.txt')
df = pd.read_csv(train_path, names=col_names)

# Drop difficulty level as it's not a real feature
df.drop('difficulty_level', axis=1, inplace=True)

# Map labels to categories
df['attack_category'] = df['label'].map(lambda x: attack_mapping.get(x, 'Normal'))
df.drop('label', axis=1, inplace=True)

print("Preparing Features and Target...")
X = df.drop('attack_category', axis=1)
y = df['attack_category']

# Define categorical and numerical features
categorical_features = ['protocol_type', 'service', 'flag']
numerical_features = [col for col in X.columns if col not in categorical_features]

# We do an 80/20 train-test split on the main dataset to evaluate
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Building Preprocessing Pipeline...")
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])

print("Training Logistic Regression Model...")
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1))
])

pipeline.fit(X_train, y_train)

print("Evaluating Model...")
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

print("-" * 30)
print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1-score:  {f1 * 100:.2f}%")
print("-" * 30)

print("\nClassification Report:")
report = classification_report(y_test, y_pred, zero_division=0)
print(report)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
labels = sorted(y_test.unique())

plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - Network Traffic Classification')
plt.tight_layout()

# Save confusion matrix plot
os.makedirs(os.path.join('static', 'images'), exist_ok=True)
plt.savefig(os.path.join('static', 'images', 'confusion_matrix.png'))
print("Confusion matrix saved to static/images/confusion_matrix.png")

# Save the model pipeline and feature config
print("Saving Model Artifacts...")
os.makedirs('model', exist_ok=True)
joblib.dump(pipeline, os.path.join('model', 'logistic_model_pipeline.pkl'))

feature_config = {
    'categorical': categorical_features,
    'numerical': numerical_features,
    'columns': list(X.columns)
}
joblib.dump(feature_config, os.path.join('model', 'feature_config.pkl'))

# Save a small sample for the user to test CSV upload functionality
sample_df = df.sample(50, random_state=42).drop('attack_category', axis=1)
sample_df.to_csv('sample_traffic.csv', index=False, header=False)
print("Saved sample_traffic.csv for testing upload functionality.")

print("Training Complete!")
