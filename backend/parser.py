import PyPDF2
import re

def extract_text_from_pdf(file_object):
    """
    Extracts and cleans text from a PDF file object.
    Returns cleaned text string or empty string on failure.
    """
    try:
        reader = PyPDF2.PdfReader(file_object)
        full_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

        return clean_text(full_text)

    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def clean_text(text):
    """
    Cleans extracted PDF text:
    - Remove excessive whitespace
    - Remove special characters that aren't useful
    - Normalize line breaks
    """
    # Replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace multiple newlines with single newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
    return text.strip()
