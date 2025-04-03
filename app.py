import fitz
import docx

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def main():
    print("Resume Parser")
    file_path = input("Enter the file path of the resume (PDF or DOCX): ")
    
    if file_path.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_path)
    else:
        extracted_text = "Unsupported file format."
    
    print("\nExtracted Text:\n")
    print(extracted_text)

if __name__ == "__main__":
    main()
