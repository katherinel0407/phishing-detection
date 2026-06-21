import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, classification_report

import seaborn as sns
import matplotlib.pyplot as plt

import joblib

df = pd.read_csv("../dataset/processed_dataset.csv")

# defining X and Y
X = df["clean_text"]
y = df["label"]
# let's also differentiate by source
source = df["source"]

# train/test split
X_train, X_test, y_train, y_test, source_train, source_test = train_test_split(
    X,
    y,
    source,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# using TF-IDF
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2),
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# train
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)

results = pd.DataFrame({
    "source": source_test,
    "actual": y_test,
    "predicted": y_pred
})

print(results)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
for src in ["human", "llm"]:
    subset = results[results["source"] == src]

    print(f"\n===== {src.upper()} =====")

    print(
        classification_report(
            subset["actual"],
            subset["predicted"]
        )
    )

# save these models
joblib.dump(model, "../models/baseline_logreg.pkl")

joblib.dump(
    vectorizer,
    "../models/tfidf_vectorizer.pkl"
)

# let's see what emails were misclassified
errors = results[
    results["actual"] != results["predicted"]
]

print(f"Total Errors: {len(errors)}")
print(errors.head(20))
