import google.generativeai as genai
import os
import cv2
from PIL import Image
import numpy as np

def extract_text_image(image_file):
    # Read uploaded file as bytes
    file_bytes = np.frombuffer(image_file.read(), np.uint8)

    if file_bytes.size == 0:
        raise ValueError("Uploaded file is empty or could not be read")

    # Decode image with OpenCV
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("OpenCV could not decode the uploaded image. "
                         "Check file format (jpg, jpeg, png).")

    # Convert to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to grayscale + threshold to black and white
    image_grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, image_bw = cv2.threshold(image_grey, 150, 255, cv2.THRESH_BINARY)

    # Convert back to PIL for Gemini
    final_image = Image.fromarray(image_bw)

    # ✅ Configure Gemini API with your key
    genai.configure(api_key="AIzaSyAd0ryPa58oDWVJOOlyck11oOPMHnJn2_A")

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = """You act as an OCR application on the given image and extract the text 
    from it. Give only the text as output, no explanation or description."""

    # Send image + prompt to Gemini
    response = model.generate_content([prompt, final_image])
    return response.text
