FROM python:3.8

WORKDIR /app

COPY  ..

RUN pip install requirements.txt

EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
