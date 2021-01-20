#!/bin/sh

cd auth
sudo docker-compose restart
cd ..

cd django
sudo docker-compose restart
cd ..

cd flask
sudo docker-compose restart
cd ..

cd shared
sudo docker-compose restart
cd ..
