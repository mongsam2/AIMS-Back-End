import os
import fitz  # PyMuPDF
import numpy as np

from PIL import Image
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate


def pdf_to_images(pdf_path, output_folder="temp_images"):
    """
    PDF 파일을 이미지(PNG)로 변환
    """
    os.makedirs(output_folder, exist_ok=True)
    pdf_doc = fitz.open(pdf_path)
    image_paths = []
    
    for i, page in enumerate(pdf_doc):
        img = page.get_pixmap(dpi=300) # 원본 pdf의 dpi 확인하기
        image_path = os.path.join(output_folder, f"page_{i + 1}_original.png")
        img.save(image_path)
        image_paths.append(image_path)
    
    pdf_doc.close()
    return image_paths


def rotate_and_crop(image_path, output_path):
    """
    이미지를 주어진 각도로 회전하고 원고지 영역만 crop
    """
    img = Image.open(image_path)

    x = np.array(img)
    angle = get_angle(x)

    output_image = rotate(x, angle)
    rotate_img = Image.fromarray(output_image)
    crop_img = rotate_img.crop((54, 1050, 3430, 4810)) # 원고지 있는 구역만 crop -> 예외 생각해야 함

    crop_img.save(output_path)


def preprocess_pdf(pdf_path, output_pdf_path):
    """
    PDF 문서를 처리하여 모든 페이지를 전처리한 새 PDF 생성
    """
    # PDF를 이미지로 변환
    images = pdf_to_images(pdf_path)

    preprocessed_images = []
    for image_path in images:
        preprocess_path = image_path.replace(".png", "_preprocess.png")
        rotate_and_crop(image_path, preprocess_path)
        preprocessed_images.append(preprocess_path)
    
    # 이미지를 PDF로 합치기
    pdf_doc = fitz.open()
    for preprocessed_image in preprocessed_images:
        img_doc = fitz.open(preprocessed_image)
        pdf_bytes = img_doc.convert_to_pdf()
        img_pdf = fitz.open("pdf", pdf_bytes)
        pdf_doc.insert_pdf(img_pdf)
    
    pdf_doc.save(output_pdf_path)
    pdf_doc.close()