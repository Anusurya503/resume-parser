import spacy
import pytesseract
from PIL import Image

nlp = spacy.load("en_core_web_sm")

# Load the resume image using Pillow
image = Image.open("resume.jpeg")

# Perform OCR using pytesseract
text = pytesseract.image_to_string(image)
print(text)

# Perform NLP using spaCy
doc = nlp(text)

# Extract the name and email
name = ""
email = ""

for ent in doc.ents:
    print(doc.ents)
    if ent.label_ == "PERSON":
        name = ent.text
    elif ent.label_ == "EMAIL":
        email = ent.text

print("Name:", name)
print("Email:", email)
