#!/bin/sh

cd auth
sudo docker-compose stop
cd ..

cd django
sudo docker-compose stop
cd ..

cd flask
sudo docker-compose stop
cd ..

cd shared
sudo docker-compose stop
cd ..
