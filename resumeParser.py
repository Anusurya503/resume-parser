import docx2txt
import PyPDF2
import re
import spacy
import pandas as pd 
from spacy.matcher import PhraseMatcher


# Load the NLP model
nlp = spacy.load('en_core_web_sm')

# Define a function to extract text from a file
def extract_text(file_path):
    try:
        if file_path.endswith('.docx'):
            # Load the docx file
            text = docx2txt.process(file_path)
        elif file_path.endswith('.pdf'):
            # Load the PDF file
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                # Extract text from the PDF file
                text = ""
                for page in range(pdf_reader.getNumPages()):
                    text += pdf_reader.getPage(page).extractText()
        else:
            raise ValueError('Unsupported file format')
    except:
        print("Error: Failed to extract text from file.")
        return ""
    
    text = str(text)
    return text


skills_df = pd.read_csv("skills.csv")
print("====================>>>>>>>>>>>>>",skills_df.columns)
skills_df.rename(columns = {'(ISC)2':'Skill'}, 
            inplace = True)
  
skills = list(skills_df["Skill"].values)

# Create a phrase matcher with the skills as patterns
matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(str(skill) )for skill in skills]
matcher.add("Skills", None, *patterns)


def extract_skills(resume_text):
    doc = nlp(resume_text)
    matches = matcher(doc)
    skills = [doc[start:end].text for match_id, start, end in matches]
    return skills


# Define a function to extract email, name, and phone number from text using regex and NLP
def extract_info(text):
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    name = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', text)
    phone = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    linkedin = None
    github = None
    location = None
    college_name = None
    degree = None
    designation = None
    company_names = []
    
    doc = nlp(text)
    
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ == "EMAIL" and not email:
            email = ent.text
        elif ent.label_ == "PHONE" and not phone:
            phone = ent.text
        elif ent.label_ == "ORG" and "linkedin" in ent.text.lower():
            linkedin = ent.text.strip()
        elif ent.label_ == "ORG" and "github" in ent.text.lower():
            github = ent.text.strip()
        elif ent.label_ == "GPE":
            location = ent.text.strip()
        elif ent.label_ == "ORG" and "university" in ent.text.lower():
            college_name = ent.text
        elif ent.label_ == "EDUCATION":
            degree = ent.text
        elif ent.label_ == "TITLE":
            designation = ent.text
        elif ent.label_ == "ORG" and "university" not in ent.text.lower():
            company_names.append(ent.text)

    return email, name, phone, linkedin, github, location, college_name, degree, designation, company_names


file_path = 'Michael.pdf'
text = extract_text(file_path)
email, name, phone, linkedin, github, location, college_name, degree, designation, company_names= extract_info(text)
skills = extract_skills(text)
print("Email:", email[0])
print("Name:", name[0])
print("Phone:", phone)
print("LinkedIn:", linkedin)
print("GitHub:", github)
print("Location:", location)
print("College name:", college_name)
print("Degree:", degree)
print("Designation:", designation)
print("Company names:", company_names)
print("Skills:", skills)



    