#!/bin/bash

EVENT_TYPE=$1
SOURCE_PATH=$2
TARGET_PATH=$3  # Only used for rename events

# Set the API URL
API_URL="http://localhost:8000/event-update/"

# Construct the JSON payload
if [ "$EVENT_TYPE" == "renamed" ]; then
    JSON_PAYLOAD=$(jq -n --arg path "$TARGET_PATH" --arg old_path "$SOURCE_PATH" --arg type "$EVENT_TYPE" \
    '{path: $path, old_path: $old_path, type: $type}')
else
    JSON_PAYLOAD=$(jq -n --arg path "$SOURCE_PATH" --arg type "$EVENT_TYPE" \
    '{path: $path, type: $type}')
fi

# Send the HTTP POST request to Django
curl -X POST -H "Content-Type: application/json" -d "$JSON_PAYLOAD" $API_URL