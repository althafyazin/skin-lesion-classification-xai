from keras.models import load_model
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "incepx_ensemble_best.keras")

def load_trained_model():
    model = load_model(MODEL_PATH, compile=False)
    return model
