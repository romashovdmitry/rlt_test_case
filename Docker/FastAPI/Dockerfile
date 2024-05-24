FROM python:3.10

WORKDIR /app

# Yerevan time
ENV TZ=Asia/Baku

COPY ./Docker/FastAPI/requirements.txt /app
COPY ./app /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload", "--reload-dir", "/app"]