#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/admin/deployment #helloworld
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop flaskdemo
docker rm flaskdemo
docker rmi gading09/deployment:pe2
docker run -d --name flaskdemo -p 5000:5000 gading09/deployment:pe2