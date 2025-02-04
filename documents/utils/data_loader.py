import os
from PIL import Image

from torchvision import transforms
from pdf2image import convert_from_path


def pdf_to_image(pdf_path, output_folder="/data/ephemeral/home/tmp", dpi=300):
    """
    PDF 파일을 이미지로 변환하여 첫 번째 페이지를 반환
    
    Args:
        pdf_path (str): 변환할 PDF 파일 경로
        output_folder (str): 변환된 이미지 저장 경로 (기본값: /tmp)
        dpi (int): 변환 시 해상도 설정 (기본값: 300)
    
    Returns:
        image_path (str): 변환된 첫 번째 페이지 이미지 경로
    """
    os.makedirs(output_folder, exist_ok=True)

    images = convert_from_path(pdf_path, dpi=dpi, output_folder=output_folder, fmt="png", first_page=1, last_page=1)
    if not images:
        raise ValueError("PDF 변환 실패!")

    saved_images = [f for f in os.listdir(output_folder) if f.endswith(".png")]
    saved_images.sort()

    if not saved_images:
        raise ValueError("변환된 이미지 파일이 존재하지 않습니다!")

    image_path = os.path.join(output_folder, saved_images[0])

    return image_path


def preprocess_image(file_path):
    """
    파일 경로를 입력받아 이미지 전처리를 수행하는 함수.
    PDF 파일이 입력되면 먼저 이미지로 변환 후 처리함.

    Args:
        file_path (str): 이미지 또는 PDF 파일 경로

    Returns:
        torch.Tensor: 전처리된 이미지 텐서
    """
    
    if file_path.lower().endswith(".pdf"):
        file_path = pdf_to_image(file_path)

    image = Image.open(file_path).convert("RGB")

    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image = transform(image).unsqueeze(0)

    os.remove(file_path)
    print(f"🗑️ 변환된 이미지 삭제 완료: {file_path}")

    return image


