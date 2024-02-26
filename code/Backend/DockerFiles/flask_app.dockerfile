from python:3.11.8-slim

RUN mkdir -p /app
COPY Flask_App/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

COPY Flask_App /app
WORKDIR /app

CMD gunicorn --config /app/gunicorn_config.py app:app