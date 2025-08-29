import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mimetypes
from Documents.PdfLoader import LoadPDF
from Documents.DocxLoader  import LoadDOCX
from Documents.TextLoader  import TextLoader
from Documents.PPTLoader import LoadPPTX
def detect_file_type(filename):
    ext = filename.lower().split('.')[-1]  # Get extension safely

    if ext == 'pdf':
        return "PDF"
    elif ext == 'txt':
        return "Text"
    elif ext == 'docx':
        return "DOCX"
    elif ext == 'pptx':
        return "PPTX"
    else:
        return "Unknown"
def Loader(file):
    text = ""
    mime_type, _ = mimetypes.guess_type(file)
    
    # PDF
    if detect_file_type(file)=="PDF":
        document=LoadPDF(file)
        return document


 # DOCX
    elif detect_file_type(file)=="DOCX":
        doc = LoadDOCX(file)
        return doc

    # TXT
    elif detect_file_type(file)=="Text":
        text = TextLoader(file)
        print(type(text))

    # PPTX
    elif detect_file_type(file)=="PPTX":
        prs = LoadPPTX(file)
        return prs

    else:
        text = "⚠️ Unsupported file type"
        return text
