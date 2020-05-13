#!/usr/bin/bash

# Wait for the required to be up, before we attempt to start the web-workers.
URL="http://$GREMLIN_DEFAULT_HOST:$GREMLIN_DEFAULT_PORT"
echo "Curl Gremlin Server @ $URL"
while ! curl --data '{"gremlin":"1"}' --output /dev/null --silent --fail "$URL"
do
    sleep 2 && echo "Waiting for Gremlin HTTP Server..."
done

echo "Skip schema flag : $SKIP_SCHEMA"
if [ ! -z "$SKIP_SCHEMA" ]; then
    echo "Creating schema based on groovy script"
    python3 /app/populate_schema.py
fi

echo "Starting API service"
# Start API backbone service with time out
gunicorn --pythonpath /app -b 0.0.0.0:$API_SERVER_PORT -t $API_SERVER_TIMEOUT -k $CLASS_TYPE -w $NUMBER_WORKER_PROCESS main:app
