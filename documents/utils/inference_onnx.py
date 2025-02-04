import os
import onnxruntime
import numpy as np

from django.conf import settings
from documents.utils.data_loader import preprocess_image


MODEL_DIR = os.path.join(settings.BASE_DIR, "documents/models")


def load_onnx_model(model_name="student_model.onnx"):
    
    model_path = os.path.join(MODEL_DIR, model_name)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ONNX 모델 파일이 존재하지 않습니다: {model_path}")

    session = onnxruntime.InferenceSession(model_path, providers=["CPUExecutionProvider"])
    print(f"ONNX Model Loaded: {model_path}")
    
    return session


def predict_onnx(image_path, class_labels):
    
    session = load_onnx_model()
    image = preprocess_image(image_path)
    
    inputs = {session.get_inputs()[0].name: image}
    output = session.run(None, inputs)[0]

    predicted_class = np.argmax(output, axis=1).item()
    confidence = np.max(output).item()

    return class_labels[predicted_class], confidence