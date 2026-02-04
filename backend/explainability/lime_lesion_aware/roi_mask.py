import cv2
import numpy as np

def extract_lesion_mask(gradcam, threshold=0.5):
    heatmap = cv2.resize(gradcam, (299, 299))
    heatmap = heatmap / (heatmap.max() + 1e-8)
    mask = heatmap > threshold
    return mask.astype(np.uint8)
