from PIL import Image
import pytesseract
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pydeepl

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def detectText(image_path):
    # Simple image to string
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def detectLanguage (string):
    from langdetect import DetectorFactory
    from langdetect import detect
    from langdetect import lang_detect_exception
    DetectorFactory.seed = 0

    try:
         return detect(string.lower())
    except lang_detect_exception.LangDetectException as e:
        return "vier"

def extractMentions(string):
    mentions = re.findall("@([a-zA-Z0-9_]{1,15})", string)
    return mentions

def extractHashtags(string):
    hashtags = re.findall("#([a-zA-Z0-9]{1,15})", string)
    return hashtags

# Remove mentions, hashtags and url from string
def cleanText(string):
    return ' '.join(re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", string).split())

def analysisSentimentVader(string):
    string = cleanText(string)
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(string)

def analysisSentimentTextBlob(string):
    string = cleanText(string)
    testimonial = TextBlob(string)
    return testimonial.sentiment

def translateDeepL(string):
    string = cleanText(string)
    # Using auto-detection
    return pydeepl.translate(string, to_lang="EN")