#!/bin/bash

docker build --platform linux/amd64 --tag sqr-backend .
docker image tag sqr-backend fk12344321/sqr-backend:latest
docker push fk12344321/sqr-backend:latest

ssh -i ~/.ssh/ssd root@10.90.137.146 <<EOF
docker pull fk12344321/sqr-backend:latest
docker stop backend
docker rm backend
docker run --name backend -v /pasynkov.db:/pasynkov.db -d --rm -p 8000:8000 fk12344321/sqr-backend:latest
EOF
