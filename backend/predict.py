import numpy as np

# ⚠️ MUST MATCH TRAINING LABEL ORDER EXACTLY
CLASS_NAMES = ["AKIEC", "BCC", "BKL", "DF", "MEL", "NV", "VASC"]

CONFIDENCE_THRESHOLD = 0.70


def predict_image(model, img_tensor):
    """
    Returns:
    predicted_class (str)
    confidence (float)
    probabilities (dict)
    pred_index (int or None)
    """

    # Ensemble model → needs TWO identical inputs
    preds = model.predict([img_tensor, img_tensor], verbose=0)[0]

    pred_index = int(np.argmax(preds))
    confidence = float(preds[pred_index])

    probabilities = {
        CLASS_NAMES[i]: float(preds[i])
        for i in range(len(CLASS_NAMES))
    }

    # -------- OOD rejection --------
    if confidence < CONFIDENCE_THRESHOLD:
        return (
            "UNKNOWN",
            confidence,
            probabilities,
            None
        )

    return CLASS_NAMES[pred_index], confidence, probabilities, pred_index
