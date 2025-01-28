import fitz  # PyMuPDF
import numpy as np

from PIL import Image
from io import BytesIO

from jdeskew.estimator import get_angle
from jdeskew.utility import rotate


def preprocess_pdf(pdf_path, output_path, manuscript_box=(54, 1050, 3430, 4810), dpi=300):
    
    pdf_doc = fitz.open(pdf_path)
    preprocessed_images = []

    for page in pdf_doc:
        pixmap = page.get_pixmap(dpi=dpi)
        img = Image.open(BytesIO(pixmap.tobytes("png")))

        # rotate 및 crop 수행
        rotated_img = rotate(np.array(img), get_angle(np.array(img)))
        cropped_img = Image.fromarray(rotated_img).crop(manuscript_box)

        img_bytes = BytesIO()
        cropped_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        img_doc = fitz.open("pdf", fitz.open(stream=img_bytes.read(), filetype="png").convert_to_pdf())
        preprocessed_images.append(img_doc)

    output_pdf = fitz.open()
    for img_pdf in preprocessed_images:
        output_pdf.insert_pdf(img_pdf)

    output_pdf.save(output_path)
    output_pdf.close()