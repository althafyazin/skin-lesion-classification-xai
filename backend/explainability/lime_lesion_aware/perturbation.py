import numpy as np

def apply_patch_perturbation(image, patch):
    perturbed = image.copy()
    perturbed[patch] = 0
    return perturbed
