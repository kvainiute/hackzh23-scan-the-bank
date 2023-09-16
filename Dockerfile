FROM python:3.11
RUN git clone https://huggingface.co/dslim/bert-base-NER models/bert-base-NER
COPY app /app
WORKDIR /app
RUN apt-get update && apt-get -y install tesseract-ocr
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "crawler.py"]