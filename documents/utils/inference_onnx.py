import os
import onnxruntime

from django.conf import settings


MODEL_DIR = os.path.join(settings.BASE_DIR, "documents/models")


def load_onnx_model(model_name="student_model.onnx"):
    
    model_path = os.path.join(MODEL_DIR, model_name)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ONNX 모델 파일이 존재하지 않습니다: {model_path}")

    session = onnxruntime.InferenceSession(model_path, providers=["CPUExecutionProvider"])
    print(f"ONNX Model Loaded: {model_path}")
    
    return session


