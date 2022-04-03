#! /bin/bash

[[ $DEBUG == true ]] && set -x
set -euo pipefail

if [ ! -f .env ]; then
    echo "Can't find .env file"
    exit 1
fi

export $(cat '.env' | sed 's/#.*//g'| xargs)

docker exec -w /app "$CN_CODE" python run.py
