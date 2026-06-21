import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

# loading data
df = pd.read_csv(
    "../dataset/processed_dataset.csv"
)

# human training set
train_df = df[
    df["source"] == "human"
]

# LLM testing set
test_df = df[
    df["source"] == "llm"
]

# split datasets for model
X_train = train_df["clean_text"]
y_train = train_df["label_id"]

X_test = test_df["clean_text"]
y_test = test_df["label_id"]

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


model = LogisticRegression(
    max_iter=1000
)
model.fit(
    X_train_vec,
    y_train
)
y_pred = model.predict(
    X_test_vec
)

print("\nHuman to LLM Experiment\n")

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred
    )
)

print(
    classification_report(
        y_test,
        y_pred
    )
)