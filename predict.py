import os
import joblib
import pandas as pd

# Load artifacts
model_path = os.path.join('model', 'logistic_model_pipeline.pkl')
config_path = os.path.join('model', 'feature_config.pkl')

pipeline = None
feature_config = None

def load_artifacts():
    global pipeline, feature_config
    if pipeline is None or feature_config is None:
        if os.path.exists(model_path) and os.path.exists(config_path):
            pipeline = joblib.load(model_path)
            feature_config = joblib.load(config_path)
        else:
            raise FileNotFoundError("Model artifacts not found. Please train the model first.")

def predict_batch(df):
    load_artifacts()
    
    # Ensure all required columns are present (fill missing with 0 or mode)
    required_columns = feature_config['columns']
    
    # Filter the df to have the same columns in the same order
    # Note: if it's raw uploaded traffic, it might not have the 'label' or 'difficulty_level'
    df_processed = pd.DataFrame(index=df.index)
    
    for col in required_columns:
        if col in df.columns:
            df_processed[col] = df[col]
        else:
            if col in feature_config['categorical']:
                df_processed[col] = 'unknown' # Missing categorical
            else:
                df_processed[col] = 0 # Missing numerical
    
    predictions = pipeline.predict(df_processed)
    
    # Add predictions to original dataframe
    df['prediction'] = predictions
    
    return df

def predict_single(record_dict):
    load_artifacts()
    
    df = pd.DataFrame([record_dict])
    
    df_processed = pd.DataFrame(index=df.index)
    
    for col in feature_config['columns']:
        if col in df.columns and pd.notna(df[col].iloc[0]) and df[col].iloc[0] != '':
            df_processed[col] = df[col]
        else:
            if col in feature_config['categorical']:
                if col == 'protocol_type': df_processed[col] = 'tcp'
                elif col == 'service': df_processed[col] = 'http'
                elif col == 'flag': df_processed[col] = 'SF'
                else: df_processed[col] = 'unknown'
            else:
                df_processed[col] = 0.0
                
    # Ensure types are correct
    for col in feature_config['numerical']:
        df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce').fillna(0.0)
        
    prediction = pipeline.predict(df_processed)[0]
    
    # Try to get probability for confidence score (if supported)
    confidence = "N/A"
    try:
        probabilities = pipeline.predict_proba(df_processed)[0]
        confidence = f"{max(probabilities) * 100:.2f}%"
    except Exception:
        pass
        
    return prediction, confidence
