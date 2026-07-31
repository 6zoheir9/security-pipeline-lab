FROM python:3.11-slim@sha256:39f1c7d23d8c117b38d33e50669d0339d1b0d26e2e50cf6bb0eb5c30b91d2109
WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN useradd -m myuser
USER myuser

EXPOSE 5000
CMD ["python", "app.py"]