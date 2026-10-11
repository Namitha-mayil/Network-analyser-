from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
import json
from predict import predict_batch, predict_single

app = Flask(__name__)
app.secret_key = "super_secret_cyber_key"
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

STATS_FILE = 'stats.json'

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {
        'total_records': 0,
        'normal_count': 0,
        'attack_count': 0,
        'dos_count': 0,
        'probe_count': 0,
        'r2l_count': 0,
        'u2r_count': 0
    }

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def update_stats_from_predictions(predictions):
    stats = load_stats()
    
    stats['total_records'] += len(predictions)
    
    counts = predictions.value_counts().to_dict()
    
    stats['normal_count'] += counts.get('Normal', 0)
    stats['dos_count'] += counts.get('DoS', 0)
    stats['probe_count'] += counts.get('Probe', 0)
    stats['r2l_count'] += counts.get('R2L', 0)
    stats['u2r_count'] += counts.get('U2R', 0)
    
    stats['attack_count'] = stats['dos_count'] + stats['probe_count'] + stats['r2l_count'] + stats['u2r_count']
    
    save_stats(stats)
    return stats

@app.route('/')
def index():
    stats = load_stats()
    return render_template('index.html', stats=stats)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            try:
                # Assuming the CSV doesn't have headers if it's straight from sample
                # But let's read it. We might need to handle headers vs no headers
                df = pd.read_csv(filepath)
                
                # If the first column name looks like a number, it probably has no headers
                if df.columns[0].isdigit() or str(df.columns[0]).replace('.', '', 1).isdigit():
                    import predict
                    import joblib
                    feature_config = joblib.load(os.path.join('model', 'feature_config.pkl'))
                    df = pd.read_csv(filepath, names=feature_config['columns'])
                
                # Process predictions
                result_df = predict_batch(df)
                
                update_stats_from_predictions(result_df['prediction'])
                
                # Prepare data for template
                records = result_df.head(100).to_dict(orient='records') # Show max 100 in table
                
                summary = {
                    'total': len(result_df),
                    'normal': len(result_df[result_df['prediction'] == 'Normal']),
                    'attack': len(result_df[result_df['prediction'] != 'Normal']),
                    'dos': len(result_df[result_df['prediction'] == 'DoS']),
                    'probe': len(result_df[result_df['prediction'] == 'Probe']),
                    'r2l': len(result_df[result_df['prediction'] == 'R2L']),
                    'u2r': len(result_df[result_df['prediction'] == 'U2R']),
                }
                summary['normal_pct'] = round((summary['normal'] / summary['total']) * 100, 2) if summary['total'] > 0 else 0
                summary['attack_pct'] = round((summary['attack'] / summary['total']) * 100, 2) if summary['total'] > 0 else 0
                
                return render_template('analyze.html', records=records, summary=summary, uploaded=True)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
                return redirect(url_for('analyze'))
        else:
            flash('Invalid file format. Please upload a CSV file.', 'danger')
            return redirect(request.url)
            
    return render_template('analyze.html', uploaded=False)

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    result = None
    if request.method == 'POST':
        try:
            # Extract form data
            record_dict = request.form.to_dict()
            
            # Predict
            prediction, confidence = predict_single(record_dict)
            
            # Update stats
            stats = load_stats()
            stats['total_records'] += 1
            if prediction == 'Normal':
                stats['normal_count'] += 1
            else:
                stats['attack_count'] += 1
                if prediction == 'DoS': stats['dos_count'] += 1
                elif prediction == 'Probe': stats['probe_count'] += 1
                elif prediction == 'R2L': stats['r2l_count'] += 1
                elif prediction == 'U2R': stats['u2r_count'] += 1
            save_stats(stats)
            
            result = {
                'prediction': prediction,
                'confidence': confidence,
                'status': 'SAFE' if prediction == 'Normal' else 'ATTACK DETECTED'
            }
        except Exception as e:
            flash(f'Error during prediction: {str(e)}', 'danger')
            
    return render_template('prediction.html', result=result)

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
