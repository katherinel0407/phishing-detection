import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    classification_report,
    accuracy_score,
    roc_auc_score
)



df = pd.read_csv(
    "../dataset/processed_dataset.csv"
)

# phishing only dataset
phishing_df = df[
    df["label"] == "phishing"
].copy()

# new labels:
# 0 = human phishing (instead of legitimate)
# 1 = AI phishing (instead of llm)

phishing_df["ai_label"] = (
    phishing_df["source"] == "llm"
).astype(int)

# train/test splitting
X = phishing_df["clean_text"]
y = phishing_df["ai_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2),
    stop_words="english"
)
X_train_vec = vectorizer.fit_transform(
    X_train
)
X_test_vec = vectorizer.transform(
    X_test
)

# modeling
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)
model.fit(
    X_train_vec,
    y_train
)

# accuracy reports
y_pred = model.predict(
    X_test_vec
)

y_prob = model.predict_proba(
    X_test_vec
)[:,1]

print(
    classification_report(
        y_test,
        y_pred
    )
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred
    )
)

print(
    "AUROC:",
    roc_auc_score(
        y_test,
        y_prob
    )
)

# let's look at what makes it human
coef_df = pd.DataFrame({
    "feature":
        vectorizer.get_feature_names_out(),
    "coef":
        model.coef_[0]
})

print(
    coef_df
    .sort_values("coef")
    .head(20)
)

# and most AI?
print(
    coef_df
    .sort_values(
        "coef",
        ascending=False
    )
    .head(20)
)

# errors
results = pd.DataFrame({
    "text": X_test.values,
    "actual": y_test.values,
    "predicted": y_pred
})

errors = results[
    results["actual"] != results["predicted"]
]