import pdfplumber
import spacy
import io
from concurrent.futures import ThreadPoolExecutor

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model 'en_core_web_sm' not found. Text processing will be basic.")
    nlp = None

def extract_page_text(page):
    """Extract text from a single PDF page"""
    try:
        return page.extract_text() or ""
    except Exception:
        return ""

def extract_text_fast(resume_file, max_pages=3):
    """
    Fast and reliable text extraction without parallel processing
    """
    text = ""
    try:
        # Reset file pointer if it's a file-like object
        try:
            if hasattr(resume_file, 'seek'):
                resume_file.seek(0)
        except Exception:
            pass  # Continue even if seek fails

        with pdfplumber.open(resume_file) as pdf:
            # Limit pages for faster processing (most resumes are 1-3 pages)
            pages_to_process = pdf.pages[:max_pages]

            # Process sequentially to avoid hanging issues
            for i, page in enumerate(pages_to_process):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

                    # Break early if we have enough text
                    if len(text) > 3000:
                        break

                except Exception as e:
                    print(f"Error extracting page {i}: {e}")
                    continue

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

    # Limit text length for faster processing
    if len(text) > 3000:
        text = text[:3000]  # Keep first 3000 characters for speed

    return text.lower() if text else ""

def extract_text(resume_file):
    """
    Standard text extraction with fallback for different file types
    """
    try:
        # Check if it's a text file or has text content
        if hasattr(resume_file, 'getvalue'):
            content = resume_file.getvalue()
            if isinstance(content, bytes):
                try:
                    # Try to decode as text first
                    text_content = content.decode('utf-8')
                    return text_content.lower()[:3000]  # Limit length
                except UnicodeDecodeError:
                    pass  # Continue to PDF extraction

        # Try PDF extraction
        return extract_text_fast(resume_file)

    except Exception as e:
        print(f"Error in text extraction: {e}")
        # Last resort: try to read as plain text
        try:
            if hasattr(resume_file, 'read'):
                try:
                    resume_file.seek(0)
                except Exception:
                    pass  # Continue even if seek fails
                content = resume_file.read()
                if isinstance(content, bytes):
                    return content.decode('utf-8', errors='ignore').lower()[:3000]
                else:
                    return str(content).lower()[:3000]
        except Exception:
            pass

        return ""
