import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_auc_score

# train on human data

df = pd.read_csv(
    "../dataset/processed_dataset.csv"
)

# human training set
train_df = df[df["source"] == "human"]

X_train = train_df["clean_text"]
y_train = train_df["label_id"]

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2),
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(
    X_train
)

model = LinearSVC()
model.fit(
    X_train_vec,
    y_train
)

sources = ["chatgpt", "claude", "copilot", "grok"]

for source in sources:

    test_df = df[df["ai_agent"] == source]

    X_test = vectorizer.transform(
        test_df["clean_text"]
    )

    y_test = test_df["label_id"]

    scores = model.decision_function(
        X_test
    )

    print(
        source,
        scores.mean()
    )