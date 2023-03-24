import docx2txt
import re
import PyPDF2


# Load the docx file
text = docx2txt.process('resume.docx')

# Use regex to extract email, name, and phone number
email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
name = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', text)
phone = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)

print("Email:", email[0])
print("Name:", name[0])
print("Phone:", phone[0])

# Load the PDF file
pdf_file = open('resume.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Extract text from the PDF file
text = ""
for page in range(pdf_reader.getNumPages()):
    text += pdf_reader.getPage(page).extractText()

# Use regex to extract email, name, and phone number
email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
name = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', text)
phone = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)

print("Email:", email[0])
print("Name:", name[0])
print("Phone:", phone[0])
