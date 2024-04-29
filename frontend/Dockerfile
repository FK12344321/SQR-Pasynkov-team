FROM python:3.11
WORKDIR /app
COPY poetry.lock pyproject.toml ./
ENV PIP_DEFAULT_TIMEOUT=900
RUN pip install poetry && poetry install --no-root
COPY src/*.py ./
EXPOSE 9000
CMD [ "poetry", "run", "streamlit", "run", "main.py", "--server.port=9000", "--server.address=0.0.0.0" ]