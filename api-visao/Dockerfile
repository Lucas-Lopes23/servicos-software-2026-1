FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install -y \
    tesseract-ocr\
    tesseract-ocr-por\
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "from transformers import pipeline; pipeline('image-to-text', model='Salesforce/blip-image-captioning-base')"
COPY main.py /code/
EXPOSE 8081
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]