from PIL import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def detectText(image_path):
    # Simple image to string
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def detectLanguage (text):
    from langdetect import DetectorFactory
    from langdetect import detect
    from langdetect import lang_detect_exception
    DetectorFactory.seed = 0

    try:
         return detect(text.lower())
    except lang_detect_exception.LangDetectException as e:
        return "vier"