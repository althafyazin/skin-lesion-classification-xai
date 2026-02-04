# backend/explainability/visualize.py

import numpy as np
import cv2

def visualize_lime_style(image, patches, weights, top_k=4):
    """
    Create a LIME-style visualization:
    - black background
    - only important regions shown
    - sharp boundaries (no heatmap)
    """

    image = image.copy()
    h, w, _ = image.shape

    # Normalize weights
    weights = np.array(weights)
    abs_weights = np.abs(weights)

    # Select top-k influential patches
    top_indices = np.argsort(abs_weights)[-top_k:]

    # Start with black canvas
    output = np.zeros_like(image)

    # Overlay selected patches
    for idx in top_indices:
        mask = patches[idx]

        # Copy original pixels where mask is true
        output[mask] = image[mask]

        # Optional: draw boundary
        contours, _ = cv2.findContours(
            mask.astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(output, contours, -1, (0, 255, 255), 2)

    return output
