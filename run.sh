#!/bin/bash

# to stop on first error
set -e

# Delete older .pyc files
# find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Run required migrations
export FLASK_APP=core/server.py

# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/

# Run server
# gunicorn -c gunicorn_config.py core.server:app
# Check the operating system and run the appropriate server
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # For Linux or macOS
    echo "Running on Linux or macOS. Starting with Gunicorn..."
    gunicorn -c gunicorn_config.py core.server:app
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # For Windows environments
    echo "Running on Windows. Starting with Waitress..."
    python -m waitress 'core.server:app'
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi