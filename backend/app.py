import os
import numpy as np
from flask import Flask, request, render_template
from PIL import Image

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from model_loader import load_trained_model
from preprocess import preprocess_image
from predict import predict_image

from explainability.gradcam import make_gradcam_heatmap, save_gradcam
from explainability.lime_explainer import generate_lime

# 🔹 NEW: lesion-aware LIME (separate, does NOT touch old LIME)
from explainability.lime_lesion_aware.explainer import lesion_aware_lime

app = Flask(__name__)

# Load model once
model = load_trained_model()
LAST_CONV_LAYER = "block14_sepconv2_act"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
LAST_IMAGE_PATH = os.path.join(STATIC_DIR, "last_uploaded.jpg")

DISPLAY_NAMES = {
    "AKIEC": "Actinic Keratosis",
    "BCC": "Basal Cell Carcinoma",
    "BKL": "Benign Keratosis",
    "DF": "Dermatofibroma",
    "MEL": "Melanoma",
    "NV": "Melanocytic Nevi",
    "VASC": "Vascular Lesions",
    "UNKNOWN": "Unknown / Not in trained classes"
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        # ------------------ Load Image ------------------
        file = request.files["image"]
        image = Image.open(file).convert("RGB")

        os.makedirs(STATIC_DIR, exist_ok=True)
        image.save(LAST_IMAGE_PATH)

        # ------------------ Predict ------------------
        img_tensor = preprocess_image(image)

        predicted_class, confidence, probabilities, pred_index = predict_image(
            model, img_tensor
        )

        display_class = DISPLAY_NAMES[predicted_class]
        display_probs = {DISPLAY_NAMES[k]: v for k, v in probabilities.items()}

        lesion_text = None  # default

        # ------------------ Explainability ------------------
        if pred_index is not None:

            # Grad-CAM
            heatmap = make_gradcam_heatmap(
                img_tensor, model, LAST_CONV_LAYER, pred_index
            )
            resized = np.array(image.resize((299, 299)))
            save_gradcam(resized, heatmap)

            # Default LIME (baseline)
            generate_lime(resized, model, pred_index)

            # ✅ Modified lesion-aware LIME (NEW)
            lesion_text = lesion_aware_lime(
                resized, model, heatmap, pred_index
            )

        return render_template(
            "index.html",
            show_result=True,
            predicted_class=display_class,
            confidence=confidence,
            probabilities=display_probs,
            lesion_text=lesion_text
        )

    return render_template("index.html", show_result=False)

if __name__ == "__main__":
    app.run(debug=True)
