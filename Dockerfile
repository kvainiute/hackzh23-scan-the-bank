FROM python:3.11
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install git-lfs && git clone https://huggingface.co/dslim/bert-base-NER models/bert-base-NER
RUN apt-get update && apt-get -y install tesseract-ocr
RUN pip install --upgrade pip
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY app /app
WORKDIR /app
CMD ["python", "crawler.py"]