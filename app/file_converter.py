from PyPDF2 import PdfReader
from pathlib import Path
import pandas
from docx2python import docx2python

def convert(file_path):
    suffix = Path(file_path).suffix
    match suffix:
        case '.pdf':
            reader = PdfReader(file_path)
            text = ''
            number_of_pages = len(reader.pages)
            for page in range(number_of_pages):
                text += reader.pages[page].extract_text()
            return text
        case '.xlsx':
            return pandas.read_excel(file_path).to_string()
        case '.docx':
            with docx2python(file_path, 'app/misc/') as docx_content:
                return docx_content.text
        # case '.jpg':
        # case '.png':
    return IOError('File cannot be converted')

