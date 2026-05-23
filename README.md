# Cyber Threat Detection Using Supervised Machine Learning

University of Basrah — Computer Engineering Department
Author: Ali Amer Ibrahim Supervisor: M.Sc. Amjed Ahmed Majied
Academic Year: 2025–2026

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask_/_Kotlin-orange.svg)](https://flask.palletsprojects.com/)

An end-to-end cyber security production system designed to detect Android malware via **Static Permission Analysis** using a highly optimized **Random Forest Classifier**. The solution features a live Android application that extracts application permissions and communicates over HTTP with a containerized/local Flask REST API, delivering high-accuracy security predictions in **under 2 seconds**.

Developed as a graduation project for the Council of the Engineering College, **University of Basrah**.

---

## Project Overview & Intent
With over 3.9 billion active Android devices worldwide, the mobile threat landscape has expanded exponentially, witnessing over 14 million malware attacks in 2025 alone. Traditional defenses rely heavily on signature-based detection, which fails against obfuscated or unseen malware variants. 

This project solves this research gap by utilizing **Android Permissions** as immutable behavioral fingerprints. Since permissions are declared statically in the `AndroidManifest.xml` and cannot be hidden by code obfuscation, they provide an ideal, lightweight, and proactive signal for detecting malware before execution.

---

## System Architecture & Component Interactions

The system leverages a decoupled Client-Server architecture separating mobile-side lightweight data collection from heavy machine learning inference tasks.

[ Android Client (Mobile) ]
│
▼ (Extracts Manifest Permissions via PackageManager)
[ Binary Vector Generation ]
│
▼ (Sends HTTP POST JSON payload)
[ Flask REST API (Server) ] ──> [ Feature Engineering Unit (7 Derived Features) ]
│                                        │
▼                                        ▼
[ Final Prediction Result ] <── [ Optimized Random Forest Classifier (Threshold=0.3) ]

### Component Breakdown:
1. **Android Application (Kotlin/Client):** Uses Android's `PackageManager` API to automatically scan all installed apps, extracts their declared permissions, maps them to a binary vector space, and dispatches real-time classification queries.
2. **Flask REST API (Server Backend):** A stateless HTTP server that exposes inference endpoints, receives permission arrays, injects advanced engineered behavioral indicators, and queries the machine learning model.
3. **Machine Learning Model:** A serialized ensemble Random Forest model tuned with class weights and custom risk-probability thresholds to dramatically reduce False Negatives.

---

## Project Workflow & Operations

### End-to-End Execution Flow
1. **Initiation:** The user opens the Android security app and taps the "Scan System" button.
2. **Local Processing:** The mobile client scans installed APKs, parses their manifests, and maps active permissions to an 86-bit binary format (1 if requested, 0 if absent).
3. **Transmission:** The mobile app batches the binary vectors and pushes an HTTP POST request containing JSON objects to the Flask backend.
4. **Backend Ingestion & Augmentation:** The Flask API captures the vector and programmatically generates **7 Engineered Behavioral Features** (e.g., specific permission groups, ratios).
5. **Inference Execution:** The data passes into the trained `RandomForestClassifier`. The classification boundary utilizes a conservative **0.3 probability threshold** (Optimized to catch 98.67% of malware).
6. **Response Delivery:** The backend converts outputs into a structured JSON response object and responds to the client, displaying a clear threat evaluation screen in real time.

---

## 📈 Machine Learning Model & Dataset Information

### Dataset Properties
* **Source:** Derived from Kaggle public repository of Android applications.
* **Original Distribution:** 29,332 raw records with high row duplications.
* **Preprocessed Dataset:** 7,491 completely unique deduplicated records (4,867 benign applications and 2,624 malicious records) ensuring balanced learning and zero null data points.
* **Validation Strategy:** Stratified 80/20 train-test partition yielding exactly 1,499 clean samples in the final test matrix.

### Random Forest Classifier Design
The project implements a **Random Forest Ensemble** containing 600 independent decision trees. To handle minor data imbalances and emphasize security-first operations, custom `class_weight='balanced'` criteria were passed into Scikit-Learn.

#### Feature Engineering (Expanding the Space From 86 to 93 columns)
Seven high-level behavioral attributes were introduced to capture systemic intents:
* `sensitive_permission_count`: Combined declarations of high-risk properties (`READ_PHONE_STATE`, `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`).
* `network_permission_ratio`: Calculated ratio of internet/network permissions relative to overall requests.
* `persistence_permission_count`: Total requests for background/boot persistence intents.

#### Classification Threshold Optimization
While the traditional model boundaries are fixed at `0.5`, this system sets the critical prediction threshold to **0.3**:
$$\hat{y} = \begin{cases} 1 & \text{if } P(\text{Malware}) \geq 0.3 \\ 0 & \text{otherwise} \end{cases}$$
This strategic optimization reduced False Negatives by **86.3%** compared to the baseline model, dropping the count to just 7 undetected threats.

### Empirical Results & Performance Progress
* **Recall (Sensitivity):** **98.67%** (The primary objective: ensuring malware rarely slips past defenses).
* **Accuracy:** **85.26%**
* **Area Under ROC Curve (ROC-AUC):** **97.48%**

---

## Project Structure

```text
cyber-threat-detection/
├── data/
│   └── data.csv
├── models/
│   └── malware_rf_final.pkl
├── notebooks/
│   ├── finalModel.ipynb
│   └── fortyFeatuers.ipynb
├── server/
│   └── app.py
├── android_app/
│   └── ...
├── .gitignore
├── LICENSE
└── requirements.txt
```

---

## Installation & Local Deployment Guide
Prerequisites
Ensure you have Python 3.9+ installed along with Git.

## 1. Environment Setup

### Clone the repository
git clone [https://github.com/YOUR_USERNAME/cyber-threat-detection.git](https://github.com/YOUR_USERNAME/cyber-threat-detection.git)
cd cyber-threat-detection

### Create a isolated virtual environment
python -m venv venv

### Activate the environment
### On Windows:
venv\Scripts\activate
### On macOS/Linux:
source venv/bin/activate

### Install all backend requirements
pip install -r requirements.txt

## 2. Operating the Jupyter Notebooks
### To run, review, or retrain the models:

pip install jupyter
jupyter notebook notebooks/finalModel.ipynb

## 3. Launching the Flask REST API Server

python server/app.py

### The server will boot locally at http://127.0.0.1:5000/.

## 4. Running/Testing the API via Python Client
### You can simulate a transaction payload using the following payload format:

import requests

url = "[http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict)"
payload = {
    "permissions": [0, 1, 0, 0, 1, ..., 0] # 86 binary elements array
}
response = requests.post(url, json=payload)
print(response.json())

## System Screenshots

## Use Case: Client-Manager/User Interactions
### Actors Involved:
#### End-User (Client Mobile Node): Demands instant application risk classification without processing or battery strain.

#### Security Manager (The ML System Environment): Handles rules, validates vectors, generates calculations, and provides security declarations.

[ End-User (Client) ] ───── (Requests Scan) ─────> [ Android UI Node ]
         │                                               │
         │ <─── (Displays Visual Malware Alerts) ────────┤
         ▼                                               ▼
[ API Ingestion Port ] ── (Infers Risk Score) ──> [ System Classifier ]


## Challenges Faced & Future Roadmap
### Challenges Overcome:
Class Imbalance & Evasion: Traditional configurations missed sophisticated malware families. Solved by designing 7 custom behavioral metrics and re-anchoring thresholds down to 0.3.

### Deployment Gap: Bridged the divide between code execution within isolated Jupyter Notebooks and live runtime transactions over Android clients.

### Roadmap & Future Extensions:
### Dynamic Analysis Integration: Implementing a sandbox layer to analyze API system actions in real-time alongside static manifests.

### Explainable AI (XAI): Integrating SHAP or LIME frameworks into the server backend to return exactly why a certain application was flagged as a threat.

### On-Device Inference: Porting the Random Forest model into TensorFlow Lite (TFLite) format to run natively on the mobile OS without requiring internet connectivity.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
Prepared By: Hussein Zuhair Kadhim & Ali Amer Ibrahim
Project Supervisor: M.Sc. Amjed Ahmed Majied
Department of Computer Engineering, University of Basrah, 2026.
