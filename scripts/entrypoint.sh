#!/usr/bin/bash

# Start API backbone service with time out
gunicorn --pythonpath /app -b 0.0.0.0:$API_SERVER_PORT -t $API_SERVER_TIMEOUT -k $CLASS_TYPE -w $NUMBER_WORKER_PROCESS main:app
