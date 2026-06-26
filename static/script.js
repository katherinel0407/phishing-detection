async function analyzeEmail() {

    const email =
        document.getElementById("email").value;

    const response =
        await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email
            })
        });

    const data = await response.json();

    let html = `
        <div class="card">

            <h2>
                ${data.prediction ? "🚨 Likely Phishing" : "✅ Legitimate"}
            </h2>

            <p>
                <strong>Confidence:</strong>
                ${(data.confidence * 100).toFixed(1)}%
            </p>
    `;

    // Add each important feature
    if (data.prediction) {
        html += `
            <h3>Why was this flagged?</h3>

            <ul>
        `;
        data.top_features.forEach(feature => {
            html += `<li>${feature}</li>`;
        });

        html += `
            </ul>

            <h3>Suspicious Keywords</h3>

            <p>${data.suspicious_words.join(", ")}</p>
        `;
    }

    html += `
        </div>
    `;

    document.getElementById("results").innerHTML = html;
}