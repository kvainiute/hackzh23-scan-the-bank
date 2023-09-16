from PyPDF2 import PdfReader
from pathlib import Path
import pandas
from docx2python import docx2python
import pytesseract
from PIL import Image
from zipfile import ZipFile
import magic
import extract_msg


def convert(file_path):
    suffix = Path(file_path).suffix
    mime = magic.from_file(file_path, mime=True)
    if 'text/' in mime:
        file_content = open(file_path, encoding='utf-8').read()
        return file_content
    else:
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
            case '.jpg':
                return convertImage(file_path)
            case '.png':
                return convertImage(file_path)
            case '.zip':
                contents = []
                with ZipFile(file_path) as zf:
                    zf.extractall('app/files/')
                    for file in zf.namelist():
                        unzipped_file_path = 'app/files/' + file
                        result = convert(unzipped_file_path)
                        contents.append(result)
                return '\n'.join(contents)
            case '.msg':
                return extract_msg.Message(file_path).getJson()
            case '.log':
                file_content = open(file_path, encoding='utf-8').read()
                return file_content
        return IOError('File cannot be converted')

def convertImage(file_path):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)

