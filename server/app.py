
from flask import Flask, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# ===== Load model =====
with open("/content/flask_app/model/malware_rf_final.pkl", "rb") as f:
    data = pickle.load(f)

model         = data["model"]
threshold     = data["threshold"]
feature_names = data["features"]

# ===== Predict endpoint =====
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not request.is_json:
            return error_response("INVALID_FORMAT", "Request must be JSON")

        content = request.get_json()

        if "features" not in content:
            return error_response("MISSING_FIELD", "'features' field is required")

        feature_dict = content["features"]

        missing = [f for f in feature_names if f not in feature_dict]
        if missing:
            return error_response("MISSING_FEATURE", f"Missing feature(s): {missing}")

        X = np.array(
            [feature_dict[f] for f in feature_names],
            dtype=float
        ).reshape(1, -1)

        prob = model.predict_proba(X)[0][1]
        pred = int(prob >= threshold)

        return jsonify({
            "status": "ok",
            "prediction": pred,
            "probability": round(float(prob), 4),
            "threshold": threshold
        })

    except ValueError:
        return error_response("INVALID_VALUE", "All features must be numeric")
    except Exception as e:
        return error_response("INTERNAL_ERROR", str(e))

# ===== Health check =====
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# ===== Error helper =====
def error_response(code, message, status=400):
    return jsonify({
        "status": "error",
        "error_code": code,
        "message": message
    }), status

if __name__ == "__main__":
    app.run(port=5000)
