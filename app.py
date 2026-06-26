from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

phishing_model = joblib.load(
    "models/baseline_logreg.pkl"
)

phishing_vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    text = data["email"]

    X = phishing_vectorizer.transform([text])

    score = phishing_model.decision_function(X)[0]

    prediction = int(score > 0)

    confidence = 1 / (1 + pow(2.71828, -score))

    indices = X.nonzero()[1]

    feature_names = phishing_vectorizer.get_feature_names_out()
    coefficients = phishing_model.coef_[0]

    # explanations for top features
    EXPLANATIONS = {
        "verification": "Requests identity verification",
        "verify": "Requests identity verification",
        "urgent": "Creates a strong sense of false urgency",
        "invoice": "Uses financial pressure",
        "account": "References sensitive account access",
        "password": "Mentions login credentials",
        "login": "Requests authentication",
        "click": "Encourages clicking a link",
        "confirm": "Requests confirmation of information",
        "security": "Mentions account security",
        "bank": "References financial institutions",
        "payment": "Requests or references payments",
        "suspend": "Threatens account suspension",
        "redacted": "Mentions sensitive or hidden information",
        "delivery": "Refers to package or shipment updates, commonly used in fake delivery notification scams",
        "document": "Impersonates shared files or invoices, often used to trick users into opening malicious attachments",
        "restricted": "Uses fear of losing access"
    }

    important = []
    top_features = []

    for idx in indices:
        weight = coefficients[idx]
        if abs(weight) > 0:
            important.append(
                (
                    feature_names[idx],
                    weight
                )
            )

    important.sort(
        key=lambda x:x[1],
        reverse=True
    )

    for word, weight in important[:5]:
        explanation = EXPLANATIONS.get(word)
        if explanation is not None:
            top_features.append(explanation)
        else:
            top_features.append(f"Contains suspicious keyword: '{word}'")

    return jsonify({
        "prediction": prediction,
        "confidence": round(confidence, 3),
        "top_features": top_features,
        "suspicious_words": [word for word, _ in important[:5]]
    })

if __name__ == "__main__":
    app.run(debug=True)