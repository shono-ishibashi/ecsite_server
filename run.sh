#!/bin/sh

sudo docker network create --driver bridge common_link

cd auth
sudo docker-compose up -d
cd ..

cd django
sudo docker-compose up -d
cd ..

cd flask
sudo docker-compose up -d
cd ..

cd shared
sudo docker-compose up -d
cd ..
