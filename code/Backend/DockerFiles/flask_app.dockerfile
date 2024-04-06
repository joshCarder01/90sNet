from python:3.11.8-slim

# Setup redis daemon
RUN apt update && apt install -y redis systemctl && \
    apt clean && rm -rf /var/lib/apt/lists/*

EXPOSE 6379
RUN systemctl enable --now redis-server

RUN mkdir -p /app
COPY Flask_App/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

COPY Flask_App /app
WORKDIR /app

CMD bash /app/start_container.sh