FROM python:3.11.12-slim

RUN mkdir /marketplace

WORKDIR /marketplace

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /marketplace/docker/app.sh

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]