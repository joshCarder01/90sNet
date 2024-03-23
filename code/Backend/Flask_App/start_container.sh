#! /bin/bash

# Starts redis service inline with the system, I don't really care about anything else
redis-server /etc/redis/redis.conf --daemonize yes

gunicorn --config /app/gunicorn_config.py app:app

wait -n

exit $#