# 🛡️ PhishGuard AI — Intelligent Phishing Email Detection System

An end-to-end Machine Learning web application designed to identify and classify deceptive emails into **Phishing** or **Legitimate** categories. Built using **Scikit-learn** and **Streamlit**, this project combines Natural Language Processing (TF-IDF) on raw email content with heuristic metadata indicators (hyperlinks, attachments, and urgency triggers).

---

## 📌 Problem Statement
Phishing remains one of the most pervasive cyber threats, causing massive credential theft and financial fraud worldwide. Traditional signature-based email filters frequently fail against obfuscated phishing templates and evolving social engineering tactics. 

**PhishGuard AI** solves this by leveraging statistical NLP models trained on linguistic cues, combined with structural metadata analysis to deliver high-confidence, real-time threat verdicts.

---

## 🚀 Key Features

* **Dual-Layer Feature Fusion:** Analyzes textual semantics (`subject` + `email_text`) while evaluating threat flags (`has_link`, `has_attachment`, `urgency_flag`).
* **Real-time Email Scanner:** Interactive UI for immediate text input inspection with instantaneous risk probabilities and confidence scores.
* **Batch Dataset Processing:** Upload multiple `.xlsx` or `.csv` files simultaneously, run batch inferences, and export labeled audits as clean CSV reports.
* **Interactive Confusion Matrix:** Transparent performance breakdown showcasing True Positives, True Negatives, False Alarms, and Missed Threats.
* **High-Performance Pipeline:** Sub-15ms inference latency, completely decoupled from heavy external dependencies.

---

## 🧠 Machine Learning Architecture

The underlying model uses a composite **Scikit-learn Pipeline** equipped with a `ColumnTransformer`:

1. **Text Transformation (`TfidfVectorizer`):**
   * Preprocessing: Lowercasing, punctuation handling, English stopword removal.
   * N-Gram Range: `(1, 2)` (captures single suspicious keywords as well as multi-word phrasing like *"verify account"*, *"urgent action"*).
2. **Flag Features (`passthrough`):**
   * Directly feeds binary flags (`has_link`, `has_attachment`, `urgency_flag`) into the feature matrix.
3. **Classification Engine (`MultinomialNB`):**
   * Utilizes Multinomial Naive Bayes with Laplace smoothing (`alpha=0.1`) optimized for sparse text representations.

---

## 📊 Evaluation & Benchmark Results

The model was evaluated using a stratified 80/20 train-test split on an 800-email benchmark dataset:

| Metric | Score |
| :--- | :--- |
| **Accuracy** | **98.75%** |
| **Precision (Legitimate)** | **0.99** |
| **Recall (Legitimate)** | **0.99** |
| **Precision (Phishing)** | **0.99** |
| **Recall (Phishing)** | **0.99** |
| **F1-Score (Macro Avg)** | **0.99** |

### Confusion Matrix Breakdown (Test Split: 160 Samples)
* **True Legitimate (Safe):** 76
* **True Phishing (Caught Threat):** 82
* **False Phishing (False Alarm):** 1
* **False Legitimate (Missed Phish):** 1

> **Note:** The minor edge cases reflect real-world scenarios such as promotional newsletters featuring urgency cues or stealthy text attacks with masked domains.

---

## 📂 Repository Structure

```text
├── app.py                   # Streamlit interactive web application
├── train.py                 # ML pipeline training and serialization script
├── phishing_detector.pkl    # Serialized Scikit-learn model artifact
├── phishing_dataset.xlsx    # Benchmark training and validation dataset
├── requirements.txt         # Project dependencies
└── README.md                # Comprehensive project documentation
