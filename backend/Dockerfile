FROM python:3.11
COPY poetry.lock pyproject.toml ./
RUN pip install poetry && poetry install --no-root
COPY app/ /app/
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]