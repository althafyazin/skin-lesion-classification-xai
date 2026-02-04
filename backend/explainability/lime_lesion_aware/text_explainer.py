import numpy as np

def generate_text_explanation(weights):
    important = np.argsort(weights)[-3:]
    return (
        "The prediction is mainly influenced by lesion regions "
        f"{important.tolist()}, suggesting localized structural patterns."
    )
