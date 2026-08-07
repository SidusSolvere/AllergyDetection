import numpy as np
import tensorflow as tf
import keras

class AllergyPredictor:
    def __init__(self, model_path: str):
        self.model = keras.saving.load_model(model_path)

    def predict(self, img: np.ndarray) -> dict:
        resized = tf.image.resize(img, (256, 256))
        sev = float(self.model.predict(np.expand_dims(resized / 255.0, 0))[0][0])
        return self._interpret(sev)

    def _interpret(self, sev: float) -> dict:
        if sev < 0.1: result = "Severe allergy. Please visit a doctor immediately."
        elif sev < 0.3: result = "Moderate allergy. Please consult a doctor."
        elif sev < 0.5: result = "Mild allergy. Monitor the condition."
        elif sev < 0.7: result = "Low chance of allergy. Keep an eye on symptoms."
        else: result = "No signs of allergy."
        return {"result": result, "severity": round(1 - sev, 4), "severity_percentage": round((1 - sev) * 100, 2)}