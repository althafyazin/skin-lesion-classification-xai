import os
import numpy as np
import cv2

from .roi_mask import extract_lesion_mask
from .patch_generator import lesion_patches
from .perturbation import apply_patch_perturbation
from .surrogate import train_surrogate
from .text_explainer import generate_text_explanation
from .visualize import visualize_lime_style


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")


def lesion_aware_lime(image, model, gradcam, class_index):

    # 1. ROI mask from Grad-CAM
    mask = extract_lesion_mask(gradcam)

    # 2. Deterministic lesion patches
    
    patches = lesion_patches(mask, image)

    X, y, weights = [], [], []

    for i, patch in enumerate(patches):

        # 3. Deterministic perturbation (remove one patch)
        perturbed = apply_patch_perturbation(image, patch)

        pred = model.predict(
            [perturbed[None], perturbed[None]]
        )[0, class_index]

        # 4. Multi-patch feature vector (IMPORTANT FIX)
        feature = np.ones(len(patches))
        feature[i] = 0   # patch removed

        X.append(feature)
        y.append(pred)

        # 5. Stabilized lesion-aware weight (IMPORTANT FIX)
        lesion_overlap = np.sum(mask & patch) / (np.sum(patch) + 1e-8)
        weight = 0.3 + 0.7 * lesion_overlap
        weights.append(weight)

    # 6. Ridge surrogate
    surrogate = train_surrogate(
        np.array(X), np.array(y), np.array(weights)
    )

    # 7. Text explanation
    explanation_text = generate_text_explanation(
        surrogate.coef_
    )

    # 8. LIME-style visualization (black background)
    explanation_image = visualize_lime_style(
        image, patches, surrogate.coef_, top_k=4
    )

    os.makedirs(STATIC_DIR, exist_ok=True)
    path = os.path.join(STATIC_DIR, "lesion_lime.png")
    cv2.imwrite(path, explanation_image)

    return explanation_text
