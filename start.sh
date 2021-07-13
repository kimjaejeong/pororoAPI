#################################
# !/bin/bash

# Apply database migrations
echo "Apply database migrations"
python ./pororo_api/manage.py makemigrations
python ./pororo_api/manage.py migrate --fake-initial

# Start server
echo "Start server"
python ./pororo_api/manage.py runserver 0.0.0.0:9000
