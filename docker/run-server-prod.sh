#!/bin/bash
echo ----------------------------
echo killing old docker processes
echo ----------------------------
docker-compose rm -fs
echo ----------------------------
echo building and running docker containers
echo ----------------------------
docker-compose up --build -d
echo ----------------------------
echo waiting for db to set-up...
echo ----------------------------
sleep 20
echo ----------------------------
echo collecting static files
echo ----------------------------
docker-compose exec backend python manage.py collectstatic --noinput
echo ----------------------------
echo flushing and migrating data from fixtures
echo ----------------------------
docker-compose exec backend python manage.py flush --no-input
docker-compose exec backend python manage.py migrate
echo ----------------------------
echo creating super user
echo ----------------------------
docker-compose exec backend python manage.py createsuperuser --noinput
echo ----------------------------
echo success
echo ----------------------------