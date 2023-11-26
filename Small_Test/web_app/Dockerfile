FROM python:alpine

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt \
        && mkdir /app && rm /requirements.txt

COPY ./app/ /app

WORKDIR /app

ENTRYPOINT ["python"]
CMD ["/app/__init__.py"]
EXPOSE 8080
