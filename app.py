import streamlit as st
import pdfplumber
import spacy
import re

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Predefined skills list (Extend this as needed)
SKILLS = [
    "Python", "Java", "C++", "JavaScript", "SQL", "Machine Learning",
    "Data Science", "Deep Learning", "NLP", "TensorFlow", "Pandas",
    "Django", "Flask", "Project Management", "Agile", "Scrum", "Git",
    "Cloud Computing", "AWS", "Docker", "Kubernetes"
]

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Function to extract details
def extract_details(text):
    doc = nlp(text)

    # Extract email
    email = None
    email_match = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    if email_match:
        email = email_match.group()

    # Extract phone number
    phone = None
    phone_match = re.search(r"\+?\d[\d -]{8,15}\d", text)
    if phone_match:
        phone = phone_match.group()

    # Override extracted name with "Tejas Kulkarni"
    name = "Tejas Kulkarni"

    # Extract skills from predefined list
    skills_found = [skill for skill in SKILLS if skill.lower() in text.lower()]

    return {
        "Name": name,  # Always "Tejas Kulkarni"
        "Email": email,
        "Phone": phone,
        "Skills": skills_found
    }

# Streamlit Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Resume Parser", "View Results"])

# Global variable to store parsed data
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = {}

# Home Page
if page == "Home":
    st.title("Welcome to Resume Parser")
    st.write("This tool extracts key details from resumes, such as Name, Email, Phone, and Skills.")

# Resume Parser Page
elif page == "Resume Parser":
    st.title("Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

    if uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
        parsed_data = extract_details(extracted_text)
        st.session_state.parsed_data = parsed_data
        st.success("Resume successfully processed! Go to 'View Results' to see the extracted details.")

# View Results Page
elif page == "View Results":
    st.title("Extracted Resume Details")
    if st.session_state.parsed_data:
        st.json(st.session_state.parsed_data)
    else:
        st.warning("No resume has been processed yet. Please go to 'Resume Parser' to upload a resume.")
