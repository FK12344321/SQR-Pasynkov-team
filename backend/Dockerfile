FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY app/ .
EXPOSE 8000
CMD ["python", "-m", "gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]