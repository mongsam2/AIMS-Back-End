import os
import torch
import onnxruntime
from torchvision import models
from functools import lru_cache

from django.conf import settings
MODEL_DIR = os.path.join(settings.BASE_DIR, "documents/models")


@lru_cache(maxsize=1)
def load_pytorch_model(model_name="student_model.pth"):
    
    model_path = os.path.join(MODEL_DIR, model_name)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 가중치 파일이 존재하지 않습니다: {model_path}")

    model = models.mobilenet_v3_small(weights=None)
    model.classifier[3] = torch.nn.Linear(1024, 6)

    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    print(f"model load completed: {model_path}")

    return model


@lru_cache(maxsize=1)
def load_onnx_model(model_name="student_model.onnx"):
    
    model_path = os.path.join(MODEL_DIR, model_name)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ONNX 모델 파일이 존재하지 않습니다: {model_path}")

    session = onnxruntime.InferenceSession(model_path, providers=["CPUExecutionProvider"])
    print(f"ONNX Model Loaded: {model_path}")
    
    return session







