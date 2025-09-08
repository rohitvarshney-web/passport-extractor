# Use slim Python
FROM python:3.11-slim


# system deps for pdf2image and poppler + tesseract (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
poppler-utils \
tesseract-ocr \
libgl1 && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app


EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "extract_passport_from_pdf:app"]
