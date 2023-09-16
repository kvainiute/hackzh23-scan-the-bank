from PyPDF2 import PdfReader
from pathlib import Path
import pandas
import magic

def convert(file_path):
    suffix = Path(file_path).suffix
    mime = magic.from_file(file_path, mime=True)
    print(suffix, mime)
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
        case '.ps1':
            return

