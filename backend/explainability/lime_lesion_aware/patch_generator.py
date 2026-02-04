# backend/explainability/patch_generator.py

import numpy as np
from skimage.segmentation import slic

def lesion_patches(mask, image, n_segments=50):
    """
    Generate lesion-aware patches using superpixels.
    Only superpixels overlapping the lesion ROI are kept.
    """

    segments = slic(
        image,
        n_segments=n_segments,
        compactness=10,
        start_label=0
    )

    patches = []

    for seg_id in np.unique(segments):
        seg_mask = segments == seg_id

        # keep only lesion-overlapping superpixels
        overlap = np.sum(seg_mask & mask) / (np.sum(seg_mask) + 1e-8)
        if overlap > 0.15:
            patches.append(seg_mask)

    return patches
