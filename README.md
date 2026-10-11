# AI-Based Network Traffic Analyzer / Intrusion Detection System (IDS)

## 1. Project Introduction
The increasing number of cyber threats and unauthorized network activities has made Network Intrusion Detection Systems (NIDS) a critical component of modern cybersecurity. The AI-Based Network Traffic Analyzer is a software application designed to monitor, analyze, and classify network traffic using Machine Learning techniques.

## 2. Project Objective
Build a web-based cybersecurity application that analyzes network traffic records and predicts whether the traffic is:
- **Normal**
- **DoS Attack** (Denial of Service)
- **Probe Attack** (Surveillance/Probing)
- **R2L Attack** (Root to Local)
- **U2R Attack** (User to Root)

The application uses a trained Machine Learning model (Logistic Regression) to automatically classify network traffic based on the features provided in the NSL-KDD dataset.

## 3. Features
- **Batch Traffic Analysis:** Upload network traffic logs (CSV) and classify thousands of records simultaneously.
- **Real-Time Manual Prediction:** Manually enter network parameters to check a single record instantly.
- **Professional Dashboard:** View real-time statistics of analyzed traffic and attack distributions through interactive charts.
- **Performance Metrics:** View the model's accuracy, precision, recall, F1-score, and confusion matrix.
- **Cybersecurity UI:** Modern, dark-themed interface built specifically for a security context.

## 4. Technologies Used
- **Programming Language:** Python 3.x
- **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
- **Web Framework:** Flask
- **Frontend UI:** HTML5, CSS3, JavaScript, Bootstrap 5, FontAwesome
- **Data Visualization:** Chart.js, Matplotlib, Seaborn

## 5. Dataset: NSL-KDD
The project utilizes the **NSL-KDD** dataset, which is a widely accepted benchmark dataset for Network Intrusion Detection. The dataset resolves inherent issues in the KDD'99 dataset by removing redundant records. It contains 41 features for each network connection record.

## 6. Machine Learning Algorithm: Logistic Regression
Logistic Regression is used as the primary classification algorithm.
**Why Logistic Regression?**
- **Simplicity:** It is easy to implement and interpret.
- **Speed & Efficiency:** It trains incredibly fast compared to deep learning models and requires minimal computational resources.
- **Classification Ability:** It excels at classifying linearly separable data. Since our dataset is preprocessed well, Logistic Regression achieves ~98.8% accuracy on the train-test split without overfitting.

## 7. Data Preprocessing
The system preprocesses raw traffic data before feeding it to the model:
1. **Cleaning:** Drops non-feature columns (like difficulty level).
2. **Encoding:** Applies `OneHotEncoder` to categorical features (`protocol_type`, `service`, `flag`).
3. **Scaling:** Applies `StandardScaler` to numerical features so they have a mean of 0 and variance of 1.
4. **Mapping:** Maps 39 specific attack sub-types into 4 main categories (DoS, Probe, R2L, U2R).

## 8. System Architecture
```text
                 NSL-KDD DATASET
                       │
               DATA PREPROCESSING
          ┌────────────┼────────────┐
       Cleaning     Encoding     Scaling
          └────────────┼────────────┘
               LOGISTIC REGRESSION
                       │
                 TRAINED MODEL
                       │
                  FLASK SERVER
          ┌────────────┴────────────┐
   CSV FILE UPLOAD            MANUAL INPUT
          └────────────┬────────────┘
                  PREDICTION
                       │
            ┌─────────────────────┐
            │ NORMAL / DoS /      │
            │ Probe / R2L / U2R   │
            └─────────────────────┘
                       │
                WEB DASHBOARD
```

## 9. Installation & Setup

1. **Clone or Download the Repository.**
2. **Navigate to the Project Directory.**
   ```bash
   cd AI_Based_Network_Analyser
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 10. Training the Model
Before running the web app, you must fetch the data and train the machine learning model.
1. **Download Dataset:**
   ```bash
   python fetch_data.py
   ```
2. **Train Model:**
   ```bash
   python train_model.py
   ```
   This script will train the Logistic Regression model, output performance metrics in the terminal, save the confusion matrix image, and serialize the trained model artifacts into the `model/` directory. It also creates a `sample_traffic.csv` file for testing.

## 11. Running the Flask Application
1. **Start the server:**
   ```bash
   python app.py
   ```
2. **Access the application:** Open your web browser and go to `http://127.0.0.1:5000`

## 12. Using the Application
- **CSV Prediction (Batch):** Go to the "Analyze Traffic" tab. Upload `sample_traffic.csv` (generated during training) to see the model classify multiple records at once.
- **Manual Prediction:** Go to the "Manual Prediction" tab. Fill in the network feature details manually and click "Predict".

## 13. Model Evaluation
The model has been evaluated using an 80/20 train-test split of the `KDDTrain+.txt` dataset.
- **Accuracy:** ~98.89%
- **Precision:** ~98.89%
- **Recall:** ~98.89%
- **F1-Score:** ~98.89%
*(Metrics can be viewed interactively in the "Model Performance" tab of the web app).*

## 14. Project Limitations
- **Dataset Dependency:** The model is trained purely on the NSL-KDD dataset. While accurate within this distribution, it may struggle with modern Zero-Day attacks that don't share features with late-90s/early-2000s network anomalies.
- **Static Signatures:** It acts more as an anomaly/signature detector based on established features rather than a dynamic real-time packet sniffer.

## 15. Future Improvements
- Integration with tools like `Scapy` or `Wireshark (TShark)` to capture live PCAP data and convert it into NSL-KDD features for real-time live network sniffing.
- Implementation of Deep Learning algorithms (e.g., LSTMs) to capture sequential patterns in traffic over time.

---

### Viva Questions & Answers

**Q: What is Network Traffic?**
A: Data moving between computers/devices through a network.

**Q: What is Intrusion Detection?**
A: Finding suspicious or malicious activity in network traffic.

**Q: What is NSL-KDD?**
A: A commonly used cybersecurity dataset containing network traffic records labelled as normal or different types of attacks.

**Q: Why Logistic Regression?**
A: It is simple, extremely fast, computationally efficient, and highly suitable for classification in this academic lightweight IDS implementation.

**Q: Why Flask?**
A: Flask connects the trained Python ML model to a web interface so users can interact with the system through a browser without coding.
