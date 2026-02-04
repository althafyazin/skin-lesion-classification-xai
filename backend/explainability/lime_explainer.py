import os
from lime import lime_image
from lime import lime_text
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

def generate_lime(image, model, pred_index):

    def predict_wrapper(images):
        return model.predict([images, images])

    explainer = lime_image.LimeImageExplainer()

    explanation = explainer.explain_instance(
        image,
        predict_wrapper,
        top_labels=5,
        hide_color=0,
        num_samples=200
    )

    label = explanation.top_labels[0]

    lime_img, mask = explanation.get_image_and_mask(
        label,
        positive_only=True,
        hide_rest=True,     # ✅ KEY CHANGE
        num_features=5     # ✅ FORCE VISIBILITY
    )

    lime_img = mark_boundaries(lime_img / 255.0, mask)

    os.makedirs(STATIC_DIR, exist_ok=True)
    path = os.path.join(STATIC_DIR, "lime.png")

    plt.imsave(path, lime_img)
