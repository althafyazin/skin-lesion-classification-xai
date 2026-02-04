# backend/explainability/confidence.py

import numpy as np


def explanation_confidence(weights):
    """
    Measures explanation strength / stability
    """
    weights = np.asarray(weights)
    return float(np.sum(np.abs(weights)) / (len(weights) + 1e-8))


def confidence_level(conf):
    """
    Converts numeric score to human-readable certainty
    """
    if conf > 0.7:
        return "high confidence"
    elif conf > 0.4:
        return "moderate confidence"
    else:
        return "low confidence"
