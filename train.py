import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load dataset
df = pd.read_excel("phishing_dataset.xlsx")

# Combine subject and body text
df["combined_text"] = (
    df["subject"].astype(str) + " " + df["email_text"].astype(str)
)

X = df[["combined_text", "has_link", "has_attachment", "urgency_flag"]]
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Feature extraction pipeline
preprocessor = ColumnTransformer(
    transformers=[
        (
            "text",
            TfidfVectorizer(stop_words="english", ngram_range=(1, 2)),
            "combined_text",
        ),
        ("flags", "passthrough", ["has_link", "has_attachment", "urgency_flag"]),
    ]
)

model = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("classifier", MultinomialNB(alpha=0.1)),
    ]
)

# Train and evaluate
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "phishing_detector.pkl")
print("Model saved as phishing_detector.pkl ✅")