!# /usr/bin/env bash
#let the database start
python ./app/backend_prestart.py

#run migrations
alembic upgrade head

#create initial data
python ./app/initial_data.py

read -p
